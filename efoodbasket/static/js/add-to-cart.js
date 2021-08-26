window.addEventListener("load", function(){
    var mainCartCountNavElem = document.querySelectorAll(".main-cart-count");

    var addToCartBtns = this.document.querySelectorAll(".add-to-cart");
    var clickedElem = null;

    var onAddSuccess = function(response){
        hideBigLoader();
        var result = JSON.parse(response);
        var newTotalCartItems = result.totalItems;
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
            data.append("product_id", product_id);
            data.append("quantity", quantity);
            ajax("POST", "/ajax/cart/add/", data, onAddSuccess);
        }
    });
});