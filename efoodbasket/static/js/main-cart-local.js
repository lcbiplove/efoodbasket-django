showBigLoader();
window.addEventListener("load", function () {
    hideBigLoader();

    var mainCartCountNavElem = document.querySelectorAll(".main-cart-count");

    var cartItemCountSelectElem = document.getElementById("cart-items-selected");
    var checkAllCheckbox = document.getElementById("checkAllCheckbox");
    var cartTotalElements = document.querySelector(".cart-total-price");
    var subTotalElement = document.getElementById("cart-sub-total");
    var mainDeleteBtn = document.getElementById("main-delete");
    var cardRowElem = document.getElementById("card-row");

    var allCheckboxes, allSubtractBtns, allAddBtns, allDeleteBtns;

    var loadLazyElems = function() {
        allCheckboxes = document.querySelectorAll(".each-checkbox");
        allQuantities = document.querySelectorAll(".each-quantity");
        allTotals = document.querySelectorAll(".each-total");
        allSubtractBtns = document.querySelectorAll(".each-subtract");
        allAddBtns = document.querySelectorAll(".each-add");
        allDeleteBtns = document.querySelectorAll(".each-delete");
    }

    var getCartItemsCount = function () {
        totalItems = 0;
        cartLS.list().forEach(function(item){
            totalItems += item.quantity;
        });
        return totalItems;
    }

    var getSelectedItems = function () {
        var selected_ids = [];
        (document.querySelectorAll(".each-checkbox")).forEach(function (item, index) {
          if (item.checked === true) {
            var myProductData = cartLS.list();
            if(myProductData[index]){
              var id = myProductData[index].id;
              selected_ids.push(id);
            }
          }
        });
        return selected_ids;
    };

    var getGrandTotal = function (params) {
        var total = 0;
        cartLS.list().forEach(function (item) {
            total += (100-item.discount) * item.price * item.quantity / 100;
        });
        return total;
    }

    var updateElems = function () {
        mainCartCountNavElem.forEach(function(item){
            item.innerHTML = getCartItemsCount(); 
        }); 
        cartItemCountSelectElem.innerHTML = getCartItemsCount(); 

        cartTotalElements.innerHTML = "&pound;"+getGrandTotal().toFixed(2);
        subTotalElement.innerHTML = "&pound;"+getGrandTotal().toFixed(2);
    }

    var loadCart = function () {
        if(getCartItemsCount() <= 0){
            cardRowElem.innerHTML = "<div style='margin: 60px auto; text-align: center'>No cart item added</div>";
            return;
        }

        cartTotalElements.innerHTML = "&pound;"+getGrandTotal().toFixed(2);
        subTotalElement.innerHTML = "&pound;"+getGrandTotal().toFixed(2);

        cartItemCountSelectElem.innerHTML = getCartItemsCount();
        cartLS.list().forEach(function(item){
            var total = item.quantity * item.price * (100-item.discount) / 100 ;
            var content = `<div class='card-col-big' data-product-id='${item.id}' > <label class='select-check-container'> <input class='each-checkbox' type='checkbox' /> <span class='checkmark'></span> </label> <div class='card-big'> <div class='card-img-wrapper'> <a href='/products/${item.id}/'> <img class='card-big-img' src='${item.image}' alt='cart-item' /> </a> </div> <div class='card-big-body'> <div class='card-big-title'> <a href='/products/${item.id}/' >${item.name}</a > <button class='individual-delete-btn each-delete' data-product-id='${item.id}'> <span class='iconify' data-icon='fluent:delete-20-regular' data-inline='false' ></span> </button> </div> <div class='card-key-value-wrapper'> <div class='card-key-value-row'> <div class='card-key no-key-sm'>Price</div> <div class='card-value'> <div class='card-big-price each-price'> &pound;${item.price.toFixed(2)} </div> </div> </div> ${item.discount > 0 ? `<div class='card-key-value-row'> <div class='card-value'> <div class='light-text'> <b >${item.discount}% off</b > </div> </div> </div>` : "" }  </div> <div class='quantity-total-wrapper'> <div class='quantity-wrapper'> <span class='no-key-sm'>Quantity</span> <button class='quantity-btn each-subtract add-to-cart' data-product-id='${item.id}' data-quantity='${item.quantity}' > - </button> <span class='quantity each-quantity' data-product-id='${item.id}'>${item.quantity}</span > <button class=' quantity-btn each-add add-to-cart ' data-product-id='${item.id}' data-quantity='${item.quantity}' > + </button> </div> <div class='total-wrapper'> <div class='total-text'>Total</div> <div class='total-value each-total' data-product-id='${item.id}'> &pound;${total.toFixed(2)} </div> </div> </div> </div> </div> </div>`;
            cardRowElem.innerHTML += content;
        });

        loadLazyElems();

        allAddBtns.forEach(function (item, index) {
            item.onclick = function (e) {
                e.preventDefault();
                var product_id = item.getAttribute("data-product-id");

                if(getCartItemsCount() < 20) {
                    cartLS.quantity(product_id, +1);
                    updateElems();
                    var total = (100-cartLS.get(product_id).discount) * cartLS.get(product_id).price * cartLS.get(product_id).quantity / 100;
                    var quantityRow = document.querySelector(".each-quantity[data-product-id='"+product_id+"']");
                    var totalRow = document.querySelector(".each-total[data-product-id='"+product_id+"']");
                    quantityRow.innerHTML = cartLS.get(product_id).quantity;
                    totalRow.innerHTML = "&pound;"+total.toFixed(2);
                } else {
                    showJsMessage("Product is already full.", "info");
                }
            };
        });

        allSubtractBtns.forEach(function(item, index) {
            item.onclick = function (e) {
                e.preventDefault();
                var product_id = item.getAttribute("data-product-id");
                var quantity = cartLS.get(product_id).quantity;

                if(quantity > 1) {
                    cartLS.quantity(product_id, -1);
                    updateElems();
                    var total = (100-cartLS.get(product_id).discount) * cartLS.get(product_id).price * cartLS.get(product_id).quantity / 100;
                    var quantityRow = document.querySelector(".each-quantity[data-product-id='"+product_id+"']");
                    var totalRow = document.querySelector(".each-total[data-product-id='"+product_id+"']");
                    quantityRow.innerHTML = cartLS.get(product_id).quantity;
                    totalRow.innerHTML = "&pound;"+total.toFixed(2);
                } 
            };
        });

        checkAllCheckbox.onclick = function () {
            allCheckboxes.forEach(function (item) {
                if (checkAllCheckbox.checked === true) {
                    item.checked = true;
                } else {
                    item.checked = false;
                }
            });
        };

        mainDeleteBtn.onclick = function () {
            var product_ids_array = getSelectedItems();

            if(product_ids_array.length > 0){
                product_ids_array.forEach(function(id){
                    var row = document.querySelector(".card-col-big[data-product-id='"+id+"']");
                    row.style = "opacity: 0.1; transition: opacity 1s; pointer-events: none;";
                    setTimeout(function () {
                        row.remove();
                        cartLS.remove(id);
                        updateElems();  

                        checkAllCheckbox.checked = false;

                        if(getCartItemsCount() == 0){
                            window.location.reload();
                        }
                    }, 1000);
                });
            }
        }     
        
        allDeleteBtns.forEach(function (item) {
            item.onclick = function () {
                var product_id = item.getAttribute("data-product-id");
                
                var row = document.querySelector(".card-col-big[data-product-id='"+product_id+"']");
                row.style = "opacity: 0.1; transition: opacity 1s; pointer-events: none;";
                setTimeout(function () {
                    row.remove();
                    cartLS.remove(product_id);
                    updateElems();  

                    if(getCartItemsCount() == 0){
                        window.location.reload();
                    }
                }, 800);
            };
        });
    }

    loadCart();

    
});