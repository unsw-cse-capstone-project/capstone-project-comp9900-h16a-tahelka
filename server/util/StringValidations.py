import re
from werkzeug.exceptions import BadRequest


def cleanString(stringVar: str):
    return stringVar.strip()


def isValidEmail(email: str):

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if not (re.search(email_regex, email)):
        raise BadRequest

def validate_search_keywords(keywords):
    if type(keywords) is not str or len(keywords) > 250:
        raise BadRequest
    return ' '.join(word for word in keywords.split())

def validate_rating(rating):
    if type(rating) is not str\
    or not re.fullmatch('\.[05]0?|[0-4](\.[05]?)?|5(\.0?)?|0[0-5]\.?|00[0-5]',
                        # We allow all possible representations (up
                        # to three characters in length) of a rating
                        # from 0 to 5 that is a multiple of 0.5.
                        rating
                       ):
        raise BadRequest

def validate_review(review):
    if type(review) is not str or len(review) > 1_000:
        raise BadRequest
