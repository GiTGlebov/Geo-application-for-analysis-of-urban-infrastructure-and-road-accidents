import json
import csv
from pathlib import Path


def convert_accidents(in_path, out_path):
    """
    Конвертирует в CSV формата lat,lon,name,value
    """
    in_path = Path(in_path)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open(encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        records = data
    elif isinstance(data, dict) and "features" in data:
        records = [feat.get("properties", {}) for feat in data["features"]]
    else:
        raise RuntimeError("Неизвестный формат файла")

    with out_path.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["lat", "lon", "name", "value"])

        count = 0
        for rec in records:
            point = rec.get("point", {})
            lat = point.get("lat")
            lon = point.get("long")
            if lat is None or lon is None:
                continue

            addr = rec.get("address", "")
            cat = rec.get("category", "")
            dt  = rec.get("datetime", "")
            sev = rec.get("severity", "")
            dead = rec.get("dead_count", 0) or 0
            inj  = rec.get("injured_count", 0) or 0

            name_parts = []
            if addr: name_parts.append(addr)
            if cat:  name_parts.append(cat)
            if dt:   name_parts.append(dt)
            if sev:  name_parts.append(f"Тяжесть: {sev}")
            if dead or inj:
                name_parts.append(f"Погибших: {dead}, Раненых: {inj}")

            name = " | ".join(name_parts) if name_parts else "ДТП"

            severity_map = {
                "Легкий": 1,
                "Средний": 2,
                "Тяжкий": 3,
                "С погибшими": 4,
            }
            value = severity_map.get(sev, 1) + dead * 3 + inj * 1

            writer.writerow([lat, lon, name, value])
            count += 1

    print(f"✓ {out_path} готов ({count} точек)")


if __name__ == "__main__":
    convert_accidents("moskva.geojson", "data/accidents_msk.csv")
    convert_accidents("sankt-peterburg.geojson",   "data/accidents_spb.csv")
    convert_accidents("moskovskaia-oblast.geojson",   "data/accidents_mo.csv")

    
