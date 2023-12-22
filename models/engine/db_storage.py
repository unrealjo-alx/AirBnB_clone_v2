#!/usr/bin/python3
"""
This module defines the DBStorage class,
which provides relational database storage using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    DBStorage class
    Provides relational database storage using SQLAlchemy.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage class"""

        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        database = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        if env == "test":
            Base.metadata.drop_all(self.__engine)

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{database}",
            pool_pre_ping=True,
        )

        if env == "test":
            Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """Query objects from the current database session"""
        classes = [User, State, City, Amenity, Place, Review]
        objects = {}

        if cls:
            objects = self.__session.query(cls).all()
        else:
            for cls in classes:
                objects.update({obj.id: obj for obj in self.__session.query(cls).all()})

        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )

    def close(self):
        """Close the session"""
        self.__session.remove()
