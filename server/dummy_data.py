from db_engine import Session
from models.Movie import Movie


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
                 Movie('A Movie', 2020, '.', 0, 0, 12, 'English'),
                ]
               )
session.commit()
