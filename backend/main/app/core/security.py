""" Password hashing and verification. """

from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    """Hash a password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Verify a password.

    Args:
        plain_password (str): The password to verify.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password is correct, else False.
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)
