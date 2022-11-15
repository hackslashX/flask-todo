class GeneralStringsClass:
    """General strings"""

    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._strings = {
            "invalid_request_data": {
                "en": "Request data is invalid. Please check the data and try again.",
            },
            "invalid_response_data": {
                "en": "Response data is invalid. Please contact administrator.",
            },
        }

    def invalid_request_data(self):
        """Request data is invalid. Please check the data and try again."""
        return self._strings["invalid_request_data"][self._lang]

    def invalid_response_data(self):
        """Response data is invalid. Please contact administrator."""
        return self._strings["invalid_response_data"][self._lang]


GeneralStrings = GeneralStringsClass()
