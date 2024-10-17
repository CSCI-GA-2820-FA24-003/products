# Products service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

The Products service represents the store items that customers can buy. It provides a RESTful API for creating, retrieving, updating, and deleting products in a store's catalog. The service is built with Flask and uses PostgreSQL as the database to store product information.

### How to Run It


#### 1. Using Remote Development Container (Recommended)

 **VS Code with Docker Plugin**: Use Visual Studio Code along with the Docker extension. The development environment can be set up by pulling the appropriate image via the scripts located in the `.devcontainer` folder.  
 **Run the Flask development server**:  
 Start the server using Flask's built-in development server:

   ```bash
   flask run
   ```

#### 2. Running Locally with Flask

If you prefer to run the service locally, you need to install the required dependencies and start the application manually. Below are the main dependencies and instructions for setting it up:

##### Steps to Run Locally:

1. **Install the dependencies**:
   Ensure you have Python and pip installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file to store environment-specific variables such as database credentials. Example:

   ```bash
   FLASK_APP=service:app
   FLASK_ENV=development
   DATABASE_URL=postgresql://<username>:<password>@localhost/<dbname>
   ```

3. **Run the Flask development server**:
   Start the server using Flask's built-in development server:

   ```bash
   flask run
   ```

## How to Test It

We use standard **PyUnit** syntax for writing and running tests. To execute the tests, follow the instructions in our `Makefile`. Simply run the following command in your terminal:

```bash
make test
```

This will automatically run the tests and generate a coverage report.

## Test Coverage

**Required Test Coverage:** 95%  
**Total Coverage (as of 16/10/2024):** 95.91%


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

 **Status:** `200 OK` (if deleted successfully)  
 **Status:** `404 Not Found` (if the product is not found)

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
