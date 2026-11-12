/* My IICCT flavour profile for a bar, drawn the way Seventy% draws it:
   the flavour map on top, the defect (off-flavour) map below (left out when no off-flavours were marked), one soft blob per
   attribute at its point on the map, blob area doubling with each intensity step (1-5).
   Points and colours follow the course's flavour map and defect map.
   Usage: profileSVG(r['My profile'], r['My off-flavours']) -> SVG markup string. */
(function () {
  // [name, x, y, colour or [top, bottom]] on a 1460 x 1040 map
  const UP = [["Cinnamon", 563, 128, "#efec4f"], ["Capsicum (dried)", 387, 183, "#eeec4f"], ["Dried leaves", 208, 307, "#efec4f"], ["Sour cherry", 726, 112, "#e4b671"], ["Geranium", 578, 263, "#aca435"], ["Jasmin", 414, 340, "#aca435"], ["Citrus", 725, 243, "#a4834e"], ["Cranberry", 890, 125, "#c0588f"], ["Raspberry", 1068, 177, "#c0578f"], ["Physalis", 1252, 298, "#c0578f"], ["Melon", 873, 262, "#91495f"], ["Guanabana", 1038, 335, "#91495f"], ["Strawberry", 1140, 513, ["#915c70", "#636c75"]], ["Blackberry", 1350, 513, ["#c977a7", "#7592b2"]], ["Banana", 725, 380, "#63502b"], ["Honey", 603, 417, "#665b25"], ["Lychee", 847, 416, "#5c392f"], ["Plum", 931, 515, "#554535"], ["Raisin", 847, 615, "#484637"], ["Rum", 725, 653, "#49482d"], ["Dairy", 603, 617, "#494923"], ["Almond", 518, 516, "#585122"], ["Chocolatey", 725, 515, "#433119"], ["Walnut", 111, 518, ["#e1e552", "#79b053"]], ["Hazelnut", 313, 517, ["#a39f34", "#647d3b"]], ["Coconut", 413, 697, "#567943"], ["Olive", 200, 733, "#5ea559"], ["Grassy", 578, 773, "#567943"], ["Woody", 384, 858, "#5ea559"], ["Loam", 561, 912, ["#83ac72", "#5ea559"]], ["Cocoa powder", 725, 792, "#54735b"], ["Coffee", 725, 927, ["#91b390", "#5ba17f"]], ["Winey", 1038, 695, "#526e72"], ["Mulberry", 1255, 730, "#5a94b1"], ["Prune", 873, 772, "#516e72"], ["Dark sugars", 1070, 858, "#5b93b1"], ["Molasses", 888, 912, ["#90b3af", "#5b94b2"]]];
  const DN = [["Petrol", 561, 108, "#276f0b"], ["Nut skins", 731, 93, "#22544a"], ["Cardboard", 898, 108, "#1c326c"], ["Plasticky", 381, 165, "#276f0b"], ["Dusty", 1080, 165, "#1b326c"], ["Rancid", 579, 254, "#33940e"], ["Lumber", 731, 233, "#2d6c4c"], ["Plaster", 880, 254, "#254290"], ["Rubber", 194, 294, "#276f0b"], ["Metallic", 1266, 294, "#1c326c"], ["Medicinal", 411, 332, "#33950e"], ["Dirt", 1050, 332, "#254290"], ["Biscuit", 731, 377, "#368760"], ["Ashy", 606, 415, "#3fb811"], ["Mouldy", 854, 415, "#2d53b4"], ["Sulphurous", 98, 517, ["#336f0b", "#7d7a11"]], ["Smokey", 309, 517, ["#42960d", "#a9a61b"]], ["Carbon", 519, 517, ["#52bc12", "#d4ce20"]], ["Fungal", 941, 517, ["#3b4da3", "#972431"]], ["Bouillon", 1151, 517, ["#2e3d80", "#771d27"]], ["Rust", 1362, 517, ["#242d64", "#5b1520"]], ["Acetic", 606, 620, "#f2d424"], ["Peaty", 731, 658, "#d1771f"], ["Overcooked meat", 854, 635, "#ab1c17"], ["Dried meat", 1050, 702, "#8b1513"], ["Sweaty", 411, 702, "#c2ab1d"], ["Vomit", 194, 740, "#918016"], ["Yeast extract", 1266, 740, "#68100e"], ["Rotting fruit", 579, 781, "#c2ab1d"], ["Compost", 731, 800, "#a36018"], ["Leather", 880, 781, "#8b1513"], ["Cheesey", 381, 871, "#918016"], ["Hammy", 1080, 871, "#68100e"], ["Faecal", 561, 925, "#918016"], ["Manure", 731, 941, "#7d4912"], ["Carrion", 898, 925, "#68100e"], ["Indistinct", 730, 517, "#7a5a3a"]];
  const QUP = [['HERBAL / SPICY', '#f1ec9f', 'start'], ['FRUITY', '#e7bfd6', 'end'], ['VEGETAL', '#cfe6da', 'start'], ['DARK SWEET', '#b9d8e6', 'end']];
  const QDN = [['CHEMICAL', '#b9c6ad', 'start'], ['MINERAL', '#b8bdd0', 'end'], ['BACTERIAL', '#d6e6c9', 'start'], ['ANIMAL', '#ddc0c0', 'end']];
  // Seventy% blob radius: 17px at intensity 1 on a 415px-wide chart, x sqrt(2) per step
  const radius = L => 17 * Math.pow(Math.SQRT2, Math.max(1, Math.min(5, L)) - 1) * 1460 / 415;
  let uid = 0;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function panel(points, quads, blobs, y0, id) {
    const byName = new Map(points.map(p => [p[0], p]));
    let s = '<g transform="translate(0,' + y0 + ')">';
    quads.forEach(([name, bg, anchor], q) => {
      const x = q % 2 ? 730 : 0, y = q < 2 ? 0 : 520;
      s += '<rect x="' + x + '" y="' + y + '" width="730" height="520" fill="' + bg + '"/>';
      s += '<text x="' + (q % 2 ? 1430 : 30) + '" y="' + (q < 2 ? 60 : 1000) + '" text-anchor="' + anchor + '" class="pq">' + name + '</text>';
    });
    for (const rx of [700, 520, 340]) s += '<ellipse cx="730" cy="520" rx="' + rx + '" ry="' + rx * 0.68 + '" fill="#fff" fill-opacity="0.18"/>';
    for (const [name, x, y] of points) {
      if (name === 'Indistinct') continue;
      s += '<circle cx="' + x + '" cy="' + y + '" r="46" fill="#fff" fill-opacity="0.35"/>';
      s += '<text x="' + x + '" y="' + (y + 8) + '" text-anchor="middle" class="pn">' + esc(name.replace(' (dried)', '')) + '</text>';
    }
    const list = (blobs || []).filter(b => byName.has(b[0])).sort((a, b) => b[1] - a[1]);   // big ones underneath
    for (const [name, L] of list) {
      const [, x, y, col] = byName.get(name), r = radius(L);
      let fill = col;
      if (Array.isArray(col)) {
        const g = 'pg' + id + '-' + (uid++);
        s += '<defs><linearGradient id="' + g + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0.3" stop-color="' + col[0] + '"/><stop offset="0.7" stop-color="' + col[1] + '"/></linearGradient></defs>';
        fill = 'url(#' + g + ')';
      }
      s += '<circle cx="' + x + '" cy="' + y + '" r="' + r.toFixed(0) + '" fill="' + fill + '" fill-opacity="0.9" filter="url(#pblur' + id + ')"><title>' + esc(name) + ' · ' + L + '/5</title></circle>';
    }
    for (const [name, L] of list) {
      const [, x, y] = byName.get(name);
      s += '<text x="' + x + '" y="' + (y + 10 + L * 3) + '" text-anchor="middle" class="pb" style="font-size:' + (26 + L * 8) + 'px">' + esc(name.replace(' (dried)', '')) + '</text>';
    }
    return s + '</g>';
  }

  window.profileSVG = function (flavour, off) {
    const id = uid++;
    const hasOff = (off || []).length;
    return '<svg class="profile-svg" viewBox="0 0 1460 ' + (hasOff ? 2090 : 1040) + '" role="img" aria-label="Flavour profile: ' +
      esc((flavour || []).map(b => b[0] + ' ' + b[1]).concat((off || []).map(b => b[0] + ' ' + b[1])).join(', ') || 'none') + '">' +
      '<defs><filter id="pblur' + id + '" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter></defs>' +
      '<style>.pq{font:600 34px system-ui,sans-serif;fill:#000;fill-opacity:.35;letter-spacing:1px}.pn{font:22px system-ui,sans-serif;fill:#000;fill-opacity:.4}.pb{font-family:system-ui,sans-serif;font-weight:600;fill:#fff;paint-order:stroke;stroke:#000;stroke-opacity:.25;stroke-width:3px}</style>' +
      panel(UP, QUP, flavour, 0, id) + (hasOff ? panel(DN, QDN, off, 1050, id) : '') + '</svg>';
  };
  // Plain-text version, e.g. "Honey 5, Raisin 4, Citrus 3"
  window.profileText = list => (list || []).slice().sort((a, b) => b[1] - a[1]).map(b => b[0] + ' ' + b[1]).join(', ');
})();
