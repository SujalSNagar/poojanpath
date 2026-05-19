document.querySelectorAll(".custom-slider").forEach((slider) => {
  const desktopSlides = slider.dataset.desktop || 4;

  new Swiper(slider, {
    loop: true,

    slidesPerView: 2,

    spaceBetween: 16,

    navigation: {
      nextEl: slider.querySelector(".swiper-button-next"),
      prevEl: slider.querySelector(".swiper-button-prev"),
    },

    breakpoints: {
      576: {
        slidesPerView: 2,
      },

      768: {
        slidesPerView: 3,
      },

      992: {
        slidesPerView: 4,
      },

      1200: {
        slidesPerView: Number(desktopSlides),
      },
    },
  });
});

new Swiper(".promo-swiper", {
  loop: true,

  centeredSlides: true,

  slidesPerView: 1.2,

  spaceBetween: 16,
});

const samagriCarousel = document.querySelector("#samagriCarousel");

if (samagriCarousel) {
  new bootstrap.Carousel(samagriCarousel, {
    interval: 2000,

    ride: true,

    pause: false,

    wrap: true,
  });
}
