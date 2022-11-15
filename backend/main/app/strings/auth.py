class AuthStringsClass:
    """Strings for the auth module."""

    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._strings = {
            "incorrect_email_or_password": {
                "en": "Incorrect email or password. Please try again.",
            },
            "user_logged_in": {
                "en": "User logged in successfully.",
            },
        }

    def incorrect_email_or_password(self):
        """Incorrect email or password. Please try again."""
        return self._strings["incorrect_email_or_password"][self._lang]

    def user_logged_in(self):
        """User logged in successfully."""
        return self._strings["user_logged_in"][self._lang]


AuthStrings = AuthStringsClass()
