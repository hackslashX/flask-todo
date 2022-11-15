""" Base Schema """

from marshmallow import RAISE, Schema, post_dump


class BaseSchema(Schema):
    """Base schema"""

    class Meta:
        """Meta"""

        unknown = RAISE

    SKIP_VALUES = [None]

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        """Remove skip values from the data

        Args:
            data (dict): The data to remove the skip values from.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The data without the skip values.
        """
        return {
            key: value for key, value in data.items() if value not in self.SKIP_VALUES
        }
