#!/usr/bin/python3
"""Module for FileStorage class."""
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import datetime
import json
import os


class FileStorage:

    """Class for storing and retrieving data"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(d, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        dict_to_obj = {}
        try:
            cls_arr = {"BaseModel": BaseModel, "Amenity": Amenity,
                       "City": City, "Place": Place,
                       "Review": Review, "State": State, "User": User}
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                dict_to_obj = json.load(file)
                for key, value in dict_to_obj.items():
                    cls_to_ins = cls_arr.get(value['__class__'])
                    obj = cls_to_ins(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass
