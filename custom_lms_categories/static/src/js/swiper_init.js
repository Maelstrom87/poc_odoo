$(document).ready(function () {
  // Initialize all Swiper instances
  $(".swiper").each(function () {
    new Swiper(this, {
      slidesPerView: 4,
      spaceBetween: 20,
      loop: false,
      centeredSlides: false,

      navigation: {
        nextEl: this.querySelector(".custom-swiper-button-next"),
        prevEl: this.querySelector(".custom-swiper-button-prev"),
      },
      pagination: {
        el: this.querySelector(".swiper-pagination"),
        clickable: true,
      },
      breakpoints: {
        640: { slidesPerView: 2 },
        768: { slidesPerView: 3 },
        1024: { slidesPerView: 4 },
      },
      on: {
        slideChangeTransitionStart: function () {
          const activeIndex = this.activeIndex;
          const slidesPerView = this.params.slidesPerView;
          const slides = this.slides;
          // Rimuovi la classe "out-of-view" da tutte le slide
          slides.forEach((slide) => {
            slide.classList.remove("out-of-view");
          });
          // Applica la classe "out-of-view" alle slide fuori dal container
          slides.forEach((slide, index) => {
            if (index < activeIndex || index > activeIndex + (slidesPerView - 1)) {
              slide.classList.add("out-of-view");
            }
          });
        },
        // Applica la logica anche all'inizializzazione
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
