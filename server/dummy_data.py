from db_engine import Session
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person


session = Session()
session.add_all([Movie('Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 1964, 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.', 0, 0, 12, 'English'),
                 Movie('2001: A Space Odyssey', 1968, 'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.', 0, 0, 13, 'English'),
                 Movie('A Clockwork Orange', 1971, "In the future, a sadistic gang leader is imprisoned and volunteers for a conduct-aversion experiment, but it doesn't go as planned.", 0, 0, 122, 'English'),
                 Movie('Hello, Wonderful World!', 2000, 'Fake movie.', 0, 0, 12, 'English'),
                 Movie('The Best Movie', 2001, 'Description', 0, 0, 12, 'English'),
                 Movie('My Favourite Film', 1999, 'Dummy data', 0, 0, 12, 'English'),
                 Movie('Hello World!', 1987, '', 0, 0, 12, 'English'),
                 Movie('Wonderful World!', 1931, 'Hello', 0, 0, 12, 'English'),
                 Movie('This Will Match', 2010, ' ', 0, 0, 12, 'English'),
                 Movie('Movie', 2020, '.', 0, 0, 12, 'English'),
                 Genres('Comedy'),
                 Genres('Adventure'),
                 Genres('Sci-Fi'),
                 Genres('Crime'),
                 Genres('Drama'),
                 GenreOfFilm(1, 1),
                 GenreOfFilm(2, 2),
                 GenreOfFilm(2, 3),
                 GenreOfFilm(3, 4),
                 GenreOfFilm(3, 5),
                 GenreOfFilm(3, 3),
                 GenreOfFilm(4, 3),
                 GenreOfFilm(5, 5),
                 GenreOfFilm(6, 4),
                 GenreOfFilm(7, 3),
                 GenreOfFilm(8, 2),
                 GenreOfFilm(9, 1),
                 GenreOfFilm(10, 1),
                 Person('Stanley Kubrick'),
                 Person('Ian Dunkerley'),
                 Person('Nishant Chokkarapu'),
                 Person('Jatin Gupta'),
                 Person('Theruni Pethiyagoda'),
                 Person('Yash Umeshkumar Tamakuwala'),
                 FilmDirector(1, 1),
                 FilmDirector(2, 1),
                 FilmDirector(3, 1),
                 FilmDirector(4, 2),
                 FilmDirector(5, 4),
                 FilmDirector(6, 3),
                 FilmDirector(7, 2),
                 FilmDirector(7, 3),
                 FilmDirector(8, 5),
                 FilmDirector(8, 4),
                 FilmDirector(8, 2),
                 FilmDirector(9, 6),
                 FilmDirector(10, 5),
                 FilmDirector(10, 6),
                ]
               )
session.commit()
