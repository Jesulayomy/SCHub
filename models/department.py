#!/usr/bin/python3
"""This module contains the department class"""

from models.base import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Department(BaseModel, Base):
    """defines the department class"""

    __tablename__ = "departments"
    name = Column(String(60), nullable=False)
    teachers = relationship("Teacher", backref="department", cascade="all")
    courses = relationship("Course", backref="department", cascade="all")

    students = relationship("Student", backref="department", cascade="all")
