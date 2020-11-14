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


VARIABLE_LIMIT = 999  # SQLite sets a limit of 999 for the number of
# variable parameters in a single SQL statement, such as an insertion.  In
# the case of inserting a single tuple with five attributes, this counts
# as five variables, therefore, when inserting in bulk, a maximum of 199
# such tuples, i.e. 199 * 5 = 995 variables, can be inserted at once.


data_dirname = Path('dataset')


def import_data(file, table):
    try:
        with open(data_dirname / file, encoding = 'utf-8') as file:
            file = csv.reader(file)
            degree = len(next(file))
            records = []
            for line in file:
                if (len(records) + 1) * degree <= VARIABLE_LIMIT:
                    records.append(line)
                else:
                    try:
                        Engine.execute(table.__table__.insert().values(records))
                    except: pass
                    records = [line]
        Engine.execute(table.__table__.insert().values(records))
    except: pass

password_hash = HashGenerator('COMP9900').generate()
try:
    with open(data_dirname / 'User.csv', encoding = 'utf-8') as file:
        file = csv.reader(file)
        next(file)
        records = []
        for line in file:
            if (len(records) + 1) * 5 <= VARIABLE_LIMIT:
                records.append((line[0], line[1], line[2], password_hash, 2001))
            else:
                try:
                    Engine.execute(User.__table__.insert().values(records))
                except: pass
                records = [line]
    Engine.execute(User.__table__.insert().values(records))
except: pass

for file, table in ('Genres.csv', Genres), ('Movie.csv', Movie),\
                   ('Person.csv', Person), ('FilmCast.csv', FilmCast),\
                   ('FilmDirector.csv', FilmDirector),\
                   ('GenreOfFilm.csv', GenreOfFilm),\
                   ('MovieReview.csv', MovieReview):
    import_data(file, table)
