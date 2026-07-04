# 🍫 Chocolate Map

A personal, zoomable world map for taking notes on cacao farms and chocolate facilities.

**Live site:** https://hulelan.github.io/chocolate-map/

## Features

- Zoomable world map (Leaflet + OpenStreetMap — no API key, no billing).
- Click anywhere to drop a pin; tag it **Farm** or **Facility**, add a name and notes.
- Sidebar list with text search and type filters.
- Everything saves to your browser's local storage (`localStorage`).
- **Export / Import** your pins as JSON for backup or moving between devices.

## Your data & privacy

Pins you create are stored **only in your own browser**, not in this repository or on any
server. This public repo contains just the app code and a starter set of researched pins.
Export a JSON backup periodically if the notes matter to you.

## Starter pins

Seeded from public research on chocolate makers and their sourcing:

- **Makers/facilities:** Castronovo Chocolate (Stuart, FL), BOHO Chocolate (Florence, MA),
  SOMA Chocolatemaker (Toronto).
- **Origins/farms:** Soma's ~20-country origin list, Castronovo's Sierra Nevada de Santa Marta
  (Colombia) & Tumaco, BOHO's Kablon Farms, plus several HCP-designated heirloom farms.

Coordinates are region-level approximations and every pin is editable. Verify HCP designation
numbers against the [HCP interactive globe](https://www.hcpcacao.org/our-heirloom-farmers.html).

## Run locally

Just open `index.html` in any browser. No build step, no dependencies to install.

## Sources

- [SOMA farms & origins](https://www.somachocolate.com/pages/farms-and-origins)
- [Castronovo Chocolate](https://www.castronovochocolate.com/)
- [BOHO Chocolate](https://bohochocolate.com/about)
- [Heirloom Cacao Preservation Fund](https://www.hcpcacao.org/)
