from flask import Flask, render_template, jsonify, abort
import csv
import os
import random

app = Flask(__name__)

DATA_DIR = "data"

MAX_POINTS = {
    "wifi": 1000,
    "bicycle": 4000,
    "accidents_msk": 1000,
    "accidents_spb": 1000,
    "accidents_mo": 1000,
}

DATASETS = {
    "wifi": "wifi.csv",
    "bicycle": "bicycle.csv",
    "accidents_msk": "accidents_msk_clean.csv",
    "accidents_spb": "accidents_spb_clean.csv",
    "accidents_mo": "accidents_mo_clean.csv",
}


def load_csv(dataset_name):
    filename = DATASETS.get(dataset_name)
    if not filename:
        abort(404, "Unknown dataset")

    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        abort(404, f"File {filename} not found")

    heat = []
    points = []

    max_points = MAX_POINTS.get(dataset_name, None)

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        rows = list(reader)
        if max_points and len(rows) > max_points:
            rows = random.sample(rows, max_points)

        for row in rows:
            try:
                lat = float(row["lat"])
                lon = float(row["lon"])
            except (KeyError, ValueError):
                continue

            value = float(row.get("value", 1) or 1)
            name = row.get("name", "").strip()

            heat.append([lat, lon, value])
            points.append({
                "lat": lat,
                "lon": lon,
                "name": name,
                "value": value,
            })

    return {"heat": heat, "points": points}


@app.route("/")
def index():
    return render_template("index.html",
                           start_lat=55.751244,
                           start_lon=37.618423,
                           start_zoom=10)


@app.route("/api/data/<dataset>")
def api_data(dataset):
    if dataset not in DATASETS:
        abort(404, "Unknown dataset")
    data = load_csv(dataset)
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)
