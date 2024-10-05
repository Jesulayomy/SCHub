#!/usr/bin/python3
"""Tests for the Student class"""

import inspect
import unittest
import models
import pep8 as pycodestyle

from datetime import datetime

Student = models.student.Student
module_doc = models.student.__doc__


class TestStudentDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of Student class
    """

    @classmethod
    def setUpClass(self):
        """SetUp for docstring tests"""

        self.student_funcs = inspect.getmembers(Student, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/student.py conforms to PEP8."""

        for path in ["models/student.py", "tests/test_models/test_student.py"]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""

        self.assertIsNot(module_doc, None, "student.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "student.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Student class docstring"""

        self.assertIsNot(
            Student.__doc__, None, "Student class needs a docstring"
        )
        self.assertTrue(
            len(Student.__doc__) >= 1, "Student class needs a docstring"
        )

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Student methods"""

        for func in self.student_funcs:
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


class TestStudent(unittest.TestCase):
    """Tests for the student class"""

    def test_init(self):
        """Tests the initialization of the student class"""

        tester = Student()
        self.assertEqual(type(tester.id), str)
        self.assertEqual(type(tester.created_at), datetime)

    def test_to_dict(self):
        """Tests the to_dict method of the student class"""

        tester = Student()
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
