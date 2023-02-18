import random
import secrets
import string


class RngProvider():
    def generate_pseudo_random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))

    def generate_cryptographic_pseudo_random_string(self, length):
        return secrets.token_urlsafe(length)[:length]
