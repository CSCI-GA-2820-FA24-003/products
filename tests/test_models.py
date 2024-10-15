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
from unittest import TestCase
from wsgi import app
from service.models import Products, DataValidationError, db
from .factories import ProductsFactory
from decimal import Decimal

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

    # Todo: Add your test cases here...
    # ----------------------------------------------------------
    # TEST DELETE
    # ----------------------------------------------------------
    def test_delete_product(self):
        """It should Delete a Product by id"""
        # First, create a product to be deleted
        test_product = ProductsFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the new product's id
        new_product = response.get_json()
        product_id = new_product["id"]

        # Delete the product
        response = self.client.delete(f"{BASE_URL}/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to retrieve the deleted product to confirm deletion
        response = self.client.get(f"{BASE_URL}/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)