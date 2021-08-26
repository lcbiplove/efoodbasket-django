window.addEventListener("load", function () {
    var mainCartCountNavElem = document.querySelectorAll(".main-cart-count");

    totalItems = 0;
    cartLS.list().forEach(function(item){
        totalItems += item.quantity;
    });


    mainCartCountNavElem.forEach(function(item){
        item.innerHTML = totalItems; 
    }); 
});
