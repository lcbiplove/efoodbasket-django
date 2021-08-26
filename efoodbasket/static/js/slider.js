/**
 * Slider animates slides horizontally
 *
 * @param {*} imageWrapperId - Image wrapper element id
 * @param {int} hold - Time to hold the slides (in milliseconds)
 * @param {int} transitionTime - Time to change slide (in milliseconds)
 * @param {boolean} autoplay - Autoplay slides or not
 */
 function Slider(
    imageWrapperId,
    hold = 4000,
    transitionTime = 400,
    autoplay = true,
    showNextPrev = true,
  ) {

    let main_width_container = document.querySelector(".main-wrapper");

    const IMAGE_HEIGHT = 600;
  
    const IS_AUTOPLAY = autoplay;
    const TRANSITION_TIME = transitionTime;
    const HOLD_TIME = hold;
  
    this.sliderIndex = 1;
    this.carouselImageContainer = document.getElementById(`${imageWrapperId}`);
  
    this.carouselContainer = this.carouselImageContainer.parentElement;

    let IMAGE_WIDTH = this.carouselContainer.parentElement.clientWidth;

    this.buildPrevNextButtons = () => {
      const arrowsWrapper = document.createElement("div");
      arrowsWrapper.className = "carousel-controls";
    
      this.prev = document.createElement("div");
      this.prev.className = "btn";
      this.prev.innerHTML = '<span class="iconify" data-icon="akar-icons:circle-chevron-left-fill" data-inline="false" data-height="100%"></span>';
    
      this.next = document.createElement("div");
      this.next.className = "btn";
      this.next.innerHTML = '<span class="iconify" data-icon="akar-icons:circle-chevron-right-fill" data-inline="false" data-height="100%"></span>';
    
      arrowsWrapper.appendChild(this.prev);
      arrowsWrapper.appendChild(this.next);
      this.carouselContainer.parentElement.style.width = IMAGE_WIDTH;
      this.carouselContainer.parentElement.style.position = "relative";
      this.carouselContainer.parentElement.appendChild(arrowsWrapper);
    }

    if(showNextPrev){
      this.buildPrevNextButtons();
    }
  
    /* Cloned first and last images are for infinite in forward direction looping 
    slides */
    const clonedFirstImage = this.carouselImageContainer.firstElementChild.cloneNode();
    clonedFirstImage.id = "cloned-first";
  
    const clonedLastImage = this.carouselImageContainer.lastElementChild.cloneNode();
    clonedLastImage.id = "cloned-last";
  
    this.carouselImageContainer.append(clonedFirstImage);
    this.carouselImageContainer.prepend(clonedLastImage);
  
    this.setResizeImage = () => {
      IMAGE_WIDTH = this.carouselContainer.parentElement.clientWidth;
      // Hide cloned lastImage to left side
      this.carouselImageContainer.style.transform = `translateX(-${IMAGE_WIDTH}px) translateZ(0)`;
      this.slidesCount = this.carouselImageContainer.childElementCount;

      this.carouselImageContainer.style.width  = `${IMAGE_WIDTH*this.slidesCount}px`;
      this.carouselContainer.style.maxWidth = `${IMAGE_WIDTH}px`;

      [...this.carouselImageContainer.children].forEach(item => {
        item.style.width = `${IMAGE_WIDTH}px`;
    });
    }
    this.setResizeImage();

    this.autoplay = () => {
      this.autoplay.interval = setInterval(() => {
        this.next.click();
      }, HOLD_TIME);
    };
  
    this.resetAutoplay = () => {
      if (IS_AUTOPLAY) {
        clearInterval(this.autoplay.interval);
        this.autoplay();
      }
    };
  
    this.resetAutoplay();
  
    /**
     * Animate slides to destination slide index
     *
     * @param {int} fromIndex
     * @param {int} toIndex
     */
    this.animate = () => {
        this.carouselImageContainer.style.transform = `translateX(-${
            IMAGE_WIDTH * (this.sliderIndex)
            }px) translateZ(0)`;

      
      this.carouselImageContainer.style.transition = `transform ${TRANSITION_TIME}ms linear`;
    };
  
    /**
     * There is no slide in next direction
     * @returns {boolean}
     */
    this.isNextEnd = () => {
      return this.sliderIndex+2 > this.slidesCount;
    };
  
    /**
     * There is no slide in previous direction
     * @returns {boolean}
     */
    this.isPrevEnd = () => {
      return this.sliderIndex <= 0;
    };
  
    /**
     * Next Button
     */
    this.next.onclick = () => {
      this.resetAutoplay();
  
      if (this.isNextEnd()) return;
  
      this.indicators.forEach(elem => {
        elem.classList.remove("active");
      });
  
      let index = this.sliderIndex >= this.slidesCount - 2 ? 0 : this.sliderIndex;
      this.indicators[index].className = "active";
  
      this.sliderIndex++;
  
      this.animate();
    };
  
    /**
     * Previous Button
     */
    this.prev.onclick = () => {
      this.resetAutoplay();
  
      if (this.isPrevEnd()) return;
  
      this.indicators.forEach(elem => {
        elem.classList.remove("active");
      });
  
      let index =
        this.sliderIndex === 1 ? this.slidesCount - 3 : this.sliderIndex - 2;
      this.indicators[index].className = "active";
  
      this.sliderIndex--;
  
      this.animate();
    };
  
    /**
     * When animation ends
     */
    this.carouselImageContainer.ontransitionend = () => {
      // When the slider reached the cloned last element
      const currentSlide = this.carouselImageContainer.children[this.sliderIndex];
      if (currentSlide.id === clonedLastImage.id) {
        this.sliderIndex = this.slidesCount - 2;
        this.animate();
        this.carouselImageContainer.style.transition = "none";

      }
  
      if (currentSlide.id === clonedFirstImage.id) {
        this.sliderIndex = this.slidesCount - this.sliderIndex;
        this.animate();
        this.carouselImageContainer.style.transition = "none";
      }

    };
  
    /**
     * Dots creations and event listener
     */
  
    const dotsWrapper = document.createElement("div");
    dotsWrapper.className = "carousel-indicators";
  
    this.indicators = [];
    for (let ind = 0; ind < this.slidesCount - 2; ind++) {
      let dot = document.createElement("span");
      dotsWrapper.appendChild(dot);
      this.indicators.push(dot);
  
      dot.onclick = () => {
        this.resetAutoplay();
  
        // Check if slide of current dot is shown
        if (this.sliderIndex === ind + 1) return;
  
        this.indicators.forEach(elem => {
          elem.classList.remove("active");
        });
        this.sliderIndex = ind + 1;
  
        this.animate();
  
        dot.className = "active";
      };
    }
    // Show active status to initial slide
    this.indicators[0].className = "active";
    this.carouselContainer.appendChild(dotsWrapper);
  }


