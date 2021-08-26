function imageZoom(imgID, resultID) {
    var img, lens, result, cx, cy;

    var moveLens = function(e) {
        var pos, x, y;

        e.preventDefault();

        pos = getCursorPos(e);

        x = pos.x - (lens.offsetWidth / 2);
        y = pos.y - (lens.offsetHeight / 2);

        if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;}
        if (x < 0) {x = 0;}
        if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight;}
        if (y < 0) {y = 0;}

        lens.style.left = x + "px";
        lens.style.top = y + "px";

        result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
    }
    var getCursorPos = function(e) {
        var a, x = 0, y = 0;
        e = e || window.event;

        a = img.getBoundingClientRect();

        x = e.pageX - a.left;
        y = e.pageY - a.top;

        x = x - window.pageXOffset;
        y = y - window.pageYOffset;
        return {x : x, y : y};
    }

    var buildAllBlocks = function(){
        var alreadyLens = document.querySelectorAll(".img-zoom-lens");
        alreadyLens.forEach(function(item) {
            item.remove();
        });

        img = document.getElementById(imgID);
        result = document.getElementById(resultID);

        lens = document.createElement("DIV");
        lens.setAttribute("class", "img-zoom-lens");

        img.parentElement.insertBefore(lens, img);

        cx = result.offsetWidth / lens.offsetWidth;
        cy = result.offsetHeight / lens.offsetHeight;

        result.style.backgroundImage = "url('" + img.src + "')";
        result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
    }


    var myMoveLensListener = moveLens.bind(this);

    var myMouseEnterListener = function(e){
        lens.style.visibility = "visible";
        result.style.transform = "scale(1)";
    }.bind(this);

    var myMouseLeaveListener = function(e){
        lens.style.visibility = "hidden";
        result.style.transform = "scale(0)";
    }.bind(this);

    var checkForWidth = function(){
        if(innerWidth <= 620 && ((typeof lens !== "undefined" || typeof img !== "undefined" )) ){
            lens.removeEventListener('mousemove', myMoveLensListener);
            img.removeEventListener('mousemove', myMoveLensListener);
            img.parentElement.removeEventListener("mouseenter", myMouseEnterListener);
            img.parentElement.removeEventListener("mouseleave", myMouseLeaveListener);
        } else {
            buildAllBlocks();

            lens.addEventListener('mousemove', myMoveLensListener);
            img.addEventListener('mousemove', myMoveLensListener);
            img.parentElement.addEventListener("mouseenter", myMouseEnterListener);
            img.parentElement.addEventListener("mouseleave", myMouseLeaveListener);
        }
    }

    window.addEventListener("resize", function(){
        checkForWidth();
    });
    checkForWidth();
}