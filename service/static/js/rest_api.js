$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_price").val(res.price);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#product_name").val();
        let description = $("#product_description").val();
        let price = $("#product_price").val();

        let data = {
            "name": name,
            "description": description,
            "price": parseFloat(price)
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Product created successfully!");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message || "Error occurred while creating the product!");
        });
    });

    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let description = $("#product_description").val();
        let price = $("#product_price").val();

        let data = {
            "name": name,
            "description": description,
            "price": parseFloat(price)
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Product updated successfully!");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message || "Error occurred while updating the product!");
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: '',
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Product retrieved successfully!");
        });

        ajax.fail(function (res) {
            clear_form_data();
            flash_message(res.responseJSON.message || "Error occurred while retrieving the product!");
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: '',
        });

        ajax.done(function (res) {
            clear_form_data();
            flash_message("Product deleted successfully!");
        });

        ajax.fail(function (res) {
            flash_message("Error occurred while deleting the product!");
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data();
    });

    // ****************************************
    // Apply Discount to a Product
    // ****************************************

    $("#apply-discount-btn").click(function () {

        let product_id = $("#product_id").val();
        let discount_percentage = $("#discount_percentage").val();

        let data = {
            "discount_percentage": parseFloat(discount_percentage)
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/products/${product_id}/discount`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Discount applied successfully!");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message || "Error occurred while applying the discount!");
        });

    });

});
