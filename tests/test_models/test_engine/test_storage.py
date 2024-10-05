#!/usr/bin/python3
"""Tests for the engine storage"""

from models.admin import Admin
from models.course import Course
from models.department import Department
from models.student import Student
from models.teacher import Teacher

import inspect
import unittest
import models
import pep8

from models.engine import storage

Storage = storage.Storage
classes = {
    "Admin": Admin,
    "Course": Course,
    "Department": Department,
    "Student": Student,
    "Teacher": Teacher,
}


class TestStorageDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of the Storage class
    """

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""

        cls.storage_funcs = inspect.getmembers(Storage, inspect.isfunction)

    def test_pep8_conformance_storage(self):
        """Test that models/engine/storage.py conforms to PEP8."""

        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/storage.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_storage(self):
        """Test tests/test_models/test_storage.py conforms to PEP8."""

        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            [
                "tests/test_models/test_engine/\
test_storage.py"
            ]
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_storage_module_docstring(self):
        """Test for the storage.py module docstring"""
        self.assertIsNot(storage.__doc__, None, "storage.py needs a docstring")
        self.assertTrue(
            len(storage.__doc__) >= 1, "storage.py needs a docstring"
        )

    def test_storage_class_docstring(self):
        """Test for the Storage class docstring"""
        self.assertIsNot(
            Storage.__doc__, None, "Storage class needs a docstring"
        )
        self.assertTrue(
            len(Storage.__doc__) >= 1, "Storage class needs a docstring"
        )

    def test_funcs_docstrings(self):
        """Test for the presence of docstrings in Storage methods"""

        for func in self.storage_funcs:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} method needs a docstring".format(func[0]),
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]),
            )


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

        self.assertTrue(type(models.storage.all("Admin")), dict)

    def test_new(self):
        """Test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_count(self):
        """Test that count returns the total no object of all or a class"""

        storage = models.storage
        count = storage.count()
        all_count = len(storage.all())

        self.assertTrue(type(count) is int)
        self.assertEqual(count, all_count)

    def test_get_empty(self):
        """Test that get returns an object that exists in FS.__obj"""

        with self.assertRaises(TypeError):
            models.storage.get("Admin")

    def test_get(self):
        """Test that get returns an object that exists in FS.__obj"""

        storage = models.storage

        self.assertTrue(storage.get(Admin, "fake_id") is None)
