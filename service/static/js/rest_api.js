$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_price").val(res.price.toFixed(2));
    }

    // Clears all form fields
    function clear_form_data() {
        $("#product_id").val("");
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
// Search Products
// ****************************************

$("#search-btn").click(function () {
    let name = $("#product_name").val();
    let query_string = "";
    if (name) {
        // 使用精确的名称匹配
        query_string = `?name=${encodeURIComponent(name)}`;
    }

    $("#flash_message").empty();

    let ajax = $.ajax({
        type: "GET",
        url: `/api/products${query_string}`,
        contentType: "application/json",
        data: ''
    });

    ajax.done(function(res){
        $("#search_results").empty();
        
        // 如果是搜索特定名称，只显示完全匹配的结果
        let filteredRes = name 
            ? res.filter(product => product.name.toLowerCase() === name.toLowerCase())
            : res;

        let table = '<table class="table table-striped">' +
                    '<thead><tr>' +
                    '<th class="col-md-1">ID</th>' +
                    '<th class="col-md-4">Name</th>' +
                    '<th class="col-md-4">Description</th>' +
                    '<th class="col-md-3">Price</th>' +
                    '</tr></thead><tbody>';

        filteredRes.forEach(product => {
            table += `<tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.description}</td>
                <td>$${product.price.toFixed(2)}</td>
            </tr>`;
        });

        table += '</tbody></table>';
        $("#search_results").append(table);

        // 如果有精确匹配的结果，填充表单
        if (filteredRes.length === 1) {
            update_form_data(filteredRes[0]);
        }

        flash_message("Success");
    });

    ajax.fail(function(res){
        clear_form_data();
        flash_message(res.responseJSON?.message || "Error occurred while searching for products!");
    });
});
    // ****************************************
    // List All Products
    // ****************************************

    $("#list-btn").click(function () {

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: "/api/products",
            contentType: "application/json",
            data: '',
        });

        ajax.done(function (res) {
            $("#search_results").empty();
            res.forEach(product => {
                let row = `<tr>
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                </tr>`;
                $("#search_results").append(row);
            });
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message("Error occurred while listing all products!");
        });

    });
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
        console.log("Parsed Price:", parseFloat(price)); // Debugging the parsed price

        let ajax = $.ajax({
            type: "POST",
            url: "/api/products", // Adjust this URL if necessary
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
    }   );

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
            url: `/api/products/${product_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            clear_form_data();
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
            url: `/api/products/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a product
    // ****************************************
    $("#delete-btn").click(function () {
        let product_id = $("#product_id").val();
        
        if (!product_id) {
            flash_message("Please select a product to delete");
            return;
        }
    
        $("#flash_message").empty();
    
        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })
    
        ajax.done(function(res){
            clear_form_data();
            
            flash_message("Success");
            
        });
    
        ajax.fail(function(res){
            console.error('Delete failed:', res);
            flash_message(res.responseJSON?.message || `Server error! Status: ${res.status}`);
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        //$("#product_id").val("");
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
            url: `/api/products/${product_id}/discount`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message || "Error occurred while applying the discount!");
        });

    });

});
