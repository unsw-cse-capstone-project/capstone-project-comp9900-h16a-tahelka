#COMP9900 T3 2020 - Team Tahelka 
#2.99 seconds (with 2/100 users with subscribers)

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import time
from db_engine import Session
from models.MovieReview import MovieReview
from models.Subscription import Subscription
from sqlalchemy import func


def getIndex(userID, index_table):
    return index_table[index_table['userID'] == userID].index[0]

def getSimilarUsers(model, index_table, userID, matrix, neighbours=5, calc_metric='cosine', req_algorithm="brute"):
    model = model(metric=calc_metric, n_neighbors=neighbours, algorithm=req_algorithm)
    model.fit(matrix)
    index = getIndex(userID, index_table)
    distance, indicies = model.kneighbors(matrix[index], n_neighbors=neighbours) #row from matrix corresponding to the user 
                                                                                 #finds the row index of the closest neighbours
    
    n_list = indicies[0].tolist() 
    return n_list

# Make sure the subscibed_list is a dictinary of userID as key and value as list of userID's
def getPerdictionsOfUsers(df, subscribed_dict):
    df = df.drop('review', axis=1)

    pivot_table = pd.pivot_table(df, values='rating', columns=['movieID'], index='userID', fill_value=0)
    pivot_table = pivot_table.sort_index()

    index_table = pd.DataFrame(sorted(set(df['userID'])), columns=["userID"])

    movie_user_matrix = csr_matrix(pivot_table.values)

    final_df = pd.DataFrame(columns=pivot_table.columns)

    for userID in list(index_table['userID']):
        neighbours = getSimilarUsers(NearestNeighbors, index_table, userID, movie_user_matrix)
        neighbours_df = pivot_table.take(neighbours)

        if userID in subscribed_dict.keys(): #if the user has subscribed to >0 people
            subscribed_list = subscribed_dict[userID]
        else:
            subscribed_list = []

        for subscriberID in subscribed_list:
            subcribed_neighbours = getSimilarUsers(NearestNeighbors, index_table, subscriberID, movie_user_matrix,
                                                   neighbours=2)
            subcribed_neighbours_df = pivot_table.take(subcribed_neighbours)

            neighbours_df = pd.concat([neighbours_df, subcribed_neighbours_df])

        neighbours_df = neighbours_df.drop([userID]) #drop the user themselves if they are the closest neighbour to someone they subscribed to
        user_df = neighbours_df.mean(axis=0).to_frame().rename(columns={0: userID}).transpose()

        final_df = pd.concat([final_df, user_df])
        final_df.index.name = 'userID'

    #reset positions with original rating values to -1 so users will not see movie they have seen in the recommended movies section
    final_df[pivot_table > 0.0] = -1

    #reorganise column names 
    colNames = [float(movie) for movie in movie_movie.columns[1:]]         #get the columns names as floats excluding the first column
    final_df = final_df[colNames]                                                    #reorder the columns 
    
    #save file 
    final_df.to_csv('user_movie.csv',index=True)                        # save to file
    return 0



#---------------------------
#import dataset ----------- CHANGE TO DRAW FROM DATABASE ------------------------------
# dataset = pd.read_csv('MovieReview.csv', header = 0)  
session = Session()
dataset = pd.read_sql('movieReviews', session.bind)
movie_movie = pd.read_csv('movie_movie.csv', header = 0)               #load the movie-movie file

#get the user: subscribed to users list dicionary
# sub_dict = {2177.0:[8619.0, 17474.0], 8619.0:[156183.0]}
sub_dict = {userID: list(map(int, subscribedUserIDs.split(',')))
                for userID, subscribedUserIDs
                    in session.query(Subscription.userID,
                                     func.group_concat(Subscription.subscribedUserID)
                                    ).group_by(Subscription.userID)
           }

#run file
start = time.time()
getPerdictionsOfUsers(dataset, sub_dict)
print(time.time() - start)









