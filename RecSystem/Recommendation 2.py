import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors



# dataset = './Dataset/final/MovieReview_original.csv'
dataset = '/Users/nishant/OneDrive - UNSW/UNSW/Terms/2020_T3/capstone-project-comp9900-h16a-tahelka/Dataset/final/MovieReview_original.csv'

def getIndex(userID, index_table):
    return index_table[index_table['userID'] == userID].index[0]

def getSimilarUsers(model, index_table, userID, matrix, neighbours=6, calc_metric='cosine', req_algorithm="brute"):
    model = model(metric=calc_metric, n_neighbors=neighbours, algorithm=req_algorithm)
    model.fit(matrix)
    index = getIndex(userID, index_table)
    distance, indicies = model.kneighbors(matrix[index], n_neighbors=neighbours)
    
    n_list = indicies[0].tolist()
    
    return n_list


# Make sure the subscibed_list is a dictinary of userID as key and value as list of userID's
def getPerdictionsOfUsers(dataset_path, subscribed_dict, subscribed_neighbours_number):

    df = pd.read_csv(dataset_path)
    df = df.drop('review', axis=1)

    pivot_table = pd.pivot_table(df, values='rating', columns=['movieID'], index='userID', fill_value=0)
    pivot_table = pivot_table.sort_index()

    index_table = pd.DataFrame(sorted(set(df['userID'])), columns=["userID"])

    movie_user_matrix = csr_matrix(pivot_table.values)

    final_df = pd.DataFrame(columns=pivot_table.columns)

    for userID in list(index_table['userID']):
        neighbours = getSimilarUsers(NearestNeighbors, index_table, userID, movie_user_matrix)
        neighbours_df = pivot_table.take(neighbours)

        if userID in subscribed_dict.keys():
            subscribed_list = subscribed_dict[userID]
        else:
            subscribed_list = []

        for subscriberID in subscribed_list:
            subcribed_neighbours = getSimilarUsers(NearestNeighbors, index_table, subscriberID, movie_user_matrix,
                                                   neighbours=subscribed_neighbours_number)
            subcribed_neighbours_df = pivot_table.take(subcribed_neighbours)

            neighbours_df = pd.concat([neighbours_df, subcribed_neighbours_df])

        neighbours_df = neighbours_df.drop([userID])
        user_df = neighbours_df.mean(axis=0).to_frame().rename(columns={0: userID}).transpose()

        final_df = pd.concat([final_df, user_df])
        final_df.index.name = 'userID'

    return final_df


sub_dict = {2177.0:[8619.0, 17474.0], 8619.0:[156183.0]}

df = getPerdictionsOfUsers(dataset, sub_dict, 2)
print(df)