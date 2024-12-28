class Slider {
    constructor(options) {
        this.container = document.querySelector('.slider');
        this.slides = Array.from(this.container.querySelectorAll('.slider-slide'));
        this.paginationContainer = this.container.querySelector('.slider-pagination');
        this.counter = this.container.querySelector('#slider-counter');
        this.currentSlideIndex = 0;
        this.loop = options.loop;
        this.auto = options.auto;
        this.stopMouseHover = options.stopMouseHover;
        this.navs = options.navs;
        this.pags = options.pags;
        this.delay = options.delay;
        this.autoSlideInterval = null;

        this.setup();
    }

    setup() {
        this.showSlide(this.currentSlideIndex);

        // Обработчик клика по слайду
        this.slides.forEach(slide => {
            slide.addEventListener('click', () => {
                const link = slide.getAttribute('data-link');
                if (link) {
                    window.location.href = link;
                }
            });
        });

        // Автопереключение
        if (this.auto) {
            this.startAutoSlide();
            if (this.stopMouseHover) {
                this.container.addEventListener('mouseenter', () => this.stopAutoSlide());
                this.container.addEventListener('mouseleave', () => this.startAutoSlide());
            }
        }

        this.updateNavVisibility();
    }


    startAutoSlide() {
        this.autoSlideInterval = setInterval(() => {
            this.nextSlide();
        }, this.delay);
    }

    stopAutoSlide() {
        clearInterval(this.autoSlideInterval);
    }

    showSlide(index) {
        if (index < 0) {
            this.currentSlideIndex = this.loop ? this.slides.length - 1 : 0;
        } else if (index >= this.slides.length) {
            this.currentSlideIndex = this.loop ? 0 : this.slides.length - 1;
        } else {
            this.currentSlideIndex = index;
        }

        this.slides.forEach((slide, i) => {
            slide.style.display = i === this.currentSlideIndex ? 'block' : 'none';
        });


        this.counter.textContent = `${this.currentSlideIndex + 1}/${this.slides.length}`;
    }

    nextSlide() {
        this.showSlide(this.currentSlideIndex + 1);
    }

    prevSlide() {
        this.showSlide(this.currentSlideIndex - 1);
    }

    updateNavVisibility() {
        if (!this.navs) {
            this.container.querySelectorAll('.slider-nav').forEach(nav => nav.style.display = 'none');
        }
        if (!this.pags) {
            this.counter.style.display = 'none';
        }

    }
}


const slider = new Slider(sliderSettings);
