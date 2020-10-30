import re
from werkzeug.exceptions import BadRequest
from db_engine import Session
from models.FilmDirector import FilmDirector
from models.Person import Person


def cleanString(stringVar: str):
    return stringVar.strip()


def isValidEmail(email: str):
    # type- first.last@domain.com
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not (re.search(email_regex, email)):
        raise BadRequest

def validate_search_keywords(keywords):
    if keywords is None:
        return ''
    if type(keywords) is not str or len(keywords) > 250:
        raise BadRequest
    return ' '.join(word for word in keywords.split())

def validate_director(director):
    if director is not None:
        if type(director) is not str or len(director) > 100:
            raise BadRequest
        director = Session().query(Person.name)\
                            .join(FilmDirector)\
                            .filter(Person.name.ilike(' '.join(name for name in director.split())))\
                            .distinct().one_or_none()
        if not director:
            raise BadRequest
        return director[0]

def validate_rating(rating):
    if type(rating) is not str\
    or not re.fullmatch('\.[05]0?|[0-4](\.[05]?)?|5(\.0?)?|0[0-5]\.?|00[0-5]',
                        rating
                       ):
        raise BadRequest

def validate_review(review):
    if type(review) is not str or len(review) > 1_000:
        raise BadRequest
