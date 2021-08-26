window.addEventListener("load", function(){
    var message_box = this.document.getElementById("message_box");
    var addFormOne = this.document.getElementById("add-shop-form-one");
    var addBtnOne = this.document.getElementById("add-shop-btn-one");

    var errName = this.document.getElementById("err-name");
    var errAddress = this.document.getElementById("err-address");
    var errContact = this.document.getElementById("err-contact");

    var url_string = this.window.location.href;
    var url = new URL(url_string);
    var nextUrl = url.searchParams.get("next");

    addBtnOne.onclick = function(e){
        e.preventDefault();
        showBigLoader();

        var formData = new FormData();
        for(var i=0; i<addFormOne.length; i++)
        {
            formData.append(addFormOne[i].name, addFormOne[i].value);
        }
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            hideBigLoader();

            data = JSON.parse(this.responseText);

            if(data.redirectTo) {
                location.href = data.redirectTo;
            }

            if(data.count >= 2){
                location.href = "/trader/shops/";
            }

            if(data.error === 1){
                errName.innerHTML = data.shop_name ?? "";
                errAddress.innerHTML = data.address ?? "";
                errContact.innerHTML = data.contact ?? "";
            }

            if(data.success === 1) {
                addFormOne.reset();

                message_box.innerHTML = "<div style='margin: 20px 0; border-radius: 5px; padding: 15px; width: 100%; box-sizing: border-box; color: #fff; background-color: var(--light-green);'>Shop added successfully.</div>";
            }
        }
        var param = nextUrl ? "?next=" + nextUrl : ""
        xhttp.open("POST", "/ajax/trader/add-shop/"+param);
        xhttp.send(formData);
    }
});