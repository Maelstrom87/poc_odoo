odoo.define('custom_lms_categories_owl.slider', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.CourseSliders = publicWidget.Widget.extend({
        selector: '.category-sliders',
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Verifica che jQuery e OwlCarousel siano caricati
                if (typeof $.fn.owlCarousel === 'function') {
                    self.$('.course-carousel').owlCarousel({
                        loop: false,
                        margin: 20,
                        nav: true,
                        navText: ['<i class="fa fa-chevron-left"/>','<i class="fa fa-chevron-right"/>'],
                        dots: false,
                        responsive: {
                            0: { items: 1 },
                            576: { items: 2 },
                            768: { items: 3 },
                            992: { items: 4 }
                        }
                    });
                } else {
                    console.warn('OwlCarousel non è stato caricato correttamente');
                }
            });
        }
    });
});