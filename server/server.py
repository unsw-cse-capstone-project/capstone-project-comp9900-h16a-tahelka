from flask import Flask
from flask_cors import CORS
from apis import blueprint
from apis import api
import pandas as pd
from os import path
from RecSystem.user_movie import readWriteComputeUserPred
import threading, time

app = Flask(__name__)
CORS(app)

app.register_blueprint(blueprint)
app.config.from_pyfile('configuration.py')

# Register app error handlers
@app.errorhandler(404)
def handle_not_found(error):
    status_code = 404

    response = {"message": "Resource not found."}
    return response, status_code

@app.errorhandler(Exception)
def handle_internal_server_error(error):
    status_code = 500

    print(error.__class__)
    print(error)

    response = {"message": "Internal server error."}
    return response, status_code

def load_df():
    recoDir = 'RecSystem'
    dataDir = 'RecoData'
    location = path.join(recoDir, dataDir)
    app.dirDf = pd.read_csv(path.join(location, 'director_movie.csv'))
    app.genDf = pd.read_csv(path.join(location,'genre_movie.csv'))
    app.userDf = pd.read_csv(path.join(location,'user_movie.csv'))
    app.movieDf = pd.read_csv(path.join(location,'movie_movie.csv'))

dataLoaderThread = threading.Thread(target=load_df, name='dataLoaderThread')
dataLoaderThread.daemon = True
dataLoaderThread.start()


def recompute_user_pred():
    while True:
        print('recomputing userPred: ', time.ctime())
        userMovieDf = readWriteComputeUserPred()
        if userMovieDf:
            app.userDf = userMovieDf
        time.sleep(300)


userPredCalcThread = threading.Thread(target=recompute_user_pred, name='userPredCalcThread')
userPredCalcThread.daemon = True
userPredCalcThread.start()

# Run
app.run(debug = True)
