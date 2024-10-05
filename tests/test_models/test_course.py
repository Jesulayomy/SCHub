#!/usr/bin/python3
"""Tests for the Admin class"""

import inspect
import unittest
import models
import pep8 as pycodestyle

from datetime import datetime

Admin = models.admin.Admin
module_doc = models.admin.__doc__


class TestAdminDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of Admin class
    """

    @classmethod
    def setUpClass(self):
        """SetUp for docstring tests"""

        self.admin_funcs = inspect.getmembers(Admin, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/admin.py conforms to PEP8."""

        for path in ["models/admin.py", "tests/test_models/test_admin.py"]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""

        self.assertIsNot(module_doc, None, "admin.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "admin.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Admin class docstring"""

        self.assertIsNot(Admin.__doc__, None, "Admin class needs a docstring")
        self.assertTrue(
            len(Admin.__doc__) >= 1, "Admin class needs a docstring"
        )

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Admin methods"""

        for func in self.admin_funcs:
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


class TestAdmin(unittest.TestCase):
    """Tests for the admin class"""

    def test_init(self):
        """Tests the initialization of the admin class"""

        tester = Admin()
        self.assertEqual(type(tester.id), str)
        self.assertEqual(type(tester.created_at), datetime)

    def test_to_dict(self):
        """Tests the to_dict method of the admin class"""

        tester = Admin()
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
