#COMP9900 T3 2020 - Team Tahelka 
#65.2 seconds 

#install packages 
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import time 
import pip
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain   
pipmain(['install', 'nltk'])

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def movie_movie_similarity(fc, fd, person, genre, genlist, movies):
	#create movieid: cast list dictionary 
	fc = pd.merge(person,fc,on='personID')
	fd = pd.merge(person,fd,on='personID')
	person = fc.append(fd)
	movie_person = dict()
	for i in range(len(person)):
	    if person.iloc[i,2] in movie_person:                                            #if the movie is in the dctionary then just append additional cast members
	        movie_person[person.iloc[i,2]].append(person.iloc[i,1].replace(" ", "")) 
	    else:           																#create a new key in the dictionary
	        movie_person[person.iloc[i,2]] = [person.iloc[i,1].replace(" ", "")]

	#create movieid: genre list dictionary 
	gen = pd.merge(genlist,genre,on='genreID')
	movie_genre = dict()
	for i in range(len(gen)):
	    if gen.iloc[i,2] in movie_genre: 												#if the movie is in the dctionary then just append additional genres           
	        movie_genre[gen.iloc[i,2]].append(gen.iloc[i,1])
	    else:   																		#create a new key in the dictionary
	        movie_genre[gen.iloc[i,2]] = [gen.iloc[i,1]]

	#append column of all genres of each movie and another column with all cast members of each movie
	for i in range(len(movies)):
	    movies.iloc[i,4] = [' '.join(word for word in movie_genre[movies.iloc[i,0]])]       #genre list for that movieid
	    movies.iloc[i,5] = [' '.join(word for word in movie_person[movies.iloc[i,0]])]      #cast list for that movieid  
	movies = movies.rename(columns = {'ratings_sum':'genre', 'review_count':'cast'})


	#Clean up description 
	stop_words = set(stopwords.words('english'))
	for i in range(len(movies)):
	    try:
	        desc = movies.iloc[i,3]
	        tokens = word_tokenize(desc)
	        words = [word for word in tokens if word.isalpha()]              #remove non alphanumerics
	        words = [word.lower() for word in words]                         #convert to lower case
	        words = [word for word in words if not word in stop_words]       #remove stopwords
	        movies.iloc[i,3] = ' '.join(word for word in words)              #join as a single string
	    except:
	        movies.iloc[i,3] = ''                                            #if nan replace with empty string

	#create bag of words 
	for i in range(len(movies)):
	    movies.iloc[i,1] = [str(movies.iloc[i,1]) + ' ' + str(movies.iloc[i,2]) + ' ' + str(movies.iloc[i,3]) + ' ' + str(movies.iloc[i,4])]
	movies.drop(columns = ['year','description','genre','cast'], inplace = True)
	movies = movies.rename(columns = {'title':'bag_of_words'})

	#create inverse document frequency 
	count = TfidfVectorizer()                              #count the occurence of each word in the bag of words for each movie, 
	                                                       #take inverse frequency
	matrix = count.fit_transform(movies['bag_of_words'])   #generating the count matrix
	cosine_sim = cosine_similarity(matrix, matrix)         #cosine similarity matrix

	#Calculate the similarity scores 
	sim = pd.DataFrame(data=cosine_sim[0:,0:],        # values
	              index=movies.movieID,               # set index
	             columns=movies.movieID)         # column names

	#save file 
	sim.to_csv('movie_movie.csv',index=True)         # save to file
	return 0


#import dataset ----------- CHANGE TO DRAW FROM DATABASE ------------------------------
fc = pd.read_csv('FilmCast.csv', header = 0) 
fd = pd.read_csv('FilmDirector.csv', header = 0) 
person = pd.read_csv('Person.csv', header = 0) 
genre = pd.read_csv('GenreOfFilm.csv', header = 0)
genlist = pd.read_csv('Genres.csv', header = 0)
movies = pd.read_csv('Movie.csv', header = 0) 

#run file
start = time.time()
movie_movie_similarity(fc, fd, person, genre, genlist, movies)
print(time.time() - start)












