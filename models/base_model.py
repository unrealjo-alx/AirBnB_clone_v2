#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

import os
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage


Base = declarative_base()


class BaseModel(Base):
    """A base class for all hbnb models"""

    __abstract__ = True
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ("created_at", "updated_at"):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            if not hasattr(self, "id"):
                setattr(self, "id", str(uuid.uuid4()))
            if not hasattr(self, "created_at"):
                setattr(self, "created_at", datetime.now())
            if not hasattr(self, "updated_at"):
                setattr(self, "updated_at", datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        storage.delete(self)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        res = {}
        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                if isinstance(value, datetime):
                    res[key] = value.isoformat()
                else:
                    res[key] = value
        res["__class__"] = self.__class__.__name__
        return res
