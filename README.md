# 🍫 Chocolate Map

A zoomable, satellite world map of cacao farms and chocolate facilities — part shared
community map, part personal notebook.

**Live site:** https://hulelan.github.io/chocolate-map/

## Features

- **Satellite + terrain basemaps** (Esri imagery with a roads/labels overlay, plus Streets
  and Terrain) via a layer switcher — no API key. Deep zoom past native resolution.
- **Community pins** — a shared, curated set everyone sees (stored in `data/pins.json`).
- **Suggest a place** — any visitor can propose a pin; it opens a pre-filled GitHub issue.
  The maintainer approves before it appears (see below).
- **Private pins** — anyone can drop pins saved only in their own browser (`localStorage`),
  with full-page Markdown notes, photos, and a draggable satellite mini-map.
- **Full-page pin view** at `#/pin/<id>` with shareable URLs.
- Optional **Mapbox HD satellite** if you paste a free token (🛰 HD key button).

## How suggestions & approval work

1. A visitor clicks **“Suggest a place for everyone,”** picks the exact spot on the map,
   and fills a short form. This opens a **pre-filled GitHub issue** (a free GitHub account
   is required to post — a natural spam barrier).
2. The maintainer reviews the issue at
   [Issues](https://github.com/hulelan/chocolate-map/issues).
3. To publish, the maintainer adds the **`approved`** label. That's the only manual step.
4. The [`Approve suggestion`](.github/workflows/approve-suggestion.yml) GitHub Action then:
   - parses and validates the suggestion (name, type, in-range coordinates, no duplicates),
   - appends a clean pin to `data/pins.json`,
   - commits, and closes the issue with a confirmation comment.
5. GitHub Pages rebuilds and the pin appears for everyone within ~1 minute.

Nothing is published without the maintainer's label. Invalid or duplicate suggestions are
rejected with an explanatory comment instead of being added.

### Maintainer notes

- Edit or remove a community pin by editing `data/pins.json` directly and committing.
- The Action needs write access to push. It declares `permissions: contents: write` in the
  workflow. If a run ever fails to push, enable **Settings → Actions → General → Workflow
  permissions → “Read and write permissions.”**

## Email notifications

Two ways to get emailed when a suggestion arrives:

1. **Built-in (zero setup).** As the repo owner you're watching the repo, so GitHub emails
   you on every new issue. Check **github.com → your avatar → Settings → Notifications** and
   make sure email is enabled. This works today.
2. **Custom branded email** via [`notify-suggestion.yml`](.github/workflows/notify-suggestion.yml).
   It stays dormant until you add these repo secrets under
   **Settings → Secrets and variables → Actions → New repository secret**:

   | Secret | Example |
   |---|---|
   | `MAIL_SERVER` | `smtp.gmail.com` |
   | `MAIL_PORT` | `465` |
   | `MAIL_USERNAME` | `you@gmail.com` |
   | `MAIL_PASSWORD` | a Gmail **App Password** (not your login password) |
   | `MAIL_TO` | `lelan@lelanhu.com` |

   For Gmail/Workspace, create an App Password at
   [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) (requires
   2-step verification). For another provider, use its SMTP host/port and credentials.

## Address search

The sidebar's **🔎 Find a place** box geocodes towns/addresses via OpenStreetMap Nominatim
(no key). Pick a result to fly there, then add a private pin or start a suggestion at that
spot. Business names are hit-or-miss in OSM; towns and addresses work best.

## Data & privacy

- **Community pins** live in `data/pins.json` in this public repo.
- **Private pins/notes/photos** live only in each visitor's browser and are never uploaded.
  Use **⬇ Export mine** for a backup; **⬆ Import** to restore.

## Run locally

Open `index.html` in any browser. (When opened as a local file it falls back to a small
built-in pin set, since browsers block reading `data/pins.json` over `file://`. Served over
http — like GitHub Pages — it loads the full shared set.)

## Sources for the starter pins

- [SOMA farms & origins](https://www.somachocolate.com/pages/farms-and-origins)
- [Castronovo Chocolate](https://www.castronovochocolate.com/)
- [BOHO Chocolate](https://bohochocolate.com/about)
- [Heirloom Cacao Preservation Fund](https://www.hcpcacao.org/)
