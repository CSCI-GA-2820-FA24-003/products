######################################################################
# Copyright 2024, Nivedita Shankaranarayanan. All Rights Reserved.
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
Product Steps
Steps file for Products.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from compare3 import expect
from behave import given  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

WAIT_TIMEOUT = 60


@given("the following products")
def step_impl(context):
    """Delete all Products and load new ones"""

    # Get a list all of the products
    rest_endpoint = f"{context.base_url}/api/products"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    expect(context.resp.status_code).equal_to(HTTP_200_OK)
    # and delete them one by one
    for product in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{product['id']}", timeout=WAIT_TIMEOUT
        )
        expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)

    # load the database with new products
    for row in context.table:
        payload = {
            "name": row["name"],
            "price": row["price"],
            "description": row["description"],
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)


@given('the product with name "{product_name}" exists')
def step_impl(context, product_name):
    """Ensure the product with the given name exists"""

    rest_endpoint = f"{context.base_url}/api/products"
    context.resp = requests.get(
        f"{rest_endpoint}?name={product_name}", timeout=WAIT_TIMEOUT
    )
    expect(context.resp.status_code).equal_to(HTTP_200_OK)

    products = context.resp.json()
    if not any(product["name"] == product_name for product in products):
        context.resp = requests.post(
            rest_endpoint,
            json={
                "name": product_name,
                "price": 10.0,
                "description": "Default description",
            },
            timeout=WAIT_TIMEOUT,
        )
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)


@given('the product with name "{product_name}" is deleted')
def step_impl(context, product_name):
    """Ensure the product with the given name is deleted"""

    rest_endpoint = f"{context.base_url}/api/products"
    context.resp = requests.get(
        f"{rest_endpoint}?name={product_name}", timeout=WAIT_TIMEOUT
    )
    expect(context.resp.status_code).equal_to(HTTP_200_OK)

    products = context.resp.json()
    for product in products:
        if product["name"] == product_name:
            product_id = product["id"]
            delete_url = f"{rest_endpoint}/{product_id}"
            context.resp = requests.delete(delete_url, timeout=WAIT_TIMEOUT)
            expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)
            break


@given('a product "{product_name}" is updated with a price of {new_price}')
def step_impl(context, product_name, new_price):
    """Ensure the product with the given name is updated"""

    rest_endpoint = f"{context.base_url}/api/products"
    context.resp = requests.get(
        f"{rest_endpoint}?name={product_name}", timeout=WAIT_TIMEOUT
    )
    expect(context.resp.status_code).equal_to(HTTP_200_OK)

    products = context.resp.json()
    for product in products:
        if product["name"] == product_name:
            product_id = product["id"]
            update_url = f"{rest_endpoint}/{product_id}"
            payload = {
                "name": product_name,
                "price": new_price,
                "description": product["description"],
            }
            context.resp = requests.put(update_url, json=payload, timeout=WAIT_TIMEOUT)
            expect(context.resp.status_code).equal_to(HTTP_200_OK)
            break
