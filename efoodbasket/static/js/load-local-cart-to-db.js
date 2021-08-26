window.addEventListener("load", function(){
    var login_btn = document.querySelector(".login-btn");
    var emailInpt = document.querySelector("#emailId");
    var passwordInpt = document.querySelector("#passwordId");

    var getCartItemsCount = function () {
        totalItems = 0;
        cartLS.list().forEach(function(item){
            totalItems += item.quantity;
        });
        return totalItems;
    }

    var getCartString = function() {
        var new_array = [];
        cartLS.list().filter(function(item){
            var obj = {};
            obj['product_id'] = item.id;
            obj['quantity'] = item.quantity;
            new_array.push(obj);
        });
        return JSON.stringify(new_array);
    }

    var onAddSuccess = function(response){
        hideBigLoader();

        var data = JSON.parse(response);

        if(data.hasOwnProperty('clearLocal')) {
            cartLS.destroy();
        }

        if(data.hasOwnProperty('error')){
            window.location.reload();
        }
        if(data.hasOwnProperty('success')){
            window.location.replace('/cart/');
        }
    }

    login_btn.onclick = function(e){
        e.preventDefault();
        showBigLoader();

        var data = new FormData();
        data.append("email", emailInpt.value);
        data.append("password", passwordInpt.value);
        data.append("cart", getCartString());
        data.append("cartItemsCount", getCartItemsCount());

        ajax("POST", "/login/?next=/cart/", data, onAddSuccess);
    }
});