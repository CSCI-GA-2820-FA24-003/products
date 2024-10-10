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
Products Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Products
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Products
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Create a Product
    This endpoint will create a Products based the data in the body that is posted
    """
    app.logger.info("Request to Create a Product")
    check_content_type("application/json")

    products = Products()
    products.deserialize(request.get_json())

    # Save the new Products to the database
    products.create()
    message = products.serialize()
    location_url = url_for("get_products", products_id=products.id, _external=True)

    app.logger.info("Products with new ID: %d created.", products.id)

    # Return the location of the new Products
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


#############################################
# Logs error messages before aborting
#############################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)


##########nivy###############
######################################################################
# RETRIEVE A PRODUCT
######################################################################
@app.route("/products/<int:products_id>", methods=["GET"])
def get_products(products_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its ID
    """
    app.logger.info(f"Request to retrieve Product with id: {products_id}")

    # Find the product by its ID
    product = Products.find(products_id)

    # If product not found, abort with a 404 error
    if not product:
        app.logger.error(f"Product with id: {products_id} not found.")
        abort(status.HTTP_404_NOT_FOUND, f"Product with id {products_id} not found.")

    app.logger.info(f"Returning product: {product.name}")

    return jsonify(product.serialize()), status.HTTP_200_OK
