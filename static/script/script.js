const warpper = document.querySelector("warpper");
const diplayPage = document.querySelector(".reg-btn");

displayPage.addEventListener("click", () => {
  warpper.classList.add("active");
});

homePage.addEventListener("click", () => {
  warpper.classList.remove("active");
});
