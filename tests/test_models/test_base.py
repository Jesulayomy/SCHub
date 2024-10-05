#!/usr/bin/python3
"""Tests for the Base class"""

import inspect
import unittest
import models
import pep8 as pycodestyle

from datetime import datetime

BaseModel = models.base.BaseModel
module_doc = models.base.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of BaseModel class
    """

    @classmethod
    def setUpClass(self):
        """SetUp for docstring tests"""

        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base.py conforms to PEP8."""

        for path in ["models/base.py", "tests/test_models/test_base.py"]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""

        self.assertIsNot(module_doc, None, "base.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "base.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""

        self.assertIsNot(
            BaseModel.__doc__, None, "BaseModel class needs a docstring"
        )
        self.assertTrue(
            len(BaseModel.__doc__) >= 1, "BaseModel class needs a docstring"
        )

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""

        for func in self.base_funcs:
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


class TestBaseModel(unittest.TestCase):
    """Tests for the base class"""

    def test_init(self):
        """Tests the initialization of the base class"""

        tester = BaseModel()
        self.assertEqual(type(tester.id), str)
        self.assertEqual(type(tester.created_at), datetime)

    def test_to_dict(self):
        """Test the to_dict method of the basemodel class"""

        tester = BaseModel()
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
