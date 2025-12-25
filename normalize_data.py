import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)

# 1) WiFi:
wifi = pd.read_csv("wifi.csv", sep="|", header=None, names=["lat","lon","name"])
wifi["value"] = 1
wifi.to_csv("data/wifi.csv", index=False)

# 2) Велосипеды:
bike = pd.read_csv("bicycle.csv")
bike.columns = ["lat","lon","name"]
bike["value"] = 1
bike.to_csv("data/bicycle.csv", index=False)

print("OK: data/wifi.csv и data/bicycle.csv готовы")
