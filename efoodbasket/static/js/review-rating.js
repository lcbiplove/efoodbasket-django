window.addEventListener("load", function () {
    var giveRating = document.getElementById("give-rating");
    var reviewInpt = document.getElementById("review-inpt");
    var rateBtn = document.getElementById("rate-btn");
    var reviewForm = document.getElementById("review-form");
    var deleteReview = document.querySelector(".delete-review") || 0;
    var editReview = document.querySelector(".edit-review") || 0;

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

        var formData = new FormData();
        var action = rateBtn.getAttribute('data-action');
        formData.append("rating", rating);
        formData.append("csrfmiddlewaretoken", getCookie('csrftoken'));

        ajax("POST", action, formData, function(response){
            console.log(response);
            hideBigLoader();
        });
    }

    reviewForm.onsubmit = function (e) {
        e.preventDefault();
        showBigLoader();

        var review = reviewInpt.value;

        if(review.length < 10) {
            hideBigLoader();
            showJsMessage("Review must be at least 10 characters long.", "fail");
            return;
        }
        
        var formData = new FormData();
        formData.append('review', review);
        formData.append("csrfmiddlewaretoken", getCookie('csrftoken'));

        var action = this.getAttribute('action');

        ajax("POST", action, formData, function (response) {
            console.log(response);
            try {
                data = JSON.parse(response);

                hideBigLoader();
                reviewInpt.value = "";

                if(data.hasOwnProperty("error")) {
                    showJsMessage(data.error, "fail");
                    return;
                }

            } catch (error) {}

            window.location.reload();
        });
    }

    deleteReview.onclick = function () {
        showBigLoader();
        if(confirm('Are you sure you want to delete this review?\n\n*Note:- Your review will be removed permanantly.')){

            var action = this.getAttribute("data-action");
            var formData = new FormData();
            formData.append("data", "data");
            formData.append("csrfmiddlewaretoken", getCookie('csrftoken'));
    
            ajax("POST", action, formData, function (response) {
                hideBigLoader();
                console.log(response);
            });
        } else {
            hideBigLoader();
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
});