(function () {
  'use strict';

  window.addEventListener("load", () => {
    const menuLink = document.querySelector(".menu-link");
    const menuBody = document.querySelector(".menu-body");
    document.body.addEventListener("click", e => {
      console.log(e.target);
      if (e.target !== menuLink && e.target !== menuBody) {
        menuBody.classList.add("hidden");
      }
    }, true);
    menuLink.addEventListener("click", () => {
      if (menuBody.classList.contains("hidden")) {
        menuBody.classList.remove("hidden");
      } else {
        menuBody.classList.add("hidden");
      }
    });
  });

})();
