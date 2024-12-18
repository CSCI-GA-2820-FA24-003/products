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
TestProducts API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from decimal import Decimal
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Products
from .factories import ProductsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "api/products"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Products).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductsFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test product",
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

    def test_create_products(self):
        """It should Create a new Products"""
        test_products = ProductsFactory()
        logging.debug("Test Products: %s", test_products.serialize())
        response = self.client.post(BASE_URL, json=test_products.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_products = response.get_json()
        self.assertEqual(new_products["name"], test_products.name)
        self.assertEqual(new_products["description"], test_products.description)
        self.assertEqual(
            round(Decimal(new_products["price"]), 2),
            round(Decimal(test_products.price), 2),
        )

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_products = response.get_json()
        self.assertEqual(new_products["name"], test_products.name)
        self.assertEqual(new_products["description"], test_products.description)
        self.assertEqual(
            round(Decimal(new_products["price"]), 2),
            round(Decimal(test_products.price), 2),
        )

    def test_update_products(self):
        """It should Update an existing Product"""
        test_products = ProductsFactory()
        response = self.client.post(BASE_URL, json=test_products.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get new product id
        new_products = response.get_json()
        product_id = new_products["id"]
        updated_data = {
            "name": "Updated Product Name",
            "description": "Updated Product Description",
            "price": "250.00",
        }

        # Check the product is updated
        response = self.client.put(f"{BASE_URL}/{product_id}", json=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_product = response.get_json()
        self.assertEqual(updated_product["name"], updated_data["name"])
        self.assertEqual(updated_product["description"], updated_data["description"])
        self.assertEqual(
            Decimal(updated_product["price"]), Decimal(updated_data["price"])
        )

        response = self.client.get(f"{BASE_URL}/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["name"], updated_data["name"])
        self.assertEqual(updated_product["description"], updated_data["description"])
        self.assertEqual(
            round(Decimal(updated_product["price"]), 2),
            round(Decimal(updated_data["price"]), 2),
        )

    def test_update_nonexistent_product(self):
        """It should return 404 when trying to update a non-existent Product"""
        # Arrange: Define a non-existent product ID and payload
        non_existent_product_id = 9999999
        updated_data = {
            "name": "Non-existent Product",
            "description": "This product does not exist",
            "price": 100.00,
        }

        # Act: Make a PUT request to update the non-existent product
        response = self.client.put(
            f"{BASE_URL}/{non_existent_product_id}", json=updated_data
        )

        # Assert: Verify the response status code and message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_message = response.get_json()
        expected_message = f"Product with id '{non_existent_product_id}' was not found."
        self.assertIn(expected_message, error_message["message"])

    # Error-Handler tests
    # ----------------------------------------------------------
    def test_400_bad_request(self):
        """It should return 400 Bad Request"""
        # Simulate bad request by making an invalid POST request
        response = self.client.post(
            BASE_URL, json={}
        )  # Empty data simulates a bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertEqual(data["error"], "Bad Request")

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------

    def test_get_product_by_id(self):
        """It should Get a single Product by ID"""
        # Creating a product
        test_products = ProductsFactory()
        response = self.client.post(BASE_URL, json=test_products.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        product_id = data["id"]
        response = self.client.get(f"{BASE_URL}/{product_id}")

        data = response.get_json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], test_products.name)
        self.assertEqual(data["description"], test_products.description)
        # Round the price to 2 decimal places for comparison
        self.assertEqual(
            round(Decimal(data["price"]), 2),
            round(Decimal(test_products.price), 2),
        )

    def test_get_product_by_id_not_found(self):
        """It should not Get a single Product by id that's not found"""
        non_existent_product_id = 9999999
        response = self.client.get(f"{BASE_URL}/{non_existent_product_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        expected_message = f"Product with id '{non_existent_product_id}' was not found."
        self.assertIn(expected_message, data["message"])

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

        # Product not found test <niv>

    def test_delete_product_not_found(self):
        """It should return 204 when trying to delete a Product that does not exist"""
        # Use a non-existent product id
        non_existent_product_id = 9999999

        # Attempt to delete the non-existent product
        response = self.client.delete(f"{BASE_URL}/{non_existent_product_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_by_name(self):
        """It should Delete Product(s) by name"""
        # First, create a product to be deleted
        test_product = ProductsFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the new product's id
        new_product = response.get_json()
        product_id = new_product["id"]
        product_name = new_product["name"]

        # Delete the product
        response = self.client.delete(f"{BASE_URL}?name={product_name}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to retrieve the deleted product to confirm deletion
        response = self.client.get(f"{BASE_URL}/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Product not found test <niv>

    def test_delete_product_not_found_by_name(self):
        """It should return 204 when trying to delete a Product that does not exist"""
        # Use a non-existent product id
        non_existent_product_name = "Q0ix6B"

        # Attempt to delete the non-existent product
        response = self.client.delete(f"{BASE_URL}?name={non_existent_product_name}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_product_list(self):
        """It should Get a list of Products with optional filters"""
        # Create 5 products for testing
        self._create_products(5)

        # Test retrieving all products
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

        # Test filtering by product_name
        response = self.client.get(f"{BASE_URL}?name=example")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        # Adjust expectations based on test data; example product count is just illustrative
        self.assertTrue(all("example" in product["name"].lower() for product in data))

        # Test filtering by price range
        response = self.client.get(f"{BASE_URL}?min_price=10&max_price=100")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(10 <= float(product["price"]) <= 100 for product in data))

    # ----------------------------------------------------------
    # TEST APPLY A DISCOUNT
    # ----------------------------------------------------------
    def test_apply_discount(self):
        """Test applying a discount to a product"""
        # Create a product to test
        product = Products(
            name="Test Product", description="Test Description", price=Decimal("100.00")
        )
        product.create()
        self.assertIsNotNone(product.id)

        # Apply a 20% discount
        discount_data = {"discount_percentage": "20"}  # Provide as string
        response = self.client.post(
            f"{BASE_URL}/{product.id}/discount",
            json=discount_data,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the new price
        data = response.get_json()
        expected_price = Decimal("80.00")
        self.assertEqual(Decimal(data["price"]), expected_price)

    def test_apply_discount_invalid_percentage(self):
        """Test applying an invalid discount percentage"""
        product = Products(
            name="Test Product", description="Test Description", price=Decimal("100.00")
        )
        product.create()

        # Invalid discount percentage (e.g., -10%)
        discount_data = {"discount_percentage": -10}
        response = self.client.post(
            f"{BASE_URL}/{product.id}/discount", json=discount_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_discount_product_not_found(self):
        """Test applying a discount to a non-existent product"""
        discount_data = {"discount_percentage": 20}
        response = self.client.post(f"{BASE_URL}/0/discount", json=discount_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_apply_discount_missing_percentage(self):
        """Test applying a discount without providing discount_percentage"""
        # Create a product to test
        product = Products(
            name="Test Product", description="Test Description", price=Decimal("100.00")
        )
        product.create()
        self.assertIsNotNone(product.id)

        # Make a request without 'discount_percentage'
        discount_data = {}  # Empty dict, no 'discount_percentage'
        response = self.client.post(
            f"{BASE_URL}/{product.id}/discount",
            json=discount_data,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify the error message
        data = response.get_json()
        self.assertIn("Discount percentage must be provided.", data.get("message", ""))
# Testing routes for the DevOps Products Team
