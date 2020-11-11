import pandas as pd 
import numpy as np 

def movie_similarity_calc(movie, director, genre, user, movieID, userID, use_genre, use_director, use_movie = 5, use_user = 1):
    #retrieve the rows and concatenate
    movie_row = movie[movie.movieID == movieID]               
    dir_row = director[director.movieID == movieID]
    genre_row = genre[genre.movieID == movieID]
    user_row = user[user.userID == userID]
    totalMovies = len(movie_row.columns) -1

    #existing user
    if len(user_row) == 1:
        final = pd.concat([movie_row, dir_row, genre_row, user_row])
        #delete user_id column
        final = final.drop(columns='userID')
        #create weight matrix
        weights = (np.matrix([[use_movie,use_director,use_genre,use_user]]*totalMovies)).T
        #calculation
        final = final.set_index('movieID')
        final = final*weights
    #new user till scheduler is run
    else:
        final = pd.concat([movie_row, dir_row, genre_row])
        #create weight matrix
        weights = (np.matrix([[use_movie,use_director,use_genre]]*totalMovies)).T
        #calculation
        final = final.set_index('movieID')
        final = final*weights


    sim_score = pd.DataFrame(final.sum(0))                       #sum down each column
    sim_score = sim_score.sort_values(by = 0, ascending = False) #sort
    limit = 12
    topMovies = [int(movie) for movie in list(sim_score.head(limit).index[2:])]
    return topMovies 



    