#!/usr/bin/python3
"""Tests for the Department class"""

import inspect
import unittest
import models
import pep8 as pycodestyle

from datetime import datetime

Department = models.department.Department
module_doc = models.department.__doc__


class TestDepartmentDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of Department class
    """

    @classmethod
    def setUpClass(self):
        """SetUp for docstring tests"""

        self.department_funcs = inspect.getmembers(
            Department, inspect.isfunction
        )

    def test_pep8_conformance(self):
        """Test that models/department.py conforms to PEP8."""

        for path in [
            "models/department.py",
            "tests/test_models/test_department.py",
        ]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""

        self.assertIsNot(module_doc, None, "department.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "department.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Department class docstring"""

        self.assertIsNot(
            Department.__doc__, None, "Department class needs a docstring"
        )
        self.assertTrue(
            len(Department.__doc__) >= 1, "Department class needs a docstring"
        )

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Department methods"""

        for func in self.department_funcs:
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


class TestDepartment(unittest.TestCase):
    """Tests for the department class"""

    def test_init(self):
        """Tests the initialization of the department class"""

        tester = Department()
        self.assertEqual(type(tester.id), str)
        self.assertEqual(type(tester.created_at), datetime)

    def test_to_dict(self):
        """Tests the to_dict method of the department class"""

        tester = Department()
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
