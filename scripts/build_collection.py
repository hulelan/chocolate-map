# Builds the "My collection" data for the site from the chocolate_collection spreadsheet:
#   data/collection.json         one record per physical bar, with map coordinates
#   collection/img/*.jpg         web-size photos (metadata stripped — originals carry GPS)
#   collection/thumb/*.jpg       thumbnails
# Run: python3 scripts/build_collection.py  (from the repo root)
import csv, json, os, re, sys, unicodedata
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_CSV = os.path.expanduser("~/Desktop/chocolate_tasting/chocolate_collection.csv")
IMG_DIR, THUMB_DIR = os.path.join(ROOT, "collection/img"), os.path.join(ROOT, "collection/thumb")

# Approximate origin coordinates. First match wins, so specific places come before regions and countries.
# (keyword(s) searched in country/region/locality/origin text, lat, lng, place label, precision)
PLACES = [
    # Venezuela
    (["chuao"], 10.49, -67.53, "Chuao, Aragua, Venezuela", "village"),
    (["patanemo"], 10.48, -67.93, "Patanemo, Carabobo, Venezuela", "village"),
    (["mantuano"], 10.25, -67.95, "Carabobo, Venezuela", "region"),
    (["trinchera"], 10.30, -68.07, "Las Trincheras, Carabobo, Venezuela", "village"),
    (["urrutia", "barlovento", "carenero"], 10.30, -66.10, "Barlovento, Miranda, Venezuela", "region"),
    (["piaroa"], 6.20, -66.60, "Estado Bolívar, Venezuela", "region"),
    (["perijá", "perija"], 10.33, -72.32, "Rosario de Perijá, Zulia, Venezuela", "region"),
    (["táchira", "tachira", "morusca"], 8.03, -72.26, "Colón, Táchira, Venezuela", "region"),
    (["chama"], 8.90, -71.80, "South of Lake Maracaibo, Venezuela", "region"),
    (["zulia"], 9.00, -71.90, "South of Lake Maracaibo, Zulia, Venezuela", "region"),
    (["hacienda san josé", "hacienda san jose"], 10.62, -63.10, "Hacienda San José, Paria, Sucre, Venezuela", "farm"),
    # Colombia
    (["tumaco"], 1.80, -78.76, "Tumaco, Nariño, Colombia", "region"),
    (["sierra nevada", "arhuaco", "katansama"], 10.80, -73.65, "Sierra Nevada de Santa Marta, Colombia", "region"),
    (["gigante", "huila"], 2.39, -75.55, "Gigante, Huila, Colombia", "village"),
    (["fuente de oro", "el jardín", "el jardin"], 3.46, -73.62, "Fuente de Oro, Meta, Colombia", "village"),
    # Peru
    (["salitral"], -5.34, -79.83, "Salitral, Morropón, Piura, Peru", "village"),
    (["morropón", "morropon"], -5.19, -79.97, "Morropón, Piura, Peru", "village"),
    (["bigote"], -5.32, -79.79, "San Juan de Bigote, Piura, Peru", "village"),
    (["chulucanas"], -5.09, -80.16, "Chulucanas, Piura, Peru", "village"),
    (["sechura", "pulache"], -5.40, -80.30, "Piura (Sechura valley), Peru", "region"),
    (["alto piura", "quemazon"], -5.45, -79.75, "Alto Piura valley, Piura, Peru", "region"),
    (["piura"], -5.20, -80.00, "Piura, Peru", "region"),
    (["awajún", "awajun", "huambisa"], -4.60, -77.90, "Condorcanqui, Amazonas, Peru", "region"),
    (["bagua"], -5.64, -78.53, "Bagua, Amazonas, Peru", "region"),
    (["la mar", "ayacucho"], -12.90, -73.90, "La Mar, Ayacucho, Peru", "region"),
    (["san ignacio"], -5.15, -79.00, "San Ignacio, Cajamarca, Peru", "region"),
    (["echarate"], -12.77, -72.58, "Echarate, La Convención, Cusco, Peru", "village"),
    (["santa ana", "quillabamba", "la convención", "la convencion"], -12.87, -72.69, "Quillabamba, La Convención, Cusco, Peru", "region"),
    (["qori warmi", "vraem"], -12.50, -73.80, "VRAEM, Cusco, Peru", "region"),
    (["don maximo", "cusco", "cuzco"], -12.85, -72.70, "Cusco region, Peru", "region"),
    (["pangoa", "junín", "junin"], -11.43, -74.49, "Pangoa, Junín, Peru", "region"),
    (["curimaná", "curimana"], -8.43, -75.15, "Curimaná, Ucayali, Peru", "village"),
    (["ucayali", "pucallpa"], -8.38, -74.55, "Ucayali, Peru", "region"),
    # Ecuador
    (["camino verde", "durán", "duran"], -2.17, -79.82, "Camino Verde, Guayas, Ecuador", "farm"),
    (["costa esmeraldas", "salazar", "tonchigüe"], 0.87, -79.95, "Costa Esmeraldas, Esmeraldas, Ecuador", "farm"),
    (["esmeraldas"], 0.95, -79.65, "Esmeraldas, Ecuador", "region"),
    (["hacienda victoria"], -1.80, -79.60, "Hacienda Victoria, Ecuador", "farm"),
    # Caribbean & Central America
    (["zorzal"], 19.10, -70.05, "Zorzal Reserve, Duarte, Dominican Republic", "farm"),
    (["öko", "oko caribe", "oko-caribe", "anconès", "ancones", "macorís", "macoris"], 19.30, -70.25, "San Francisco de Macorís, Dominican Republic", "region"),
    (["el jobo", "puerto plata"], 19.60, -70.80, "Puerto Plata, Dominican Republic", "region"),
    (["l'esterre", "st andrew"], 12.13, -61.64, "L'Esterre Estate, St Andrew, Grenada", "farm"),
    (["rio claro"], 10.30, -61.18, "Rio Claro, Trinidad", "village"),
    (["cap-haïtien", "cap-haitien", "pisa", "haiti"], 19.76, -72.20, "Cap-Haïtien, Haiti", "region"),
    (["bachelor"], 17.95, -76.45, "St Thomas Parish, Jamaica", "region"),
    (["aguada"], 18.38, -67.19, "Aguada, Puerto Rico", "village"),
    (["puerto rico"], 18.30, -66.60, "Puerto Rico", "country"),
    (["guatuso"], 10.67, -84.82, "Guatuso, Costa Rica", "region"),
    (["lanquín", "lanquin", "la laguna"], 15.58, -89.98, "Lanquín, Alta Verapaz, Guatemala", "village"),
    (["polochic", "alta verapaz"], 15.37, -89.70, "Polochic Valley, Guatemala", "region"),
    (["maya mountain", "toledo"], 16.25, -88.95, "Maya Mountain, Toledo, Belize", "region"),
    (["waslala", "bosawas"], 13.33, -85.37, "Waslala, Nicaragua", "region"),
    (["honduras", "yojoa"], 14.87, -87.98, "Lake Yojoa, Honduras", "region"),
    # Mexico
    (["lacandon"], 16.13, -91.30, "Selva Lacandona, Chiapas, Mexico", "region"),
    (["ostuacán", "ostuacan", "selva zoque"], 17.40, -93.30, "Ostuacán, Chiapas, Mexico", "region"),
    (["jabalí", "jabali"], 17.30, -92.50, "Northern Chiapas, Mexico", "region"),
    (["huehuetán", "huehuetan"], 15.02, -92.38, "Huehuetán, Chiapas, Mexico", "village"),
    (["tuxtla chico"], 14.94, -92.17, "Tuxtla Chico, Chiapas, Mexico", "village"),
    (["tapachula", "soconusco", "xoconusco", "mokaya", "rayen"], 14.90, -92.26, "Soconusco, Chiapas, Mexico", "region"),
    (["comalcalco", "arroyo hondo"], 18.26, -93.22, "Comalcalco, Tabasco, Mexico", "region"),
    (["chontalpa", "tabasco"], 18.00, -93.20, "La Chontalpa, Tabasco, Mexico", "region"),
    (["chiapas"], 16.50, -92.60, "Chiapas, Mexico", "region"),
    (["oaxaca"], 17.06, -96.72, "Oaxaca, Mexico", "region"),
    # Africa
    (["sambirano", "bejofo", "ambanja", "akesson"], -13.70, 48.45, "Sambirano Valley, Madagascar", "region"),
    (["kokoa kamili", "kilombero", "mbingu"], -8.20, 36.40, "Kilombero Valley, Tanzania", "region"),
    (["semuliki", "bundibugyo"], 0.75, 30.10, "Bundibugyo, Uganda", "region"),
    (["mirasa"], 6.70, -1.60, "South-central Ghana", "region"),
    (["aponoapono", "biakoye"], 7.20, 0.35, "Biakoye, Volta, Ghana", "region"),
    # Asia & Pacific
    (["kablon", "south cotabato"], 6.33, 124.95, "Tupi, South Cotabato, Philippines", "farm"),
    (["bến tre", "ben tre", "bén tre"], 10.24, 106.38, "Bến Tre, Vietnam", "region"),
    (["tiền giang", "tien giang"], 10.36, 106.36, "Tiền Giang, Vietnam", "region"),
    (["anamalai"], 10.40, 76.95, "Anamalai Hills, India", "region"),
    (["idukki"], 9.85, 76.97, "Idukki, Kerala, India", "region"),
    (["java"], -7.60, 110.20, "Java, Indonesia", "region"),
    (["kelantan"], 5.30, 102.00, "Kelantan, Malaysia", "region"),
    (["chiang mai"], 18.79, 98.98, "Chiang Mai, Thailand", "region"),
    (["chumphon"], 10.49, 99.18, "Chumphon, Thailand", "region"),
    (["prachuap"], 11.81, 99.80, "Prachuap Khiri Khan, Thailand", "region"),
    (["pingtung"], 22.55, 120.55, "Pingtung, Taiwan", "region"),
    (["malekula"], -16.20, 167.50, "Malekula Island, Vanuatu", "region"),
    (["kauai", "kapa'a"], 22.08, -159.32, "Kapaʻa, Kauaʻi, Hawaii", "farm"),
    (["hilo"], 19.72, -155.08, "Hilo, Hawaiʻi", "region"),
    (["oahu", "mapele"], 21.60, -158.05, "Oʻahu, Hawaii", "region"),
    (["alto beni"], -15.50, -67.30, "Alto Beni, Bolivia", "region"),
    (["ilhéus", "ilheus", "riachuelo"], -14.79, -39.05, "Ilhéus, Bahia, Brazil", "region"),
]
COUNTRIES = {  # fallback: country centroid
    "venezuela": (7.5, -66.0), "colombia": (4.5, -74.0), "peru": (-9.5, -75.0), "ecuador": (-1.5, -78.5),
    "dominican republic": (18.9, -70.4), "nicaragua": (12.9, -85.2), "belize": (17.2, -88.6), "guatemala": (15.5, -90.3),
    "mexico": (23.0, -102.0), "bolivia": (-16.3, -64.5), "brazil": (-10.0, -52.0), "madagascar": (-19.0, 46.7),
    "tanzania": (-6.4, 34.9), "uganda": (1.3, 32.3), "ghana": (7.9, -1.0), "philippines": (12.0, 122.0),
    "vietnam": (14.1, 108.3), "india": (21.0, 78.0), "indonesia": (-2.5, 118.0), "thailand": (15.5, 101.0),
    "sri lanka": (7.6, 80.7), "trinidad": (10.45, -61.3), "grenada": (12.1, -61.7), "jamaica": (18.1, -77.3),
    "haiti": (19.0, -72.3), "costa rica": (9.9, -84.1), "taiwan": (23.7, 121.0), "malaysia": (4.2, 102.0),
    "vanuatu": (-15.4, 166.9), "honduras": (14.9, -87.98),
}

