#!/usr/bin/python3
""" A base model representaion """
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all other classes in the models directory."""

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel.

        Attributes:
        - id: str - a unique identifier (UUID) converted to a string.
        - created_at: set to the current datetime when the instance is created
        - updated_at: set to current datetime when the instance is created
        """

        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at" "updated_at"]:
                    value = datetime.fromisoformat(value)

                # Set the attribute on the object.
                else:
                    setattr(self, key, value)

        # Otherwise, create new `id` and `created_at` attributes.
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Return a string representation of the BaseModel instance."""
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """ Returns string info about this class """
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
