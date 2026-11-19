(function () {
  var root = document.documentElement, btn = document.getElementById("theme");
  function current() {
    return root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function label() { if (btn) btn.textContent = current() === "dark" ? "Light" : "Dark"; }
  label();
  if (btn) btn.addEventListener("click", function () {
    var n = current() === "dark" ? "light" : "dark";
    root.dataset.theme = n;
    try { localStorage.setItem("theme", n); } catch (e) {}
    label();
  });

  var bar = document.getElementById("progress");
  if (bar) {
    var upd = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + "%";
    };
    addEventListener("scroll", upd, { passive: true });
    addEventListener("resize", upd);
    upd();
  }

  var q = document.getElementById("q"), grid = document.getElementById("grid");
  if (q && grid) {
    var tag = "", cards = [].slice.call(grid.querySelectorAll(".card")), none = document.getElementById("none");
    var apply = function () {
      var s = q.value.trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var okTag = !tag || c.dataset.tags.split("|").indexOf(tag) > -1;
        var okQ = !s || c.dataset.text.indexOf(s) > -1;
        c.hidden = !(okTag && okQ);
        if (!c.hidden) shown++;
      });
      if (none) none.hidden = shown > 0 || !cards.length;
    };
    q.addEventListener("input", apply);
    [].forEach.call(document.querySelectorAll(".chip"), function (b) {
      b.addEventListener("click", function () {
        tag = b.dataset.tag;
        [].forEach.call(document.querySelectorAll(".chip"), function (x) { x.classList.toggle("on", x === b); });
        apply();
      });
    });
  }
})();
