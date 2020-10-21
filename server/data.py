from db_engine import Engine
from models.FilmCast import FilmCast
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Person import Person
from models.User import User
from authentication.hash_generator import HashGenerator
from pathlib import Path
import csv


data_dirname = Path('final')

with open(data_dirname / 'Genres.csv') as file:
    file = csv.reader(file)
    next(file)
    Engine.execute(Genres.__table__.insert().values([line for line in file]))

# with open(data_dirname / 'Movie.csv') as file:
#     file = csv.reader(file)
#     next(file)
#     Engine.execute(Movie.__table__.insert().values([line for line in file]))

# The above and the below each produce:
# sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) too many SQL variables

# with open(data_dirname / 'Person.csv') as file:
#     file = csv.reader(file)
#     next(file)
#     Engine.execute(Person.__table__.insert().values([line for line in file]))

# This takes forever:
with open(data_dirname / 'Person.csv') as file:
    file = csv.reader(file)
    next(file)
    for line in file:
        Engine.execute(Person.__table__.insert().values(line))

# From Googling, the SQLite variable limit seems to be 999 by default.  I guess
# I can just append lines from the file to a list and insert periodically,
# before the list contains more than 999 variables.  I feel like there should
# be a nicer way of doing this, though.

password_hash = HashGenerator('COMP9900').generate()
with open(data_dirname / 'User.csv') as file:
    file = csv.reader(file)
    next(file)
    Engine.execute(User.__table__.insert().values([(line[0], line[1], line[2],
                                                    password_hash, 2001
                                                   ) for line in file
                                                  ]
                                                 )
                  )

with open(data_dirname / 'FilmCast.csv') as file:
    file = csv.reader(file)
    next(file)
    Engine.execute(FilmCast.__table__.insert().values([line for line in file]))

with open(data_dirname / 'FilmDirector.csv') as file:
    file = csv.reader(file)
    next(file)
    Engine.execute(FilmDirector.__table__.insert().values([line for line in file]))

with open(data_dirname / 'GenreOfFilm.csv') as file:
    file = csv.reader(file)
    next(file)
    Engine.execute(GenreOfFilm.__table__.insert().values([line for line in file]))

with open(data_dirname / 'MovieReview.csv') as file:
    file = csv.reader(file)
    next(file)
    Engine.execute(MovieReview.__table__.insert().values([line for line in file]))
