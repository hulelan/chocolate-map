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

## Flavour map (`flavour-map.html`)

Bars placed on a flavour map laid out after the IICCT Flavour Projection map (four quadrants around Chocolatey), from their printed or published tasting notes (`Tasting notes (EN)`). The words that count as each point are `NODES` in the page. Click a point or a quadrant name to list the bars; `?bar=<id>` shows one bar's notes. `wheel.html`, the old tasting wheel, now redirects here.

## Makers (`makers.html`)

A bubble-and-line graph of what the IICCT Level 2 course said about chocolate makers. Orange bubbles are makers, teal ones are topics (cocoa butter, roasting, sourcing…); each line holds the notes linking them, and dashed yellow lines are makers the class compared directly. Click a maker for everything said about it, a topic to compare makers on it, or a line for the notes behind it; `?n=m:<maker>` or `?n=c:<topic>` opens one. The notes are `data/maker_facts.json` (paraphrased from the class transcripts, with recording, timestamp and speaker). A maker with bars in the collection links to them with `./?brand=<Brand>`.

## Favorites and black and white

The favorite makers are `FAVORITE_BRANDS` in `index.html` and `flavour-map.html`. The black-and-white version is `bw.css`, switched by `theme.js` and remembered per browser (`?bw=1` forces it). It changes the page around the map and the wheel, which both stay in colour.

## Updating the collection

1. Update `~/Desktop/chocolate_tasting/chocolate_collection.csv`.
2. Run `python3 scripts/build_collection.py` from the repo root. It writes `data/collection.json` and web-size photos to `collection/img` and `collection/thumb`.
3. Commit and push.

## Bars tried once

Bars I tasted once but don't own (the IICCT Level 2 course kit) are in `~/Desktop/chocolate_tasting/tried_once.json`, with the same fields as the spreadsheet plus `Course sample` and `Course notes`; their photos (maker or shop product photos, see `Photo source`) are in `~/Desktop/chocolate_tasting/tried_once_photos/<slug>/`. The build adds them with `"Status": "Tried once"`; the pages label them and have a "Tried once" filter.

The script re-encodes every photo, which drops all metadata. The original iPhone photos contain GPS coordinates, so never commit them.

Map coordinates are approximate: each bar's printed origin is matched to a farm, region or country (`PLACES` in the script). Bars with no printed origin are only in the table.

## Run locally

Serve the folder over http, for example `python3 -m http.server`, and open http://localhost:8000. Opening the pages as a file won't load the data.

## Pin sources

- [SOMA farms & origins](https://www.somachocolate.com/pages/farms-and-origins)
- [Castronovo Chocolate](https://www.castronovochocolate.com/)
- [BOHO Chocolate](https://bohochocolate.com/about)
- [Heirloom Cacao Preservation Fund](https://www.hcpcacao.org/)
