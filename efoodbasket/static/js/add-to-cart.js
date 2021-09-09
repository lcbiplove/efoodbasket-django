window.addEventListener("load", function(){
    var mainCartCountNavElem = document.querySelectorAll(".main-cart-count");

    var addToCartBtns = this.document.querySelectorAll(".add-to-cart");
    var clickedElem = null;

    var onAddSuccess = function(response){
        hideBigLoader();
        var result = JSON.parse(response);
        var newTotalCartItems = result.total_items;
        showJsMessage(result.message, result.type);
        mainCartCountNavElem.forEach(function(item){
            item.innerHTML = newTotalCartItems; 
        }); 
    }

    addToCartBtns.forEach(function(elem){
        elem.onclick = function(e){
            e.preventDefault();
            showBigLoader();

            clickedElem = elem;

            var product_id = elem.getAttribute("data-product-id");
            var quantity = elem.getAttribute("data-quantity") || 1;

            var data = new FormData();
            data.append("product", product_id);
            data.append("quantity", quantity);
            data.append("csrfmiddlewaretoken", getCookie('csrftoken'));
            ajax("POST", "/ajax/carts/add/", data, onAddSuccess);
        }
    });
});