# Products service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

The Products service represents the store items that customers can buy. It provides a RESTful API for creating, retrieving, updating, and deleting products in a store's catalog. The service is built with Flask and uses PostgreSQL as the database to store product information.

### How to Deploy 

##### Steps to Deploy:
 Use the provided `Makefile` commands to streamline the setup.
   ```bash
   make cluster
   make build
   make push 
   make deploy
   ```


   Verify that all pods are running successfully:
   ```bash
   kubectl get pods
   ```
   **Expected output**:
   ```plaintext
   NAME                        READY   STATUS    RESTARTS        AGE
   postgres-0                  1/1     Running   0               4m11s
   products-xxxxxx             1/1     Running   2 (3m47s ago)   4m11s
   products-xxxxxx             1/1     Running   2 (3m47s ago)   4m11s
   ```



### Running the API Documentation

After starting the application (locally or in the cluster), you can access the API documentation via a web browser. The service provides Swagger API documentation.

#### Steps to Access API Docs:

1. **Start the application**:
   ```bash
   make run
   ```

2. **Visit the Swagger Docs**:
   Open your browser and navigate to:
   ```plaintext
   http://<your-server-url>/apidocs
   ```
   e.g., `http://127.0.0.1:8080/apidocs` for local development.


### How to Run It


#### 1. Using Remote Development Container (Recommended)

 **VS Code with Docker Plugin**: Use Visual Studio Code along with the Docker extension. The development environment can be set up by pulling the appropriate image via the scripts located in the `.devcontainer` folder.  
 **Run the Flask development server**:  
 Start the server using Flask's built-in development server:

   ```bash
   make run
   ```




## Database Schema

The table structure for storing product information is defined as follows:

| Column      | Data Type    | Description                                             |
|-------------|--------------|---------------------------------------------------------|
| `id`        | Integer      | Unique identifier for each product.                     |
| `name`      | String(63)   | The name of the product, up to 63 characters.           |
| `description`| String(256) | A short description of the product, up to 256 characters.|
| `price`     | Numeric(10,2)| Price of the product, allowing up to 10 digits with 2 decimal places. |

## API Endpoints

1. [List All Products](#1-list-all-products)
2. [Retrieve a Product](#2-retrieve-a-product)
   - [Retrieve by ID](#21-get-productsid)
   - [Retrieve by Name](#22-get-productsnameproducts_name)
3. [Create a New Product](#3-create-a-new-product)
4. [Update a Product](#4-update-a-product)
5. [Delete a Product by ID](#5-delete-a-product-by-id)
6. [Action route](#6-action-route)
   - [apply discount](#post-productsproduct_iddiscount)
7. [Query route](#7-query-route)
   - [delete by name](#71-delete-productsnameproduct_name)
   - [filter product with price or name](#72-get-nameproduct_namemin_pricevaluemax_pricevalue)

### 1. **List All Products**

#### **GET `/products`**

Retrieve a list of all available products.

#### Request

  **Method:** `GET`  
  **URL:** `/products`

#### Response

  **Status:** `200 OK`  
  **Body:**

```json
[
    {
        "description": "Updated description",
        "id": 88,
        "name": "pants",
        "price": "15.99"
    },
    {
        "description": "Updated Product Description",
        "id": 85,
        "name": "shoes",
        "price": "250.00"
    }
]
```

### 2. **Retrieve a Product**

#### 2.1 **GET `/products/id`**

Retrieve a specific product by its ID.

#### Request

  **Method:** `GET`  
  **URL:** `/products/<int:id>`

#### Response

  **Status:** `200 OK` (if the product is found)  
  **Body (if found):**

```json
{
    "description": "Description of Pants",
    "id": 87,
    "name": "Pants",
    "price": "9.99"
}
```

  **Status:** `404 Not Found` (if the product is not found)

#### 2.2 **GET `/products/name/products_name`**

Retrieve one or more products that match a specific name.

#### Request

 **Method:** `GET`  
 **URL:** `/products/name/<string:products_name>`

#### Response

 **Status:** `200 OK`  
 **Body:**

```json
[
    {
        "description": "Description of pants",
        "id": 88,
        "name": "pants",
        "price": "15.99"
    }
]
```

 **Status:** `404 Not Found` (if no products are found)

### 3. **Create a New Product**

#### **POST /products**

Create a new product by providing the required product details.

#### Request

 **Method:** `POST`  
 **URL:** `/products`  
 **Body:**

```json
{
    "description": "Description of pants",
    "name": "pants",
    "price": "9.99"
}
```

#### Response  

**Status:** `201 Created`  
**Body:**

```json
{
    "description": "Description of pants",
    "id": 88,
    "name": "pants",
    "price": "9.99"
}
```

### 4. **Update a Product**

#### **PUT `/products/id`**

Update an existing product by providing the updated product details.

#### Request

 **Method:** `PUT`  
 **URL:** `/products/<int:id>`  
 **Body:**

```json
{
  "name": "pants",
  "description": "Updated description",
  "price": 15.99
}
```

#### Response

  **Status:** `200 OK`  
  **Body:**

```json
{
    "description": "Updated description",
    "id": 88,
    "name": "pants",
    "price": "15.99"
}
```

### 5. **Delete a Product by ID**  

#### **DELETE `/products/id`**

Delete a specific product by its ID.

#### Request

  **Method:** `DELETE`  
  **URL:** `/products/<int:id>`

#### Response

 **Status:** `204 NO_CONTENT` (if deleted successfully)  
 **Status:** `204 NO_CONTENT` (if the product is not found)



### 6. **Action route** 
#### POST `/products/{product_id}/discount`


#### **Request**

**Method:** `POST`  
**URL:** `/products/{product_id}/discount`  


#### **Response**

**Status:** `200 OK` (Successfully applied discount)  

 **Status:** `400 BAD_REQUEST` (Invalid discount percentage)  
 **Status:** `404 NOT_FOUND` (Product not found)  

### 7 **Query route**

#### **7.1 DELETE `/products?name=<product_name>`**

Delete one or more products that match the specified name.

#### Request

  **Method:** `DELETE`  
  **URL:** `/products?name=<product_name>`  
  **Query Parameter:**  
  - `name` *(required)*: The name of the product(s) to delete.

#### Response

- **Status:** `204 NO_CONTENT` (if deleted successfully)  
- **Status:** `204 NO_CONTENT` (if no products are found with the specified name)

#### **7.2 GET `name=<product_name>&min_price=<value>&max_price=<value>`**
  **Query Parameter:**  
   `name` : Filter products that contain the specified name.
   `min_price` : Filter products with a price greater than or equal to the specified value.
.
   `max_price` : Filter products with a price less than or equal to the specified value.
#### Response

  **Status:** `200 OK` 



## Test Coverage

**Required Test Coverage:** 95%  
**Total Coverage (as of 16/10/2024):** 95.91%

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
Temporary change for ZenHub PR
