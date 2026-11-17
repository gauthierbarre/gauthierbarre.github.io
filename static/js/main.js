// Figure lightbox. The site is fully readable without JavaScript.
(function () {
  "use strict";
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
