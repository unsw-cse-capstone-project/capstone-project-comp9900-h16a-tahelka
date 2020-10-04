from db_engine import Engine
from models.Common import Base

from models.Movie import Movie
from models.Genres import Genres
from models.GenreOfFilm import GenreOfFilm
from models.FilmDirector import FilmDirector
from models.FilmCast import FilmCast
from models.MovieReview import MovieReview
from models.FilmFinder import FilmFinder
from models.Person import Person
from models.WishList import Wishlist
from models.Watchlist import Watchlist
from models.BannedList import Bannedlist
from models.Subscription import Subscription

Base.metadata.create_all(Engine)