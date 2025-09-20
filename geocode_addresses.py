
import pandas as pd
import requests
import time

API_KEY = "AIzaSyB6x8GDQuIXw2vXcinTHeMQUT2S84N3kY4"  # החלף במפתח שלך
INPUT_FILE = "holon_trees.xlsx"  # שם הקובץ עם הכתובות
OUTPUT_FILE = "holon_trees_geocoded.xlsx"

def geocode_address(address, api_key):
    """פונקציה שמחזירה קואורדינטות עבור כתובת"""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if result["status"] == "OK":
            location = result["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

def main():
    df = pd.read_excel(INPUT_FILE)
    
    if "כתובת" not in df.columns:
        raise ValueError("בקובץ חייבת להיות עמודה בשם 'כתובת'")
    
    latitudes = []
    longitudes = []

    for idx, row in df.iterrows():
        address = row["כתובת"]
        print(f"מעבד כתובת: {address}")
        lat, lng = geocode_address(address, API_KEY)
        latitudes.append(lat)
        longitudes.append(lng)
        time.sleep(0.2)  # מנוחה קצרה למניעת חסימות API

    df["lat"] = latitudes
    df["lng"] = longitudes
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"הקובץ נשמר בהצלחה כ: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
