#!/usr/bin/env python3
"""
Fetch Lviv food & clubs from OpenStreetMap via Overpass API,
normalize tags, deduplicate, assign city district polygons, and
write CSV / XLSX / raw JSON.

Usage:
    pip install -r requirements.txt
    python scripts/fetch_lviv_osm.py --out data/lviv_food_clubs --overwrite

Outputs:
    - data/lviv_food_clubs/raw_osm.json
    - data/lviv_food_clubs/lviv_food_clubs.csv
    - data/lviv_food_clubs/lviv_food_clubs.xlsx
    - data/lviv_food_clubs/metadata.md (not overwritten if exists)
"""
import os
import time
import json
import argparse
import requests
from datetime import datetime

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
AMENITIES = [
    "restaurant", "cafe", "bar", "fast_food", "pub", "food_court",
    "biergarten", "ice_cream", "ice_cream_stand", "takeaway", "snack",
    "coffee_shop", "coffee", "tea_house", "nightclub", "stripclub"
]

def load_overpass_query():
    with open("scripts/overpass_query.txt", "r", encoding="utf-8") as fh:
        return fh.read()

def run_overpass(query, max_tries=5, backoff=5):
    for attempt in range(max_tries):
        try:
            resp = requests.post(OVERPASS_URL, data={"data": query}, timeout=180)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            wait = backoff * (attempt + 1)
            print(f"Overpass request failed (attempt {attempt+1}/{max_tries}): {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Overpass query failed after retries")

def extract_records(osm_json):
    records = []
    for el in osm_json.get("elements", []):
        tags = el.get("tags", {}) or {}
        lat = None
        lon = None
        if el["type"] == "node":
            lat = el.get("lat")
            lon = el.get("lon")
        else:
            center = el.get("center") or el.get("bounds")
            if center:
                lat = center.get("lat") or None
                lon = center.get("lon") or None
        if lat is None or lon is None:
            continue
        rec = {
            "osm_type": el["type"],
            "osm_id": f'{el["type"]}/{el["id"]}',
            "name": tags.get("name"),
            "amenity": tags.get("amenity") or tags.get("tourism"),
            "cuisine": tags.get("cuisine"),
            "street": tags.get("addr:street"),
            "house_number": tags.get("addr:housenumber"),
            "postcode": tags.get("addr:postcode"),
            "city_district": tags.get("addr:city_district"),
            "latitude": lat,
            "longitude": lon,
            "phone": tags.get("phone") or tags.get("contact:phone"),
            "website": tags.get("website") or tags.get("contact:website"),
            "email": tags.get("email") or tags.get("contact:email"),
            "opening_hours": tags.get("opening_hours"),
            "wheelchair": tags.get("wheelchair"),
            "tags": tags,
        }
        records.append(rec)
    return records

def deduplicate_records(df, radius_m=10):
    df = df.copy()
    df["geom"] = df.apply(lambda r: Point(r.longitude, r.latitude), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry="geom", crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)
    gdf["cluster"] = -1
    idx = 0
    for i, row in gdf.iterrows():
        if gdf.at[i, "cluster"] != -1:
            continue
        name = (row["name"] or "").strip().lower()
        if not name:
            gdf.at[i, "cluster"] = idx; idx += 1
            continue
        buffer = row.geometry.buffer(radius_m)
        candidates = gdf[gdf.geometry.within(buffer) | gdf.geometry.intersects(buffer)]
        for j, cand in candidates.iterrows():
            cand_name = (cand.get("name") or "").strip().lower()
            if cand_name == name:
                if gdf.at[i, "cluster"] == -1:
                    gdf.at[i, "cluster"] = idx
                gdf.at[j, "cluster"] = gdf.at[i, "cluster"]
        if gdf.at[i, "cluster"] == -1:
            gdf.at[i, "cluster"] = idx
            idx += 1
    out_rows = []
    for cluster_id, group in gdf.groupby("cluster"):
        primary = group.loc[group["name"].notna()].iloc[0] if any(group["name"].notna()) else group.iloc[0]
        agg = primary.to_dict()
        cuisines = set()
        phones = set()
        websites = set()
        emails = set()
        tags_agg = {}
        for _, r in group.iterrows():
            if r.get("cuisine"):
                cuisines.update([c.strip() for c in str(r.cuisine).split(";")])
            if r.get("phone"):
                phones.add(r.phone)
            if r.get("website"):
                websites.add(r.website)
            if r.get("email"):
                emails.add(r.email)
            if isinstance(r.tags, dict):
                tags_agg.update(r.tags)
        agg["cuisine"] = ";".join(sorted(cuisines)) if cuisines else agg.get("cuisine")
        agg["phone"] = ";".join(sorted(phones)) if phones else agg.get("phone")
        agg["website"] = ";".join(sorted(websites)) if websites else agg.get("website")
        agg["email"] = ";".join(sorted(emails)) if emails else agg.get("email")
        agg["raw_tags"] = tags_agg
        out_rows.append(agg)
    out_df = pd.DataFrame(out_rows)
    out_df["longitude"] = out_df["geom"].x
    out_df["latitude"] = out_df["geom"].y
    out_df = out_df.drop(columns=["geom"])
    out_df = out_df.reset_index(drop=True)
    return out_df

