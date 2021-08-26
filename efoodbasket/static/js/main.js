var slider = new Slider("first-slider", 4000, 400);

window.addEventListener('resize', function(){
  slider.setResizeImage();
});