def norm_name(f): return re.sub(r"[^A-Za-z0-9_.-]+", "_", f)

def locate(rec):
    text = " ".join(rec.get(k, "") for k in ["Cacao origin: Country", "Cacao origin: Region", "Cacao origin: Locality / Farm", "Cacao origin (verbatim)", "Bar name"]).lower()
    country = rec.get("Cacao origin: Country", "").lower()
    for keys, lat, lng, label, prec in PLACES:
        if any(k in text for k in keys): return lat, lng, label, prec
    for c, (lat, lng) in COUNTRIES.items():
        if c in country: return lat, lng, c.title(), "country"
    return None

COUNTRY_FIX = {"usa": "USA (Hawaii)", "trinidad": "Trinidad and Tobago", "puerto rico": "Puerto Rico"}
def clean_country(c):
    c = re.sub(r"\s*\(.*?\)\s*", " ", c).strip()   # drop "(inferred …)" style notes
    for k, v in COUNTRY_FIX.items():
        if c.lower().startswith(k): return v
    return "Blend" if c.lower() == "blend" else c

def web_copy(src, name):
    out, th = os.path.join(IMG_DIR, name), os.path.join(THUMB_DIR, name)
    if os.path.exists(out) and os.path.exists(th): return
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")   # re-encoding without exif drops GPS & all metadata
    big = im.copy(); big.thumbnail((1400, 1400)); big.save(out, "JPEG", quality=78, optimize=True, progressive=True)
    sm = im.copy(); sm.thumbnail((360, 360)); sm.save(th, "JPEG", quality=75, optimize=True)

