class UserStringsClass:
    """Strings for the user module."""

    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._strings = {
            "user_already_exists": {
                "en": "User already exists. Please login instead.",
            },
            "user_created": {
                "en": "User created successfully.",
            },
            "get_success": {
                "en": "User retrieved successfully.",
            },
            "update_success": {
                "en": "User updated successfully.",
            },
        }

    def user_already_exists(self):
        """User already exists. Please login instead."""
        return self._strings["user_already_exists"][self._lang]

    def user_created(self):
        """User created successfully."""
        return self._strings["user_created"][self._lang]

    def get_success(self):
        """User retrieved successfully."""
        return self._strings["get_success"][self._lang]

    def update_success(self):
        """User updated successfully."""
        return self._strings["update_success"][self._lang]


UserStrings = UserStringsClass()
