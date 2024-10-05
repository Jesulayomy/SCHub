#!/usr/bin/python3
"""This module contains the course class"""

from models.base import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey


class Course(BaseModel, Base):
    """defines the course class"""

    __tablename__ = "courses"
    name = Column(String(60), nullable=False)
    level = Column(Integer, nullable=False)
    department_id = Column(
        String(50), ForeignKey("departments.id"), nullable=False
    )
    teacher_id = Column(String(50), ForeignKey("teachers.id"), nullable=False)
