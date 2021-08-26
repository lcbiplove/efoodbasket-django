window.addEventListener("load", function () {
    var giveRating = document.getElementById("give-rating");
    var ratingInpt = document.getElementById("rating-inpt");
    var reviewInpt = document.getElementById("review-inpt");
    var rateBtn = document.getElementById("rate-btn");
    var reviewForm = document.getElementById("review-form");
    var editReview = document.querySelector(".edit-review") || 0;
    var deleteReview = document.querySelector(".delete-review") || 0;

    var rating;

    giveRating.onmousemove = function (e) {
        var width = giveRating.offsetWidth;
        var x = e.offsetX;
        
        var my_rating = x/width * 5;
        rating = (Math.round(my_rating * 2) / 2).toFixed(1)

        rateBtn.classList.remove("disabled");
        if(rating <= 1) {
            rating = 1;
        }

        this.style = "--rating: "+rating;
    }

    rateBtn.onclick = function (e) {
        e.preventDefault();
        showBigLoader();

        var action = reviewForm.getAttribute('action');
        var formData = new FormData();
        formData.append("rating", rating);

        ajax("POST", action, formData, function(response){
            hideBigLoader();
            window.location.reload();
            ratingInpt.value = rating;
        });
    }

    reviewForm.onsubmit = function (e) {
        e.preventDefault();
        showBigLoader();

        var review = reviewInpt.value;
        var my_rating = ratingInpt.value;

        if(review.length < 10) {
            hideBigLoader();
            showJsMessage("Review must be at least 10 characters long.", "fail");
        }
        else if(my_rating.length <= 0) {
            hideBigLoader();
            showJsMessage("Please rate the product in order to review.", "fail");
        }
        else if(my_rating.length > 0) {
            var formData = new FormData();
            formData.append('rating', my_rating);
            formData.append('review_text', review);

            var action = this.getAttribute('action');
            ajax("POST", action, formData, function (response) {
                hideBigLoader();
                reviewInpt.value = "";
                window.location.reload();
            });
        }
    }

    editReview.onclick = function () {
        var review_text = this.getAttribute('data-review-text');

        reviewInpt.value = review_text;
        reviewInpt.focus();

        reviewForm.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        });
    }

    deleteReview.onclick = function () {
        showBigLoader();
        if(confirm('Are you sure you want to delete this review?\n\n*Note:- Your rating and review both will be removed permanantly.')){
            var product_id = this.getAttribute('data-product-id');

            var action = "/ajax/products/"+product_id+"/delete-review/";
            var formData = new FormData();
            formData.append("data", "data");
            ajax("POST", action, formData, function () {
                hideBigLoader();
                window.location.reload();
            });
        } else {
            hideBigLoader();
        }
    }
});