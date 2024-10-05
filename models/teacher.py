#!/usr/bin/python3
"""This module contains the teacher class"""

from models.base import Base, BaseModel
from models.person import Person
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Teacher(BaseModel, Person, Base):
    """defines the teacher class"""

    __tablename__ = "teachers"
    department_id = Column(
        String(40), ForeignKey("departments.id"), nullable=False
    )
    courses = relationship("Course", backref="teacher", cascade="all")
