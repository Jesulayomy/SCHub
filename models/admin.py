#!/usr/bin/python3
"""This module contains the admin class"""

from models.base import Base, BaseModel
from models.person import Person


class Admin(BaseModel, Person, Base):
    """defines the admin class"""

    __tablename__ = "admins"
