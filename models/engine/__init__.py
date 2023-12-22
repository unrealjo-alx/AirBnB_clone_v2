#!/usr/bin/python3
"""
This module instantiates an object of the appropriate storage class.
"""

import os
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage_type = os.getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
