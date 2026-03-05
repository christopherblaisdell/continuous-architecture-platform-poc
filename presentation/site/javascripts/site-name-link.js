document.addEventListener("DOMContentLoaded", function () {
  var title = document.querySelector(".md-header__title");
  if (!title) return;
  title.style.cursor = "pointer";
  title.addEventListener("click", function () {
    var logo = document.querySelector("a.md-header__button.md-logo");
    if (logo) window.location.href = logo.href;
  });
});
