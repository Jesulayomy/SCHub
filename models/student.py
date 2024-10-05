#!/usr/bin/python3
"""This module contains the student class"""

from models.base import Base, BaseModel
from models.person import Person
from sqlalchemy import Column, String, Integer, ForeignKey


class Student(BaseModel, Person, Base):
    """defines the student class"""

    __tablename__ = "students"
    age = Column(Integer, nullable=False)
    start_level = Column(Integer, nullable=False)
    current_level = Column(Integer, nullable=False)
    matric_no = Column(String(20), nullable=False)
    department_id = Column(
        String(40), ForeignKey("departments.id"), nullable=False
    )
