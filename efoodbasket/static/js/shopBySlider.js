window.onload = function() {
  /* Slider for cards */
  var shopByNext = document.getElementById("shop-by-next");
  var shopByPrev = document.getElementById("shop-by-prev");

  var browse = document.querySelector(".shop-by-images-container");

  var browseControls = document.querySelector(".shop-by-controls");

  var scrollTo = 0;

  var screen_width = document.querySelector(".shop-by-images-wrapper").offsetWidth;

  window.onresize = function(){
    checkBrowserOverflow();
  }


  shopByNext.addEventListener("click", function () {
    var browse_width = browse.scrollWidth;
    var initial = scrollTo;
    
    scrollTo += screen_width;


    if (scrollTo > browse_width) scrollTo = initial;

    browse.scrollTo({
      left: scrollTo,
      behavior: "smooth"
    });
  });

  shopByPrev.addEventListener("click", function () {
    scrollTo -= screen_width;

    if (scrollTo < 0) scrollTo = 0;

    browse.scrollTo({
      left: scrollTo,
      behavior: "smooth"
    });
  });

  /** If browse by category is overflowing, then only
   * show next and previous buttons
   */
  var checkBrowserOverflow = function () {

    if (browse.scrollWidth > browse.clientWidth) {
      screen_width = document.querySelector(".shop-by-images-wrapper").offsetWidth;
      browseControls.classList.remove("d-none");
    } else {
      browseControls.classList.add("d-none");
    }
  };

  checkBrowserOverflow();
}



