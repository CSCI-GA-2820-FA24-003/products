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
Product Service with Swagger

Paths:
------
GET / - Displays a UI for Selenium testing
GET /products - Returns a list of all products with optional filters by name and price range
GET /products/{id} - Returns the product with a given ID number
DELETE /products - Deletes products by name provided as a query parameter
POST /products - Creates a new product record in the database
PUT /products/{id} - Updates a product record in the database
DELETE /products/{id} - Deletes a product record in the database
POST /products/{id}/discount - Applies a discount to a product by ID
GET /health - Health check for the service

"""

import secrets
from decimal import Decimal
from flask import jsonify, request, abort
from flask import current_app as app  # Import Flask application
from flask_restx import Resource, fields, reqparse
from service.models import Products
from service.common import status  # HTTP Status Codes
from . import api


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """Helper function used when testing API keys"""
    return secrets.token_hex(16)


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Index page"""
    app.logger.info("Request for Root URL")
    # Integrate with Selenium UI
    # Add logic here to serve dynamic content or interact with the Selenium-based UI for testing.

    return app.send_static_file("index.html")


# Define the model for documentation and validation
create_model = api.model(
    "Product",
    {
        "name": fields.String(
            required=True, description="The name of the product, up to 63 characters"
        ),
        "description": fields.String(
            required=False,
            description="A short description of the product, up to 256 characters",
        ),
        "price": fields.Float(
            required=True,
            description="Price of the product, allowing up to 10 digits with 2 decimal places",
            min=0.01,
        ),
    },
)

product_model = api.inherit(
    "ProductModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="Unique identifier for each product"
        ),
    },
)

delete_model = api.model(
    "DeleteProductByName",
    {
        "name": fields.String(
            required=True, description="The name of the product to delete"
        )
    },
)
discount_model = api.model(
    "discount",
    {
        "discount_percentage": fields.Float(
            required=True,
            description="The discount percentage to apply (0-100)",
        )
    },
)

# Query string arguments for product filtering
product_args = reqparse.RequestParser()
product_args.add_argument(
    "name", type=str, location="args", required=False, help="Filter products by name"
)
product_args.add_argument(
    "min_price",
    type=float,
    location="args",
    required=False,
    help="Filter products with a minimum price",
)
product_args.add_argument(
    "max_price",
    type=float,
    location="args",
    required=False,
    help="Filter products with a maximum price",
)
# Query string arguments for delete product filtering
delete_product_args = reqparse.RequestParser()
delete_product_args.add_argument(
    "name",
    type=str,
    location="args",
    required=True,  # Make 'name' required for deletion
    help="Name of the product to delete",
)

######################################################################
# Authorization Decorator (skip when implementing)
######################################################################
# def token_required(func):
#     """Decorator to require a token for this endpoint"""

#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = None
#         if "X-Api-Key" in request.headers:
#             token = request.headers["X-Api-Key"]
#         if app.config.get("API_KEY") and app.config["API_KEY"] == token:
#             return func(*args, **kwargs)
#         return {"message": "Invalid or missing token"}, 401

#     return decorated


