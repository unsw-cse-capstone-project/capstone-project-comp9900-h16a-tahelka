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


data_dirname = Path('final')

records = []

with open(data_dirname / 'Genres.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        if (len(records) + 1) * degree <= VARIABLE_LIMIT:
            records.append(line)
        else:
            Engine.execute(Genres.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(Genres.__table__.insert().values(records))
    records.clear()

with open(data_dirname / 'Movie.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        if (len(records) + 1) * degree <= VARIABLE_LIMIT:
            records.append(line)
        else:
            Engine.execute(Movie.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(Movie.__table__.insert().values(records))
    records.clear()

with open(data_dirname / 'Person.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        try:
            if (len(records) + 1) * degree <= VARIABLE_LIMIT:
                records.append(line)
            else:
                Engine.execute(Person.__table__.insert().values(records))
                records.clear()
        except:
            continue
if records:
    Engine.execute(Person.__table__.insert().values(records))
    records.clear()

password_hash = HashGenerator('COMP9900').generate()
with open(data_dirname / 'User.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    next(file)
    for line in file:
        if (len(records) + 1) * 5 <= VARIABLE_LIMIT:
            records.append((line[0], line[1], line[2], password_hash, 2001))
        else:
            Engine.execute(User.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(User.__table__.insert().values(records))
    records.clear()

with open(data_dirname / 'FilmCast.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        if (len(records) + 1) * degree <= VARIABLE_LIMIT:
            records.append(line)
        else:
            Engine.execute(FilmCast.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(FilmCast.__table__.insert().values(records))
    records.clear()

with open(data_dirname / 'FilmDirector.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        if (len(records) + 1) * degree <= VARIABLE_LIMIT:
            records.append(line)
        else:
            Engine.execute(FilmDirector.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(FilmDirector.__table__.insert().values(records))
    records.clear()

with open(data_dirname / 'GenreOfFilm.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        if (len(records) + 1) * degree <= VARIABLE_LIMIT:
            records.append(line)
        else:
            Engine.execute(GenreOfFilm.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(GenreOfFilm.__table__.insert().values(records))
    records.clear()

with open(data_dirname / 'MovieReview.csv', encoding='utf-8') as file:
    file = csv.reader(file)
    degree = len(next(file))
    for line in file:
        if (len(records) + 1) * degree <= VARIABLE_LIMIT:
            records.append(line)
        else:
            Engine.execute(MovieReview.__table__.insert().values(records))
            records.clear()
if records:
    Engine.execute(MovieReview.__table__.insert().values(records))
