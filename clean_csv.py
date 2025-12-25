import csv
from pathlib import Path

# bbox: (south, west, north, east)
MSK_BBOX = (55.4899, 37.3193, 56.0219, 38.0826)
SPB_BBOX = (59.7034, 29.4887, 60.2355, 30.9057)
MO_BBOX = (54.5, 35.1, 56.9, 40.4)

def in_bbox(lat, lon, bbox):
    s, w, n, e = bbox
    return s <= lat <= n and w <= lon <= e

def clean_accidents(in_csv, out_csv, bbox):
    src = Path(in_csv)
    dst = Path(out_csv)
    dst.parent.mkdir(exist_ok=True, parents=True)

    with src.open(encoding="utf-8") as f_in, dst.open("w", newline="", encoding="utf-8") as f_out:
        r = csv.DictReader(f_in)
        fieldnames = r.fieldnames
        w = csv.DictWriter(f_out, fieldnames=fieldnames)
        w.writeheader()

        kept = 0
        skipped = 0
        for row in r:
            try:
                lat = float(row["lat"])
                lon = float(row["lon"])
            except (ValueError, TypeError, KeyError):
                skipped += 1
                continue

            if not in_bbox(lat, lon, bbox):
                skipped += 1
                continue

            w.writerow(row)
            kept += 1

    print(f"{in_csv} -> {out_csv}: оставлено {kept}, выкинуто {skipped}")

if __name__ == "__main__":
    clean_accidents("./data/accidents_msk.csv", "data/accidents_msk_clean.csv", MSK_BBOX)
    clean_accidents("./data/accidents_spb.csv", "data/accidents_spb_clean.csv", SPB_BBOX)
    clean_accidents("./data/accidents_mo.csv",  "data/accidents_mo_clean.csv",  MO_BBOX)