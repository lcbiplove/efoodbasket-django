window.addEventListener("load", function(){
    var mainCartCountNavElem = document.querySelectorAll(".main-cart-count");
    var addToCartBtns = this.document.querySelectorAll(".add-to-cart");
    var clickedElem = null;

    var getCartItemsCount = function () {
        totalItems = 0;
        cartLS.list().forEach(function(item){
            totalItems += item.quantity;
        });
        return totalItems;
    }

    addToCartBtns.forEach(function(elem){
        elem.onclick = function(e){
            e.preventDefault();
            clickedElem = elem;

            var product_id = elem.getAttribute("data-product-id");
            var product_name = elem.getAttribute("data-product-name");
            var quantity = elem.getAttribute("data-quantity") || 1;
            var price = elem.getAttribute("data-price");
            var discount = elem.getAttribute("data-discount");
            var image = elem.getAttribute("data-image");

            if(getCartItemsCount() < 20) {
                cartLS.add({id: product_id, name: product_name, price: +price, quantity: +quantity, discount: +discount, image: image});
                showJsMessage("Product added to cart", "success");
                mainCartCountNavElem.forEach(function(item){
                    item.innerHTML = getCartItemsCount(); 
                }); 
            } else {
                showJsMessage("Product is already full.", "info");
            }
        }
    });
});