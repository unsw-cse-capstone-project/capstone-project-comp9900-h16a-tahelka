from werkzeug.exceptions import Unauthorized

class TokenExtractor:
    def __init__(self, auth_header):
        self.auth_header = auth_header

    def extract(self):
        words = str(self.auth_header).split()
        if not len(words) == 2:
            raise Unauthorized

        if not words[0] == 'Bearer':
            raise Unauthorized

        return words[1].encode()
