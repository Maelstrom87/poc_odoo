$(document).ready(function () {
  if (typeof Swiper !== "undefined") {
    new Swiper(".swiper", {
      // Optional parameters
      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      // Responsive breakpoints
      breakpoints: {
        640: {
          slidesPerView: 2,
        },
        1024: {
          slidesPerView: 3,
        },
      },
      // Navigation arrows
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      // Pagination
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      // Autoplay
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
    });
    console.log("Swiper initialized");
  }
});
