#!/usr/bin/python3
"""Tests for the Teacher class"""

import inspect
import unittest
import models
import pep8 as pycodestyle

from datetime import datetime

Teacher = models.teacher.Teacher
module_doc = models.teacher.__doc__


class TestTeacherDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of Teacher class
    """

    @classmethod
    def setUpClass(self):
        """SetUp for docstring tests"""

        self.teacher_funcs = inspect.getmembers(Teacher, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/teacher.py conforms to PEP8."""

        for path in ["models/teacher.py", "tests/test_models/test_teacher.py"]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""

        self.assertIsNot(module_doc, None, "teacher.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "teacher.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Teacher class docstring"""

        self.assertIsNot(
            Teacher.__doc__, None, "Teacher class needs a docstring"
        )
        self.assertTrue(
            len(Teacher.__doc__) >= 1, "Teacher class needs a docstring"
        )

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Teacher methods"""

        for func in self.teacher_funcs:
            if func[0] != "get_id":
                with self.subTest(function=func):
                    self.assertIsNot(
                        func[1].__doc__,
                        None,
                        "{:s} method needs a docstring".format(func[0]),
                    )
                    self.assertTrue(
                        len(func[1].__doc__) > 1,
                        "{:s} method needs a docstring".format(func[0]),
                    )


class TestTeacher(unittest.TestCase):
    """Tests for the teacher class"""

    def test_init(self):
        """Tests the initialization of the teacher class"""

        tester = Teacher()
        self.assertEqual(type(tester.id), str)
        self.assertEqual(type(tester.created_at), datetime)

    def test_to_dict(self):
        """Tests the to_dict method of the teacher class"""

        tester = Teacher()
        self.assertEqual(type(tester.to_dict()), dict)
        sample_dict = tester.to_dict()
        self.assertIn(
            "id", sample_dict, "Object.to_dict() returns no 'id' attribute"
        )
        self.assertIn(
            "created_at",
            sample_dict,
            "Object.to_dict() returns no 'created_at' attribute",
        )
