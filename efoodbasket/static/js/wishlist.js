window.addEventListener("load", function(){
    var emptyHeart = "<span class='iconify' data-icon='el:heart-empty' data-inline='false'></span>";
    var filledHeart = "<span class='iconify' data-icon='bi:heart-fill' data-inline='false'></span>";
    
    var wishlistButtons = this.document.querySelectorAll(".wishlist-button");

    var currentWishElem = null;

    var onWishlistAdd = function(response) {
        currentWishElem.innerHTML = filledHeart;
        currentWishElem.classList.add("active");
    }

    var onWishlistDel = function(response) {
        currentWishElem.innerHTML = emptyHeart;
        currentWishElem.classList.remove("active");
    }

    wishlistButtons.forEach(function(element) {
        element.onclick = function() {
            currentWishElem = element;
            var product_id = element.getAttribute("data-product-id");

            var data = new FormData();
            data.append("csrfmiddlewaretoken", getCookie('csrftoken'));

            if(currentWishElem.classList.contains("active")){
                var action = "/ajax/products/"+product_id+"/wishlists/delete/";
                ajax("POST", action, data, onWishlistDel);
            } 
            else {
                var action = "/ajax/products/"+product_id+"/wishlists/add/";
                ajax("POST", action, data, onWishlistAdd);
            }
        }
    });

});