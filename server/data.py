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


VARIABLE_LIMIT = 999


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
                    records.clear()
        if records:
            Engine.execute(table.__table__.insert().values(records))
    except: pass

password_hash = HashGenerator('COMP9900').generate()
records = []
try:
    with open(data_dirname / 'User.csv', encoding = 'utf-8') as file:
        file = csv.reader(file)
        next(file)
        for line in file:
            if (len(records) + 1) * 5 <= VARIABLE_LIMIT:
                records.append((line[0], line[1], line[2], password_hash, 2001))
            else:
                Engine.execute(User.__table__.insert().values(records))
                records.clear()
except: pass
if records:
    Engine.execute(User.__table__.insert().values(records))

for file, table in (('Genres.csv', Genres), ('Movie.csv', Movie),
                    ('Person.csv', Person), ('FilmCast.csv', FilmCast),
                    ('FilmDirector.csv', FilmDirector),
                    ('GenreOfFilm.csv', GenreOfFilm),
                    ('MovieReview.csv', MovieReview)
                   ):
    import_data(file, table)