######################################################################
# PATH: /products/{id}
######################################################################
@api.route("/products/<int:product_id>")
@api.param("product_id", "The Product identifier")
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Product
    GET /products/{id} - Returns a Product with the id
    PUT /products/{id} - Update a Product with the id
    DELETE /products/{id} - Deletes a Product with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A PRODUCT
    # ------------------------------------------------------------------
    @api.doc("get_product")
    @api.response(404, "Product not found")
    @api.marshal_with(product_model)
    def get(self, product_id):
        """Retrieve a single Product"""
        app.logger.info("Request to Retrieve a product with id [%s]", product_id)
        product = Products.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PRODUCT
    # ------------------------------------------------------------------
    @api.doc("update_product", security="apikey")
    @api.response(404, "Product not found")
    @api.response(400, "The posted Product data was not valid")
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """Update a Product"""
        app.logger.info("Request to Update a product with id [%s]", product_id)
        product = Products.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )
        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PRODUCT BY ID
    # ------------------------------------------------------------------
    @api.doc("delete_product", security="apikey")
    @api.response(204, "Product deleted")
    def delete(self, product_id):
        """Delete a Product"""
        app.logger.info("Request to Delete a product with id [%s]", product_id)
        product = Products.find(product_id)
        if not product:
            app.logger.error(f"Product with id [{product_id}] not found.")
            return "", status.HTTP_204_NO_CONTENT  # Idempotent: always return 204

        product.delete()
        app.logger.info("Product with id [%s] was deleted", product_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
# PATH: /products
######################################################################
@api.route("/products", strict_slashes=False)
class ProductCollection(Resource):
    """Handles all interactions with collections of Products"""

    # ------------------------------------------------------------------
    # LIST ALL PRODUCTS
    # ------------------------------------------------------------------
    @api.doc("list_products")
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """Returns filtered or all products"""
        app.logger.info("Request for product list")

        # Retrieve query parameters
        product_name = request.args.get("name")
        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)

        # Apply filters based on query parameters
        query = Products.query
        if product_name:
            query = query.filter(Products.name.ilike(f"%{product_name}%"))
        if min_price is not None:
            query = query.filter(Products.price >= min_price)
        if max_price is not None:
            query = query.filter(Products.price <= max_price)

        products = query.all()
        results = [product.serialize() for product in products]
        app.logger.info("Returning %d products", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PRODUCT
    # ------------------------------------------------------------------
    @api.doc("create_product", security="apikey")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """Creates a Product"""
        app.logger.info("Request to Create a Product")
        product = Products()
        product.deserialize(api.payload)
        product.create()
        app.logger.info("Product with new id [%s] created!", product.id)
        location_url = api.url_for(
            ProductResource, product_id=product.id, _external=True
        )
        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

    # ------------------------------------------------------------------
    # DELETE PRODUCTS BY NAME
    # ------------------------------------------------------------------
    @api.doc("delete_products_by_name", security="apikey")
    @api.expect(delete_product_args, validate=True)
    @api.response(204, "Products deleted (idempotent)")
    @api.response(400, "Name must be specified for deletion")
    def delete(self):
        """Delete Product(s) by name"""
        args = delete_product_args.parse_args()
        name = args["name"]
        app.logger.info(f"Request to delete Product(s) with name: {name}")

        # Find products by name
        products = Products.find_by_name(name)
        if products:
            for product in products:
                product.delete()
            app.logger.info(f"Product(s) with name '{name}' deleted successfully")
        else:
            app.logger.info(f"No products found with the name '{name}'")

        # Always return 204 No Content, regardless of whether products existed
        return "", status.HTTP_204_NO_CONTENT


######################################################################
# PATH: /products/<int:product_id>/discount
######################################################################
@api.route("/products/<int:product_id>/discount", strict_slashes=False)
class DiscountResource(Resource):
    """Handles applying a discount to a product"""

    @api.doc("apply_discount")
    @api.response(404, "Product not found")
    @api.response(400, "Invalid discount percentage")
    @api.response(200, "Successfully applied discount")
    @api.expect(discount_model)
    def post(self, product_id):
        """Apply a (0-100) percentage discount  to a product's price"""
        app.logger.info(f"Request to apply discount to product with id: {product_id}")

        # Find the product by its ID
        product = Products.find(product_id)
        if not product:
            app.logger.error(f"Product with id: {product_id} not found.")
            abort(status.HTTP_404_NOT_FOUND, f"Product with id {product_id} not found.")

        # Get the discount percentage from the request body
        data = api.payload
        if not data or "discount_percentage" not in data:
            app.logger.error("Discount percentage not provided in request.")
            abort(status.HTTP_400_BAD_REQUEST, "Discount percentage must be provided.")

        try:
            # Validate discount percentage
            discount_percentage = float(data["discount_percentage"])
            if discount_percentage < 0 or discount_percentage > 100:
                raise ValueError("Discount percentage must be between 0 and 100.")
        except ValueError as e:
            app.logger.error(f"Invalid discount percentage: {e}")
            abort(status.HTTP_400_BAD_REQUEST, str(e))

        # Calculate the new price
        original_price = Decimal(str(product.price))
        discount_amount = (original_price * Decimal(discount_percentage)) / Decimal(100)
        new_price = original_price - discount_amount
        product.price = new_price.quantize(Decimal("0.01"))  # Round to 2 decimal places

        # Update the product
        product.update()
        app.logger.info(
            f"Applied {discount_percentage}% discount to product id {product_id}. New price: {product.price}"
        )

        return product.serialize(), status.HTTP_200_OK


#############################################
# Logs error messages before aborting
#############################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)


@app.route("/health")
def health():
    """Kubernetes knows that your microservice is healthy."""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK
