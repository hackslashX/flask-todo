class TaskStringsClass:
    """Task strings class"""

    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._strings = {
            "create_success": {
                "en": "Task created successfully.",
            },
            "get_success": {
                "en": "Tasks retrieved successfully.",
            },
            "update_success": {
                "en": "Task updated successfully.",
            },
            "delete_success": {
                "en": "Task deleted successfully.",
            },
            "not_found": {
                "en": "Task not found.",
            },
        }

    def create_success(self):
        """Task created successfully."""
        return self._strings["create_success"][self._lang]

    def get_success(self):
        """Tasks retrieved successfully."""
        return self._strings["get_success"][self._lang]

    def update_success(self):
        """Task updated successfully."""
        return self._strings["update_success"][self._lang]

    def delete_success(self):
        """Task deleted successfully."""
        return self._strings["delete_success"][self._lang]

    def not_found(self):
        """Task not found."""
        return self._strings["not_found"][self._lang]


TaskStrings = TaskStringsClass()
