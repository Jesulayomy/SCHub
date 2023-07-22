#!/usr/bin/python3
"""
    This module contains the person class for
    creating staffs and student
"""
from email_validator import validate_email
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import Column, String


class Person(UserMixin):
    """ The person class for creating staffs and student classes """

    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    password = Column(String(45), nullable=True)
    recovery_question = Column(String(50), nullable=True)
    recovery_answer = Column(String(50), nullable=True)

    def __setattr__(self, name, value):
        """ hashes the password to an md5 when set """

        if name == "first_name":
            if not value.isalpha():
                raise ValueError("first name must contain only letters")

        if name == "last_name":
            if not value.isalpha():
                raise ValueError("last name must contain only letters")

        if name == "email":
            try:
                validate_email(value)
            except Exception:
                raise ValueError("email address is invalid")

        if name == "password" or name == "recovery_answer":
            if name == "recovery_answer":
                value = value.lower()

            md5_hash = md5()
            md5_hash.update(value.encode("utf-8"))
            value = md5_hash.hexdigest()

        super().__setattr__(name, value)
