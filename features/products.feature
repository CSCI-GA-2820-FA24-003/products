Feature: The product store service back-end
    As a Product Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description        | price  |
        | Laptop     | High-end laptop    | 1000.00|
        | Smartphone | Latest model       | 800.00 |
        | Chair      | Office chair       | 150.00 |
        | Table      | Wooden dining table| 300.00 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Headphones"
    And I set the "Description" to "Noise cancelling headphones"
    And I set the "Price" to "150.00"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    And the "Price" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Headphones" in the "Name" field
    And I should see "Noise cancelling headphones" in the "Description" field
    And I should see "150.00" in the "Price" field



Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    And the "Price" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Laptop" in the "Name" field
    And I should see "High-end laptop" in the "Description" field
    And I should see "1000.00" in the "Price" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    When I change "Price" to "1200.00"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "1200.00" in the "Price" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should not see "1000.00" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Chair"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Chair" in the results
    When I copy the "Id" field
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Chair" in the results



Scenario: Query products by name
    When I visit the "Home Page"
    And I press the "Clear" button       
    
    When I set the "Name" to "Lap"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should not see "Smartphone" in the results


Scenario: List Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should see "Smartphone" in the results
    And I should see "Chair" in the results
    And I should not see "Pants" in the results

Scenario: Apply discount to a product
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should see "1000.00" in the "Price" field
    When I set the "Discount" to "20"
    And I press the "Apply-Discount" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should see "800.00" in the "Price" field
