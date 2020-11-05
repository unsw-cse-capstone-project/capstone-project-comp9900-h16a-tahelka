import pandas as pd 
import numpy as np 
# import time
#12.0 seconds (including reading the 4 files)

# start = time.time()
def movie_similarity_calc(movieID, userID, movie, director, genre, user,
                          use_genre, use_director, use_movie = 5, use_user = 1):
    #retrieve the rows and concatenate
    movie_row = movie[movie.movieID == movieID]               
    dir_row = director[director.movieID == movieID]
    genre_row = genre[genre.movieID == movieID]
    user_row = user[user.userID == userID]
    final = pd.concat([movie_row, dir_row, genre_row, user_row])
    totalMovies = len(movie_row.columns)

    #create weight matrix
    weights = (np.matrix([[use_movie,use_director,use_genre,use_user]]*totalMovies)).T

    #calculation
    final = final.set_index('movieID')
    final = final*weights
    sim_score = pd.DataFrame(final.sum(0))            #sum down each column
    # sim_score.columns = ['score']                     #rename
    # sim_score = sim_score.drop('movieID')             #delete movieID
    # sim_score = sim_score.drop(str(movieID))          #delete actual movieID score

    sim_score = sim_score.sort_values(by = 0, ascending = False) #sort
    limit = 12
    topMovies = [int(movie) for movie in list(sim_score.head(limit).index[2:])]
    return topMovies                    #return 10 best movies sim_score


'''
#SYSTEM INPUT -----------
movieID = 114709.0
userID = 2177.0
use_genre = 1
use_director = 1

#import dataset ----------- CHANGE TO DRAW FROM DATABASE ------------------------------
movie = pd.read_csv('movie_movie.csv', header = 0)
director = pd.read_csv('director_movie.csv', header = 0)
genre = pd.read_csv('genre_movie.csv', header = 0)
user = pd.read_csv('user_movie.csv', header = 0)
#rename the column names to the same as movie-movie 
director.columns = movie.columns.values
genre.columns = movie.columns.values


#run file
movie_similarity_calc(movie, director, genre, user, movieID, userID, use_genre, use_director)
'''
# print(time.time() - start)
