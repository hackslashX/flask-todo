class TagStringsClass:
    """Strings for the tag page."""

    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._strings = {
            "already_exists": {
                "en": "Tag already exists.",
            },
            "create_success": {
                "en": "Tag created successfully.",
            },
            "get_success": {
                "en": "Tags retrieved successfully.",
            },
            "update_success": {
                "en": "Tag updated successfully.",
            },
            "delete_success": {
                "en": "Tag deleted successfully.",
            },
            "not_found": {
                "en": "Tag not found.",
            },
        }

    def already_exists(self):
        """Tag already exists."""
        return self._strings["already_exists"][self._lang]

    def create_success(self):
        """Tag created successfully."""
        return self._strings["create_success"][self._lang]

    def get_success(self):
        """Tags retrieved successfully."""
        return self._strings["get_success"][self._lang]

    def update_success(self):
        """Tag updated successfully."""
        return self._strings["update_success"][self._lang]

    def delete_success(self):
        """Tag deleted successfully."""
        return self._strings["delete_success"][self._lang]

    def not_found(self):
        """Tag not found."""
        return self._strings["not_found"][self._lang]


TagStrings = TagStringsClass()
