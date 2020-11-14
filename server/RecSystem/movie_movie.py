#COMP9900 T3 2020 - Team Tahelka 
#92.57 seconds 

from os import path

# install packages
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from db_engine import Session

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import skipgrams

#skipgram function 
def skip_gram(window = None, words = None):
    return lambda bag_of_words: [w for w in skipgrams(word_tokenize(bag_of_words), window, words)]

def getPerdictionsOfMovies(fc, fd, person, genre, genlist, movies, review):
    fc = pd.merge(person,fc,on='personID')
    fd = pd.merge(person,fd,on='personID')
    person = fc.append(fd)
    person = person[['personID','name','movieID','bio']]
    movie_list = [int(movie) for movie in fd.movieID]

    #create movieid: cast list dictionary 
    movie_person = {key:[] for key in movie_list}
    for i in range(len(person)):
        movieID = int(person.iloc[i,2])
        movie_person[movieID].append(person.iloc[i,1]) #append the cast to the movieID key

    #create movieid: genre list dictionary 
    gen = pd.merge(genlist,genre,on='genreID')
    movie_genre = {key:[] for key in movie_list}
    for i in range(len(gen)):
        movieID = int(gen.iloc[i,2])
        movie_genre[movieID].append(gen.iloc[i,1]) #append the review to the movieID key
            
    #create movieid: reviews list dictionary
    movie_review = dict.fromkeys([int(movie) for movie in review.movieID],[])
    movie_review = {key:[] for key in movie_list}
    for i in range(len(review)):
        movieID = int(review.iloc[i,0])
        if type(review.iloc[i,3]) == str:                  #check if the review is not nan
            movie_review[movieID].append(review.iloc[i,3]) #append the review to the movieID key
            
    #append column of all genres of each movie and another column with all cast members of each movie
    movies['reviews'] = ''                                                                  #create new column 
    for i in range(len(movies)):
        movies.iloc[i,4] = [' '.join(word for word in movie_genre[movies.iloc[i,0]])]       #genre list for that movieid
        movies.iloc[i,5] = [' '.join(word for word in movie_person[movies.iloc[i,0]])]      #cast list for that movieid
        if len(movie_review[movies.iloc[i,0]]) != 0:
            movies.iloc[i,6] = ' '.join(r for r in movie_review[movies.iloc[i,0]])          #review list for that movieid    
    movies = movies.rename(columns = {'ratings_sum':'genre', 'review_count':'cast'})
    
    #Clean up description and reviews
    stop_words = set(stopwords.words('english'))
    for i in range(len(movies)):
        try:
            desc = movies.iloc[i,3]                                            #'description' 
            token_d = word_tokenize(desc)
            words_d = [word for word in token_d if word.isalpha()]             #remove non alphanumerics for 'description' 
            words_d = [word.lower() for word in words_d]                       #convert to lower case for 'description' 
            words_d = [word for word in words_d if not word in stop_words]     #remove stopwords for 'description' 
            movies.iloc[i,3] = ' '.join(word for word in words_d)              #join as a single string for 'description'
            
            rev = movies.iloc[i,6]                                             #'review'
            token_r = word_tokenize(rev)
            words_r = [word for word in token_r if word.isalpha()]             #remove non alphanumerics for 'review' 
            words_r = [word.lower() for word in words_r]                       #convert to lower case for 'review' 
            words_r = [word for word in words_r if not word in stop_words]     #remove stopwords for 'review' 
            movies.iloc[i,6] = ' '.join(word for word in words_r)              #join as a single string for 'review'
        except:
            movies.iloc[i,3] = ''                                             #if nan replace with empty string for 'description' 


    #create bag of words 
    for i in range(len(movies)):
        movies.iloc[i,1] = [str(movies.iloc[i,1]) + ' ' + str(movies.iloc[i,2]) + ' ' + str(movies.iloc[i,3]) + ' ' + str(movies.iloc[i,4])+ ' ' + str(movies.iloc[i,5]+ ' ' + str(movies.iloc[i,6]))]
    movies.drop(columns = ['year','description','genre','cast','reviews'], inplace = True)
    movies = movies.rename(columns = {'title':'bag_of_words'})

    #create inverse document frequency 
    count = TfidfVectorizer(tokenizer = skip_gram(window = 2, words = 10)) #counting the occurence of each 2 word combinations within a 10 word window for each movie, 
                                                                           #repeating for each movie, and taking the inverse document freuency 
    matrix = count.fit_transform(movies['bag_of_words'])                   #generating the count matrix
    cosine_sim = cosine_similarity(matrix, matrix)                         #cosine similarity matrix

    #Calculate the similarity scores 
    sim = pd.DataFrame(data=cosine_sim[0:,0:],        # values
                  index=movies.movieID,               # set index
                 columns=movies.movieID)         # column names
    
    #round down 
    sim = sim.round(2)

    #rename columns as strings
    sim.columns = [ str(int(movie)) for movie in sim.columns]           
    
    #save file
    recoDir = 'RecSystem'
    dataDir = 'RecoData'
    location = path.join(recoDir, dataDir)
    sim.to_csv(path.join(location, 'movie_movie.csv'),index=True)                        # save to file
    return 0

#read data from the database and compute the user_movie similarity table
def readWriteComputeMoviePred():
    session = Session()
    fc = pd.read_sql('filmCast', session.bind)
    fd = pd.read_sql('filmDirectors', session.bind)
    person = pd.read_sql('persons', session.bind)
    genre = pd.read_sql('genreOfFilm', session.bind)
    genlist = pd.read_sql('genres', session.bind)
    movies = pd.read_sql('movies', session.bind)
    review = pd.read_sql('movieReviews', session.bind)
      
    session.close()  
    return getPerdictionsOfMovies(fc, fd, person, genre, genlist, movies, review)          