def main():
    os.makedirs(IMG_DIR, exist_ok=True); os.makedirs(THUMB_DIR, exist_ok=True)
    rows = list(csv.DictReader(open(SRC_CSV, encoding="utf-8-sig")))
    out, unplaced = [], []
    for r in rows:
        best = r["Best photo"].replace(" (NOT FOUND)", "")
        folder = os.path.dirname(best)
        photos = [os.path.basename(best)] + [p.strip() for p in r["Accessory photos"].split(",") if p.strip()]
        names = []
        for p in photos:
            src = os.path.join(folder, p)
            if not os.path.exists(src):
                for d in ["chocolate_collection2", "chocolate_collection3"]:
                    alt = os.path.expanduser(f"~/Desktop/chocolate_tasting/{d}/{p}")
                    if os.path.exists(alt): src = alt; break
            n = norm_name(os.path.splitext(p)[0]) + ".jpg"
            web_copy(src, n); names.append(n)
        loc = locate(r)
        rec = {k: v for k, v in r.items() if k not in ("Best photo", "Accessory photos", "Instance ID") and v != ""}
        rec["id"] = r["Instance ID"]; rec["photos"] = names
        rec["country"] = clean_country(r.get("Cacao origin: Country", ""))
        if loc: rec["lat"], rec["lng"], rec["place"], rec["precision"] = loc
        else: unplaced.append(f'{r["Brand"]} | {r["Bar name"]}')
        out.append(rec)
    json.dump(out, open(os.path.join(ROOT, "data/collection.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(out), "records;", len(out) - len(unplaced), "mapped;", len({(o.get('lat'), o.get('lng')) for o in out if 'lat' in o}), "map points")
    print("no origin pin:", *unplaced, sep="\n  ")

if __name__ == "__main__":
    main()
