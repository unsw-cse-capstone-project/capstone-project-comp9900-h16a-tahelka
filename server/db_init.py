from db_engine import Engine
from models.Common import Base

from models.Movie import Movie
from models.Genres import Genres
from models.GenreOfFilm import GenreOfFilm
from models.FilmDirector import FilmDirector
from models.FilmCast import FilmCast
from models.MovieReview import MovieReview
from models.User import User
from models.Person import Person
from models.WishList import Wishlist
from models.Watchlist import Watchlist
from models.BannedList import BannedList
from models.Subscription import Subscription

import os
if os.path.exists('filmfinder_tahelka.db'):
    os.remove('filmfinder_tahelka.db')

Base.metadata.create_all(Engine)
seed_data_file = 'data.py'
os.system('python3 ' + seed_data_file)
