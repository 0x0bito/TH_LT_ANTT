from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password_secure(password):
    return ph.hash(password)


def verify_password(hashed, password):
    try:
        return ph.verify(hashed, password)
    except Exception:
        return False
