""" Model Base Class definition """

import re
from datetime import datetime

from sqlalchemy import Column, Integer, inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return "_".join([x.lower() for x in re.findall(r"[A-Z][^A-Z]*", cls.__name__)])

    def dict(self) -> dict:
        """Returns the model as a dictionary

        Returns:
            dict: The model as a dictionary
        """
        ret_dict = {}
        for c in inspect(self).mapper.column_attrs:
            ret_dict[c.key] = getattr(self, c.key)
            # Convert datetime objects to ISO format
            if isinstance(ret_dict[c.key], datetime):
                ret_dict[c.key] = ret_dict[c.key].isoformat()
        return ret_dict
