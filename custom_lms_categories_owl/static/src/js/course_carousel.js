document.addEventListener('DOMContentLoaded', function () {
    console.log("Caricamento del carosello..."); // Debug: Verifica che il codice venga eseguito

    const carousel = document.querySelector('.course-carousel');
    const prevButton = document.querySelector('.carousel-control.prev');
    const nextButton = document.querySelector('.carousel-control.next');
    const courseCards = document.querySelectorAll('.course-card');
    const cardWidth = courseCards[0].offsetWidth + 10; // Larghezza della card + gap
    const visibleCards = 6; // Numero di card visibili alla volta
    const scrollAmount = cardWidth * visibleCards; // Quantità di scorrimento

    console.log("Larghezza della card:", cardWidth); // Debug: Verifica la larghezza della card

    // Scorrimento a sinistra
    prevButton.addEventListener('click', () => {
        console.log("Cliccato su prev"); // Debug: Verifica il clic su prev
        carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    // Scorrimento a destra
    nextButton.addEventListener('click', () => {
        console.log("Cliccato su next"); // Debug: Verifica il clic su next
        carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });

    // Effetto mouseover sulle card
    courseCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.querySelector('.course-overlay').style.transform = 'translateY(0)';
            card.style.transform = 'scale(1.05)'; // Zoom out al passaggio del mouse
        });

        card.addEventListener('mouseout', () => {
            card.querySelector('.course-overlay').style.transform = 'translateY(100%)';
            card.style.transform = 'scale(1)'; // Ripristina la dimensione originale
        });
    });
});
