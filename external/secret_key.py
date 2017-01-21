import random
random = random.SystemRandom()


def get_secret_key(length=50, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                            '0123456789!@#$%^&*(-_=+)'):
    return ''.join(random.choice(allowed_chars) for i in range(length))