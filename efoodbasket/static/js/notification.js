window.addEventListener("load", function(){
    var notifRows = this.document.querySelectorAll(".notif-row");
    var unseenElem = this.document.getElementById("unseen-count");

    notifRows.forEach(function(item) {
        item.onclick = function(e) {
            e.preventDefault();
            showBigLoader();

            var redirectTo = this.getAttribute("href");
            var notifId = this.getAttribute("data-notif-id");

            var onSuccess = function(response) {
                hideBigLoader();

                var data = JSON.parse(response);

                if(data.success == "ok"){
                    item.classList.remove("notif-not-seen");
                    unseenElem.innerHTML = unseenElem.innerHTML - 1;
                } 
                window.location.href = redirectTo;
            }

            var action = "/ajax/notifications/" + notifId + "/make-seen/";
            var data = new FormData();
            data.append("id", notifId);
            data.append("csrfmiddlewaretoken", getCookie('csrftoken'));
            ajax("POST", action, data, onSuccess);
        }
    });
    
});

