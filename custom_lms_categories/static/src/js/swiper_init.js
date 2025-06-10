$(document).ready(function () {
  // Initialize all Swiper instances
  $(".swiper").each(function () {
    new Swiper(this, {
      // Default settings for mobile (1 slide)
      slidesPerView: 1,
      spaceBetween: 20,
      loop: false,
      centeredSlides: true,
      autoplay: false,

      navigation: {
        nextEl: this.querySelector(".custom-swiper-button-next"),
        prevEl: this.querySelector(".custom-swiper-button-prev"),
        enabled: window.innerWidth >= 768,
      },
      pagination: {
        el: this.querySelector(".custom-swiper-pagination"),
        bulletActiveClass: "custom-swiper-pagination-bullet-active",
        bulletClass: "custom-swiper-pagination-bullet",
        clickable: true,
        enabled: true,
        renderBullet: function (index, className) {
          return '<span class="' + className + '"></span>';
        },
      },
      breakpoints: {
        // Mobile first approach
        320: {
          slidesPerView: 1,
          spaceBetween: 10,
          centeredSlides: true,
          slidesPerGroup: 1,
          navigation: {
            enabled: false,
          },
        },
        // when window width is >= 640px
        640: {
          slidesPerView: 2,
          spaceBetween: 15,
          centeredSlides: false,
          slidesPerGroup: 2,
          navigation: {
            enabled: false,
          },
        },
        // when window width is >= 768px
        768: {
          slidesPerView: 3,
          spaceBetween: 15,
          centeredSlides: false,
          navigation: {
            enabled: true,
          },
          slidesPerGroup: 3,
        },
        // when window width is >= 1024px
        1024: {
          slidesPerView: 4,
          spaceBetween: 30,
          centeredSlides: false,
          slidesPerGroup: 4,
        },
        // Quando la larghezza della finestra è < 768px
        0: {
          navigation: {
            enabled: false,
          },
          pagination: {
            enabled: true,
          },
        },
      },
      on: {
        slideChangeTransitionStart: function () {
          const activeIndex = this.activeIndex;
          const slidesPerView = this.params.slidesPerView;
          const slides = this.slides;
          // Remove "out-of-view" class from all slides
          slides.forEach((slide) => {
            slide.classList.remove("out-of-view");
          });
          // Apply "out-of-view" class to slides outside the container
          slides.forEach((slide, index) => {
            if (index < activeIndex || index > activeIndex + (slidesPerView - 1)) {
              slide.classList.add("out-of-view");
            }
          });
        },

        // Apply the same logic on initialization
        init: function () {
          const activeIndex = this.activeIndex;
          const slidesPerView = this.params.slidesPerView;
          const slides = this.slides;
          slides.forEach((slide) => {
            slide.classList.remove("out-of-view");
          });
          slides.forEach((slide, index) => {
            if (index < activeIndex || index > activeIndex + (slidesPerView - 1)) {
              slide.classList.add("out-of-view");
            }
          });
        },
      },
    });
  });
});