def assign_districts(gdf_places):
    try:
        q = """
        [out:json][timeout:120];
        area["name"~"Львів|Lviv"]["boundary"="administrative"]->.city;
        (
          relation["boundary"="administrative"]["admin_level"~"9|10"](area.city);
        );
        out geom;
        """
        resp = run_overpass(q)
        rels = resp.get("elements", [])
        polys = []
        for r in rels:
            if r.get("type") != "relation":
                continue
            props = r.get("tags", {}) or {}
            name = props.get("name")
            if "geometry" in r:
                try:
                    coords = [(pt["lon"], pt["lat"]) for pt in r["geometry"]]
                    from shapely.geometry import Polygon
                    poly = Polygon(coords)
                    polys.append({"name": name, "geometry": poly, "tags": props})
                except Exception:
                    continue
        if not polys:
            print("No district polygons found via Overpass; skipping spatial join.")
            return gdf_places
        districts = gpd.GeoDataFrame(polys, crs="EPSG:4326")
        places = gdf_places.copy()
        places = places.set_geometry(gpd.points_from_xy(places.longitude, places.latitude))
        places = places.set_crs(epsg=4326)
        join = gpd.sjoin(places, districts, how="left", predicate="within")
        places["city_district_assigned"] = join["name"]
        places["city_district"] = places["city_district"].fillna(places["city_district_assigned"])
        places = places.drop(columns=["index_right", "city_district_assigned"])
        return places
    except Exception as e:
        print("Error assigning districts:", e)
        return gdf_places

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/lviv_food_clubs", help="output folder")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    query = load_overpass_query()
    print("Running Overpass query...")
    osm_json = run_overpass(query)
    with open(os.path.join(out_dir, "raw_osm.json"), "w", encoding="utf-8") as fh:
        json.dump(osm_json, fh, ensure_ascii=False, indent=2)

    records = extract_records(osm_json)
    if not records:
        print("No records extracted.")
        return
    df = pd.DataFrame(records)
    df["source"] = "OpenStreetMap"
    df["last_updated"] = datetime.utcnow().isoformat() + "Z"

    print(f"Extracted {len(df)} records. Deduplicating...")
    deduped = deduplicate_records(df, radius_m=10)
    print(f"{len(deduped)} records after deduplication.")

    try:
        gdf_places = deduped.copy()
        gdf_places = gpd.GeoDataFrame(gdf_places, geometry=gpd.points_from_xy(gdf_places.longitude, gdf_places.latitude), crs="EPSG:4326")
        gdf_places = assign_districts(gdf_places)
        final_df = pd.DataFrame(gdf_places.drop(columns=["geometry"]))
    except Exception as e:
        print("District assignment failed; continuing without it:", e)
        final_df = deduped

    cols = ["osm_id","name","amenity","cuisine","street","house_number","postcode","city_district",
            "latitude","longitude","phone","website","email","opening_hours","wheelchair","source","last_updated","raw_tags"]
    for c in cols:
        if c not in final_df.columns:
            final_df[c] = None
    final_df = final_df[cols]

    csv_path = os.path.join(out_dir, "lviv_food_clubs.csv")
    xlsx_path = os.path.join(out_dir, "lviv_food_clubs.xlsx")
    final_df.to_csv(csv_path, index=False, encoding="utf-8")
    try:
        final_df.to_excel(xlsx_path, index=False)
    except Exception as e:
        print("Writing XLSX failed:", e)
    print("Written CSV and XLSX to", out_dir)

if __name__ == "__main__":
    main()