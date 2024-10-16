######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Pet Model
"""

# pylint: disable=duplicate-code
import os
import logging
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Products, DataValidationError, db
from .factories import ProductsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P R O D U C T S   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProducts(TestCase):
    """Test Cases for Products Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Products).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_products(self):
        """It should create a Products"""
        products = ProductsFactory()
        products.create()
        self.assertIsNotNone(products.id)
        found = Products.all()
        self.assertEqual(len(found), 1)
        data = Products.find(products.id)
        self.assertEqual(data.name, products.name)
        self.assertEqual(data.description, products.description)
        # Convert the price to Decimal and compare niv
        self.assertEqual(data.price, Decimal(products.price))

    def test_create_products_with_invalid_name(self):
        """It should raise DataValidationError when the name exceeds the maximum length"""
        products = ProductsFactory()
        products.name = (
            "x" * 100
        )  # Create a product is not valid, which name exceeds the 63-character limit
        with self.assertRaises(DataValidationError) as context:
            products.create()
        self.assertIn("value too long", str(context.exception))

    def test_update_products_with_invalid_data(self):
        """It should raise DataValidationError when updating with invalid data"""
        # Create a valid product first
        products = ProductsFactory()
        products.create()
        self.assertIsNotNone(products.id)

        # Modify the product with invalid data
        products.name = "x" * 100  # Exceeds the 63-character limit

        with self.assertRaises(DataValidationError) as context:
            products.update()
        self.assertIn("value too long", str(context.exception))

    def test_delete_products_with_exception_handling(self):
        """It should handle exceptions during delete properly"""
        products = ProductsFactory()
        products.create()
        self.assertIsNotNone(products.id)

        # Mock db.session.commit() to raise an exception during delete
        with patch(
            "service.models.db.session.commit",
            side_effect=Exception("Mock commit exception during delete"),
        ), patch("service.models.db.session.rollback") as mock_rollback, patch(
            "service.models.logger.error"
        ) as mock_logger_error:
            with self.assertRaises(DataValidationError) as context:
                products.delete()
            # Verify that rollback was called
            mock_rollback.assert_called_once()
            # Verify that logger.error was called with the correct message
            mock_logger_error.assert_called_once_with(
                "Error deleting record: %s", products
            )
            # Verify that the exception message contains the original exception message
            self.assertIn("Mock commit exception during delete", str(context.exception))

    def test_deserialize_with_invalid_type(self):
        """It should raise DataValidationError when data is not a dictionary"""
        products = Products()
        # Pass None as data
        with self.assertRaises(DataValidationError) as context:
            products.deserialize(None)
        self.assertIn(
            "Invalid Products: body of request contained bad or no data",
            str(context.exception),
        )

        # Pass an integer as data
        with self.assertRaises(DataValidationError) as context:
            products.deserialize(123)
        self.assertIn(
            "Invalid Products: body of request contained bad or no data",
            str(context.exception),
        )
