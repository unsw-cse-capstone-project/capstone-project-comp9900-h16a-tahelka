#COMP9900 T3 2020 - Team Tahelka 
#42.2 seconds 

#install packages 
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import time 
from db_engine import Session
from models.Subscription import Subscription
from sqlalchemy import func
from os import path
from models.Genres import Genres
from models.GenreOfFilm import GenreOfFilm



import pip
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain   
pipmain(['install', 'nltk'])

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def getPerdictionsOfGenres(gen, movie_movie):

	 #create bag of words 
	bag = pd.DataFrame(columns = ['movieID','genre'])  
	for movieID in list(gen.movieID.unique()):
	    df = gen[gen.movieID == movieID]                                #get the list fo directors for that movie
	    bag_of_words = []
	    for i in range(len(df)):
	        bag_of_words.append(df.iloc[i,2])                           #append genre
	    bag_of_words = ' '.join(sentence for sentence in bag_of_words)
	   
	    data = [{'movieID': movieID,'words': bag_of_words}]                              
	    bag.loc[movieID]= list(data[0].values())     
	bag = bag.reset_index(drop= True, inplace = False) 


	#create inverse document frequency 
	count = TfidfVectorizer()                              				#count the occurence of each word in the bag of words for each movie, 
	                                                       				#take inverse frequency
	matrix = count.fit_transform(bag['genre'])          				#generating the count matrix
	cosine_sim = cosine_similarity(matrix, matrix)         				#cosine similarity matrix


	#Calculate the similarity scores 
	sim = pd.DataFrame(data=cosine_sim[0:,0:],        					# values
              index=bag.movieID,               							# set index
             columns=bag.movieID)              							# column names

	#reorganise column names 
	colNames = [float(movie) for movie in movie_movie.columns[1:]]         #get the columns names as floats excluding the first column
	sim = sim[colNames]                                                    #reorder the columns 
	sim = sim.reindex(colNames)                                            #reorder the rows
	
	#rename columns as strings
	sim.columns = [ str(int(movie)) for movie in sim.columns]           
    
	#round down 
	sim = sim.round(2)

	#save file
    recoDir = 'RecSystem'
    dataDir = 'RecoData'
    location = path.join(recoDir, dataDir)
    sim.to_csv(path.join(location, 'genre_movie.csv'),index=True)                        # save to file
    return 0

#read data from the database and compute the user_movie similarity table
def readWriteComputeGenrePred():
    session = Session()
    genreoffilm = pd.read_sql('genreOfFilm', session.bind)
    genre = pd.read_sql('genres', session.bind)
    gen = pd.merge(genreoffilm, genre, on = 'genreID')

    recoDir = 'RecSystem'
    dataDir = 'RecoData'
    location = path.join(recoDir, dataDir)
    movie_movie = pd.read_csv(path.join(location, 'movie_movie.csv'), header = 0)   #load the movie-movie file
      
    session.close()  
    return getPerdictionsOfGenres(gen, movie_movie)      












