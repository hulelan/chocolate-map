# Cacao Map

A map of cacao farms and chocolate makers, and a table of the bars in my collection.

Live at https://cacaomap.com

## Map (`map.html`)

- Green pins are farms, orange pins are makers. Both come from `data/pins.json`; edit that file to add, change or remove one.
- Brown numbered squares are origins of bars in my collection. The number is how many bars come from there.
- A farm pin links to the bars in the collection from that origin; a maker pin links to that maker's bars.
  The matching is done by `PIN_ORIGIN_KEYS` and `PIN_BRANDS` in `scripts/build_collection.py`.

## Collection table (`index.html`, the home page)

One row per bar, most copies first, with the same columns as `chocolatelist_processed.xlsx`; the Copies column counts copies owned. Each column header has a filter menu. Click a row for photos and all fields.

URL parameters: `?bar=<id>` opens a bar (on the map, it puts that bar and its farm and maker pins at the top of the sidebar), `?place=<map place>` filters to a collection origin, `?pin=<pin id>` filters to the bars linked to a map pin.

`collection.html` redirects to the home page so old links keep working.

## Tasting wheel (`wheel.html`)

Bars placed on a flavour wheel from their printed tasting notes (`Tasting notes (EN)`). The word lists for each note are `WHEEL` in the page. Click a segment to list the bars; `?bar=<id>` shows one bar's notes.

## Favorites and black and white

The favorite makers are `FAVORITE_BRANDS` in `index.html` and `wheel.html`. The black-and-white version is `bw.css`, switched by `theme.js` and remembered per browser (`?bw=1` forces it). It changes the page around the map and the wheel, which both stay in colour.

## Updating the collection

1. Update `~/Desktop/chocolate_tasting/chocolate_collection.csv`.
2. Run `python3 scripts/build_collection.py` from the repo root. It writes `data/collection.json` and web-size photos to `collection/img` and `collection/thumb`.
3. Commit and push.

The script re-encodes every photo, which drops all metadata. The original iPhone photos contain GPS coordinates, so never commit them.

Map coordinates are approximate: each bar's printed origin is matched to a farm, region or country (`PLACES` in the script). Bars with no printed origin are only in the table.

## Run locally

Serve the folder over http, for example `python3 -m http.server`, and open http://localhost:8000. Opening the pages as a file won't load the data.

## Pin sources

- [SOMA farms & origins](https://www.somachocolate.com/pages/farms-and-origins)
- [Castronovo Chocolate](https://www.castronovochocolate.com/)
- [BOHO Chocolate](https://bohochocolate.com/about)
- [Heirloom Cacao Preservation Fund](https://www.hcpcacao.org/)
