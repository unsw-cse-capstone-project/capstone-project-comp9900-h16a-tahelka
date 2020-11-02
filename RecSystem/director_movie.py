#COMP9900 T3 2020 - Team Tahelka 
#50.0 seconds 

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


def director_movie_similarity(final, movie_movie):
	#clean up description
	stop_words = set(stopwords.words('english'))
	for i in range(len(final)):
	    try:
	        desc = final.iloc[i,2]
	        tokens = word_tokenize(desc)
	        words = [word for word in tokens if word.isalpha()]              #remove non alphanumerics
	        words = [word.lower() for word in words]                         #convert to lower case
	        words = [word for word in words if not word in stop_words]       #remove stopwords
	        final.iloc[i,2] = ' '.join(word for word in words)              #join as a single string
	    except:
	        final.iloc[i,2] = ''                                            #if nan replace with empty string
	 
	 #create bag of words 
	bag = pd.DataFrame(columns = ['movieID','words'])                                       #empty dataframe
	movieList = list(final.movieID.unique())
	for movieID in movieList: 
	    df = final[final.movieID == movieID]                                                #get the list fo directors for that movie
	    bag_of_words = []
	    for i in range(len(df)):
	        bag_of_words.append(df.iloc[i,0])                                            #append director name
	        bag_of_words.append(df.iloc[i,2])                                            #append director bio
	    bag_of_words = ' '.join(sentence for sentence in bag_of_words)
	    
	    data = [{'movieID': movieID,'words': bag_of_words}]                              
	    bag.loc[movieID]= list(data[0].values())                                         #new row of information
	bag = bag.reset_index(drop= True, inplace = False)                                   #reset index 


	#create inverse document frequency 
	count = TfidfVectorizer()                              #count the occurence of each word in the bag of words for each movie, 
                                                       #take inverse frequency
	matrix = count.fit_transform(bag['words'])             #generating the count matrix
	cosine_sim = cosine_similarity(matrix, matrix)         #cosine similarity matrix

	#Calculate the similarity scores 
	sim = pd.DataFrame(data=cosine_sim[0:,0:],        # values
	              index=bag.movieID,                  # set index
	             columns=bag.movieID)                 # column names

	#reorganise column names 
	colNames = [float(movie) for movie in movie_movie.columns[1:]]         #get the columns names as floats excluding the first column
	sim = sim[colNames]                                                    #reorder the columns 
	sim = sim.reindex(colNames)                                            #reorder the rows

	#save file 
	sim.to_csv('director_movie.csv',index=True)         # save to file
	return 0


#import dataset ----------- CHANGE TO DRAW FROM DATABASE ------------------------------
fd = pd.read_csv('FilmDirector.csv', header = 0) 
person = pd.read_csv('Person.csv', header = 0)
movie_movie = pd.read_csv('movie_movie.csv', header = 0)               #load the movie-movie file
final = pd.merge(person,fd,on='personID')
final = final.drop(columns = ['personID'])


#run file
start = time.time()
director_movie_similarity(final, movie_movie)
print(time.time() - start)












