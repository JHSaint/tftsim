"""Adds an `image` column to your unit CSV using unit-images.csv (matched by unit name).

Usage:  python add_images.py your-units.csv [unit-images.csv]
Writes: your-units-with-images.csv  (your original file is not changed)
"""
import csv, sys

src = sys.argv[1]
images = sys.argv[2] if len(sys.argv) > 2 else "unit-images.csv"
lookup = {r["name"].strip().lower(): r["image"] for r in csv.DictReader(open(images, encoding="utf-8-sig"))}
with open(src, encoding="utf-8-sig", newline="") as f:
    rdr = csv.DictReader(f)
    fields = list(rdr.fieldnames)
    rows = list(rdr)
if "image" not in fields:
    fields.append("image")
missing = []
for r in rows:
    url = lookup.get(r["name"].strip().lower(), "")
    if url:
        r["image"] = url
    elif not r.get("image"):
        missing.append(r["name"])
out = src.rsplit(".", 1)[0] + "-with-images.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {out} ({len(rows)} units).", f"No image for: {', '.join(missing)}" if missing else "All units matched.")
