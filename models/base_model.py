#!/usr/bin/python3
""" A base model representaion """
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all other classes in the models directory."""

    def __init__(self, *args, **kwargs):
        """ Instatialisation of the init method """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(
                            self,
                            key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"),
                        )
                    else:
                        setattr(self, key, value)
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
        """ returns a dictionary containing all keys/values of the instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['created_at'] = obj_dict['created_at'].isoformat()
        obj_dict['updated_at'] = obj_dict['updated_at'].isoformat()
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict
