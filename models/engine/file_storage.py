#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Represent an abstracted storage engine."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects."""
        if cls is not None:
            cls_dict = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                odict = json.load(f)
                self.__objects = {
                    k: globals()[v["__class__"]](**v) for k, v in odict.items()
                }
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)

    def close(self):
        """Call the reload method."""
        self.reload()
