#!/usr/bin/python3
""" Tests for the Person class """

import inspect
import unittest
import models
import pep8 as pycodestyle

from datetime import datetime
from models.engine import storage
Person = models.person.Person
module_doc = models.person.__doc__


class TestPersonDocs(unittest.TestCase):
    """
        Tests to check the documentation and style of Person class
    """

    @classmethod
    def setUpClass(self):
        """ SetUp for docstring tests """

        self.person_funcs = inspect.getmembers(Person, inspect.isfunction)

    def test_pep8_conformance(self):
        """ Test that models/person.py conforms to PEP8. """

        for path in ['models/person.py',
                     'tests/test_models/test_person.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """ Test for the existence of module docstring """

        self.assertIsNot(module_doc, None,
                         "person.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "person.py needs a docstring")

    def test_class_docstring(self):
        """ Test for the Person class docstring """

        self.assertIsNot(Person.__doc__, None,
                         "Person class needs a docstring")
        self.assertTrue(len(Person.__doc__) >= 1,
                        "Person class needs a docstring")

    def test_func_docstrings(self):
        """ Test for the presence of docstrings in Person methods """

        for func in self.person_funcs:
            if func[0] != 'get_id':
                with self.subTest(function=func):
                    self.assertIsNot(
                        func[1].__doc__,
                        None,
                        "{:s} method needs a docstring".format(func[0])
                    )
                    self.assertTrue(
                        len(func[1].__doc__) > 1,
                        "{:s} method needs a docstring".format(func[0])
                    )


class TestPerson(unittest.TestCase):
    """ Tests for the person class """

    def test_init(self):
        """ Tests the initialization of the person class """

        pass
