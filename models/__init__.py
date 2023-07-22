#!/usr/bin/python3
""" starts the session """
from models.engine.storage import Storage


storage = Storage()
storage.reload()
