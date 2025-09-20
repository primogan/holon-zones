import geopandas as gpd
import pandas as pd

# קריאת הפוליגונים (האזורים)
zones = gpd.read_file("holon-zones.geojson")

# קריאת הפניות (עם lat/lng)
df = pd.read_excel("holon_trees_geocoded.xlsx")
gdf_points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lng'], df['lat']), crs="EPSG:4326")

# שיוך נקודות לפוליגונים
joined = gpd.sjoin(gdf_points, zones, how="left", predicate="within")

# שמירה ל-GeoJSON חדש עם נתוני אזור
joined[['כתובת', 'lat', 'lng', 'geometry', 'שם_איזור']].to_file("holon_trees_with_zones.geojson", driver="GeoJSON")

print("✔️ נוצר הקובץ holon_trees_with_zones.geojson עם שיוך כל פניה לאזור")
