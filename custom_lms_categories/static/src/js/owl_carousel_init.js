(function () {
  function waitForElement(selector, callback) {
    if (document.querySelector(selector)) {
      callback();
    } else {
      setTimeout(() => waitForElement(selector, callback), 100);
    }
  }

  function initializeCarousels() {
    $(".owl-carousel").each(function () {
      var $carousel = $(this);
      var itemsToShow = 1;

      // Calcola quanti elementi mostrare in base alla larghezza dello schermo
      if (window.innerWidth >= 992) itemsToShow = 4;
      else if (window.innerWidth >= 768) itemsToShow = 3;
      else if (window.innerWidth >= 576) itemsToShow = 2;
      else itemsToShow = 1;

      // Se già inizializzato, distruggilo per evitare duplicati
      if ($carousel.hasClass("owl-carousel") && !$carousel.hasClass("owl-loaded")) {
        $carousel.owlCarousel({
          loop: false,
          margin: 20,
          nav: true,
          dots: false,
          responsive: {
            0: { items: 1 },
            576: { items: 2 },
            768: { items: 3 },
            992: { items: 4 },
          },
          navText: [
            '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>',
            '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>',
          ],
        });
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (typeof jQuery === "undefined") {
      console.error("jQuery ");
      return;
    }
    if (typeof jQuery.fn.owlCarousel === "undefined") {
      console.error(" OwlCarousel non caricati");
      return;
    }

    waitForElement(".owl-carousel .item", function () {
      console.log("Inizializzo Owl Carousel...");
      initializeCarousels();
    });
  });
})();
