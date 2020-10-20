import re
from werkzeug.exceptions import BadRequest


def cleanString(stringVar: str):
    return stringVar.strip()


def isValidEmail(email: str):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not (re.search(email_regex, email)):
        raise BadRequest

def validate_rating(rating):
    if type(rating) is not str\
    or not re.fullmatch('\.[05]0?|[0-4](\.[05]?)?|5(\.0?)?|0[0-5]\.?|00[0-5]',
                        rating
                       ):
        raise BadRequest

def validate_review(review):
    if type(review) is not str or len(review) > 1_000:
        raise BadRequest
