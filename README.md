# Cacao Map

A map of cacao farms and chocolate makers, and a table of the bars in my collection.

Live at https://cacaomap.com

## Map (`index.html`)

- Green pins are farms, orange pins are makers. Both come from `data/pins.json`; edit that file to add, change or remove one.
- Brown numbered squares are origins of bars in my collection. The number is how many bars come from there.
- A farm pin links to the bars in the collection from that origin; a maker pin links to that maker's bars.
  The matching is done by `PIN_ORIGIN_KEYS` and `PIN_BRANDS` in `scripts/build_collection.py`.

## Collection table (`collection.html`)

Every bar, with the same columns as `chocolatelist_processed.xlsx`. Each column header has a filter menu.
"One row per bar" groups copies of the same bar. Click a row for photos and all fields.

URL parameters: `?bar=<id>` opens a bar, `?place=<map place>` filters to a collection origin, `?pin=<pin id>` filters to the bars linked to a map pin.

## Updating the collection

1. Update `~/Desktop/chocolate_tasting/chocolate_collection.csv`.
2. Run `python3 scripts/build_collection.py` from the repo root. It writes `data/collection.json` and web-size photos to `collection/img` and `collection/thumb`.
3. Commit and push.

The script re-encodes every photo, which drops all metadata. The original iPhone photos contain GPS coordinates, so never commit them.

Map coordinates are approximate: each bar's printed origin is matched to a farm, region or country (`PLACES` in the script). Bars with no printed origin are only in the table.

## Run locally

Serve the folder over http, for example `python3 -m http.server`, and open http://localhost:8000. Opening `index.html` as a file won't load the data.

## Pin sources

- [SOMA farms & origins](https://www.somachocolate.com/pages/farms-and-origins)
- [Castronovo Chocolate](https://www.castronovochocolate.com/)
- [BOHO Chocolate](https://bohochocolate.com/about)
- [Heirloom Cacao Preservation Fund](https://www.hcpcacao.org/)
