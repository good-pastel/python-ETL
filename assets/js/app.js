const button = document.querySelector(".mobile-menu-button");
const menu = document.querySelector(".mobile-menu");
const icon = button.querySelector("i");

button.addEventListener("click", () => {
  menu.classList.toggle("active");

  button.classList.toggle("active");

  icon.classList.toggle("ti-menu-2");
  icon.classList.toggle("ti-x");
});
/*======================================
        API DOCUMENTATION
======================================*/

const apiButtons = document.querySelectorAll(".toggle-details");

apiButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const card = button.closest(".feature-api-card");

    const detail = card.querySelector(".api-details");

    const icon = button.querySelector("i");

    card.classList.toggle("opened");

    detail.classList.toggle("opened");

    if (detail.classList.contains("opened")) {
      button.childNodes[0].nodeValue = `${button.dataset.labelOpen || "Hide Details"} `;

      icon.classList.remove("ti-chevron-down");

      icon.classList.add("ti-chevron-up");
    } else {
      button.childNodes[0].nodeValue = `${button.dataset.labelClosed || "View Details"} `;

      icon.classList.remove("ti-chevron-up");

      icon.classList.add("ti-chevron-down");
    }
  });
});
