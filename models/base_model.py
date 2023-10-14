#!/usr/bin/python3
""" A base model representaion """
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all other classes in the models directory."""

    def __init__(self):
        """Initialize a new BaseModel instance."""
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
        """
        Returns a dictionary representation of the instance.

        The dictionary includes all instance attributes
        'created_at' and 'updated_at' are converted to string objects

        Returns:
        - dict: A dictionary containing the instance attributes and metadata.
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()

        return obj_dict
