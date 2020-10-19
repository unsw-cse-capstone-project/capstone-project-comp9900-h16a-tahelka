import re
from werkzeug.exceptions import BadRequest


def cleanString(stringVar: str):
    return stringVar.strip()


def isValidEmail(email: str):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not (re.search(email_regex, email)):
        raise BadRequest
