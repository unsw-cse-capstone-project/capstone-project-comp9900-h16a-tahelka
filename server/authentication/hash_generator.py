import bcrypt

class HashGenerator:
    def __init__(self, plaintext):
        self.plaintext = plaintext

    def generate(self):
        plaintext_bytes = self.plaintext.encode()
        return bcrypt.hashpw(plaintext_bytes, bcrypt.gensalt())
