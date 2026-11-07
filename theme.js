// Black-and-white version: a per-browser choice, applied before the page draws
(function () {
  var bw = false;
  try { bw = localStorage.getItem('cacao-theme') === 'bw'; } catch (e) {}
  if (/[?&]bw=1/.test(location.search)) bw = true;
  if (bw) document.documentElement.classList.add('bw');
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
      b.textContent = bw ? 'Colour' : 'Black & white';
      b.onclick = function () {
        try { localStorage.setItem('cacao-theme', bw ? 'colour' : 'bw'); } catch (e) {}
        var u = new URL(location.href); u.searchParams.delete('bw'); location.replace(u);
      };
    });
  });
})();
