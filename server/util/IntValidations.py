from werkzeug.exceptions import BadRequest

def is_valid_integer(number):
    try:
        numb = int(number)
        if numb < 0 :
            raise BadRequest
    except:
        raise BadRequest
    