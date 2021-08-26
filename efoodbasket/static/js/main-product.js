window.addEventListener("load", function(){
    imageZoom("preview-img", "zoom-img-result"); 

    var stock_count = this.document.getElementById("stock-count").getAttribute("data-stock-count");
    
    var MAX_QUANTITY_VALUE = stock_count > 20 ? 20 : stock_count;

    var previewImage = document.getElementById("preview-img");
    var productIndicators = document.querySelectorAll(".product-img-indicator");

    var buyNowBtn = document.getElementById("buy-now");
    var addToCartBtn = document.getElementById("add-to-cart");

    var addQuantityBtn = document.getElementById("add-quantity") || 0;
    var subtractQuantityBtn = document.getElementById("subtract-quantity") || 0;
    var quantityValueDiv = document.getElementById("quantity-value");

    var quantityValue = +quantityValueDiv.innerHTML || 1;

    var totalRatingCount = document.querySelector(".rating-summary-wrapper").getAttribute("data-rating-count");

    var shareProduct = document.getElementById("share-product");

    if(shareProduct) {
        shareProduct.onclick = function() {
            var copyText = window.location.href;
            var fakeInpt = document.createElement("input");
            document.body.appendChild(fakeInpt);
            fakeInpt.value = copyText;
            fakeInpt.select();
            document.execCommand("copy");
            document.body.removeChild(fakeInpt);

            showJsMessage("Link copied to clipboard.", 'success', 5000)
        }
    }

    var checkDisablePlusMinus = function() {
        if(quantityValue <= 1){
            subtractQuantityBtn.classList.add("disabled");

        } else {
            subtractQuantityBtn.classList.remove("disabled");
        }

        if(quantityValue >= MAX_QUANTITY_VALUE){
            addQuantityBtn.classList.add("disabled");
        } else {
            addQuantityBtn.classList.remove("disabled");
        }
    }

    if(subtractQuantityBtn || addQuantityBtn)
    {
        checkDisablePlusMinus();
    }

    addQuantityBtn.onclick = function(){
        quantityValue += 1;
        quantityValueDiv.innerHTML = quantityValue;
        addToCartBtn.setAttribute("data-quantity", quantityValue);
        checkDisablePlusMinus();
    }
    subtractQuantityBtn.onclick = function(){
        quantityValue -= 1;
        quantityValueDiv.innerHTML = quantityValue;
        addToCartBtn.setAttribute("data-quantity", quantityValue);

        checkDisablePlusMinus();
    }

    productIndicators.forEach(function(item){
        item.onclick = function(){
            var shopByContainer = document.querySelector(".shop-by-images-container");

            productIndicators.forEach(function(item){
                item.classList.remove("active");
            });

            this.classList.add("active");

            shopByContainer.scrollTo({
                behavior: 'smooth',
                left: this.offsetLeft
            });
            previewImage.setAttribute("src", this.getAttribute("src"));
            imageZoom("preview-img", "zoom-img-result");
        }
    });

    // Check if from notification
    var url_string = this.window.location.href;
    var url = new URL(url_string);
    var give_review = url.searchParams.get("give_review");
    var orderId = url.searchParams.get("order_id");

    if(give_review && orderId) {
        var eachRow = document.querySelector(".review-form-wrapper");

        eachRow.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        });
        eachRow.style = "animation: focusFade 2s";
    }
});

