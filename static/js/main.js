// Small enhancements. The site is fully readable without JavaScript.
(function () {
  "use strict";

  // Notebook viewer: expand / collapse every code cell at once.
  var toggle = document.querySelector("[data-nb-toggle]");
  if (toggle) {
    var cells = document.querySelectorAll(".nb-code");
    var sync = function () {
      var allOpen = Array.prototype.every.call(cells, function (d) { return d.open; });
      toggle.textContent = allOpen ? "Hide code" : "Show all code";
    };
    toggle.addEventListener("click", function () {
      var open = toggle.textContent !== "Hide code";
      cells.forEach(function (d) { d.open = open; });
      sync();
    });
    cells.forEach(function (d) { d.addEventListener("toggle", sync); });
    sync();
  }

  var dialog = document.getElementById("lightbox");
  if (!dialog || typeof dialog.showModal !== "function") return;
  var big = dialog.querySelector("img");
  document.querySelectorAll(".zoomable").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var img = btn.querySelector("img");
      big.src = img.src;
      big.alt = img.alt;
      dialog.showModal();
    });
  });
  dialog.querySelector(".lightbox-close").addEventListener("click", function () { dialog.close(); });
  dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
})();
