#!/usr/bin/env python3
"""
Lviv Food Establishments and Clubs Data Extraction Script

This script extracts food establishments and clubs data from OpenStreetMap
for the city of Lviv using the Overpass API, processes and deduplicates the data,
and outputs it in CSV and XLSX formats.

Data Source: OpenStreetMap via Overpass API
License: ODbL (Open Database License)
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

import pandas as pd
import geopandas as gpd
import requests
from retrying import retry
from shapely.geometry import Point, shape
from shapely.ops import transform


class LvivDataExtractor:
    """Extract and process OSM data for Lviv food establishments and clubs."""
    
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    
    def __init__(self):
        self.data = []
        self.districts_data = None
        
    @retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def query_overpass(self, query: str) -> Dict[str, Any]:
        """Query Overpass API with retry logic."""
        try:
            response = requests.post(self.OVERPASS_URL, data=query, timeout=300)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying Overpass API: {e}")
            raise
    
    def load_overpass_query(self, query_file: str) -> str:
        """Load Overpass QL query from file."""
        try:
            with open(query_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Query file {query_file} not found")
            sys.exit(1)
    
    def get_centroid(self, element: Dict[str, Any]) -> Optional[tuple]:
        """Get centroid coordinates from OSM element."""
        if element['type'] == 'node':
            return (element.get('lat'), element.get('lon'))
        elif element['type'] in ['way', 'relation'] and 'geometry' in element:
            try:
                coords = []
                for geom in element['geometry']:
                    if 'lat' in geom and 'lon' in geom:
                        coords.append((geom['lon'], geom['lat']))
                
                if coords:
                    # Create a simple polygon and get centroid
                    if len(coords) > 2 and coords[0] == coords[-1]:
                        # Closed polygon
                        from shapely.geometry import Polygon
                        poly = Polygon(coords)
                        centroid = poly.centroid
                        return (centroid.y, centroid.x)
                    else:
                        # Line or open way - use middle point
                        mid_idx = len(coords) // 2
                        return (coords[mid_idx][1], coords[mid_idx][0])
            except Exception:
                pass
        return None
    
    def extract_address_components(self, tags: Dict[str, str]) -> Dict[str, str]:
        """Extract address components from OSM tags."""
        return {
            'street': tags.get('addr:street', ''),
            'house_number': tags.get('addr:housenumber', ''),
            'postcode': tags.get('addr:postcode', ''),
            'city_district': tags.get('addr:city_district', '')
        }
    
    def process_element(self, element: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single OSM element into our data format."""
        tags = element.get('tags', {})
        
        # Get coordinates
        lat, lon = self.get_centroid(element) or (None, None)
        if lat is None or lon is None:
            return None
        
        # Extract address components
        address = self.extract_address_components(tags)
        
        # Create data record
        record = {
            'osm_id': f"{element['type']}/{element['id']}",
            'name': tags.get('name', ''),
            'amenity': tags.get('amenity', tags.get('tourism', '')),
            'cuisine': tags.get('cuisine', ''),
            'street': address['street'],
            'house_number': address['house_number'],
            'postcode': address['postcode'],
            'city_district': address['city_district'],
            'latitude': lat,
            'longitude': lon,
            'phone': tags.get('phone', tags.get('contact:phone', '')),
            'website': tags.get('website', tags.get('contact:website', '')),
            'email': tags.get('email', tags.get('contact:email', '')),
            'opening_hours': tags.get('opening_hours', ''),
            'wheelchair': tags.get('wheelchair', ''),
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps(tags, ensure_ascii=False)
        }
        
        return record
    
    def deduplicate_data(self, data: List[Dict[str, Any]], distance_threshold: float = 10.0) -> List[Dict[str, Any]]:
        """Deduplicate records based on proximity and name similarity."""
        if not data:
            return data
        
        # Convert to GeoDataFrame for spatial operations
        gdf = gpd.GeoDataFrame(data)
        gdf['geometry'] = gdf.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
        gdf = gdf.set_crs(epsg=4326)
        
        # Convert to local projection for distance calculations (UTM zone 35N for Lviv)
        gdf_utm = gdf.to_crs(epsg=32635)
        
        deduplicated = []
        processed_indices = set()
        
        for i, row in gdf_utm.iterrows():
            if i in processed_indices:
                continue
                
            # Find nearby points
            distances = gdf_utm.geometry.distance(row.geometry)
            nearby_mask = (distances <= distance_threshold) & (distances.index != i)
            nearby_indices = distances[nearby_mask].index.tolist()
            
            # Check for name similarity among nearby points
            candidates = [i] + nearby_indices
            same_name_candidates = []
            
            for idx in candidates:
                if idx in processed_indices:
                    continue
                other_name = gdf.loc[idx, 'name'].lower().strip()
                current_name = row['name'].lower().strip()
                
                # Consider same if names are identical or one is empty
                if (other_name == current_name) or (not other_name) or (not current_name):
                    same_name_candidates.append(idx)
            
            if same_name_candidates:
                # Merge records with same name in proximity
                merged_record = self.merge_records([gdf.loc[idx].to_dict() for idx in same_name_candidates])
                deduplicated.append(merged_record)
                processed_indices.update(same_name_candidates)
            else:
                # Keep original record
                record_dict = row.to_dict()
                if 'geometry' in record_dict:
                    del record_dict['geometry']
                deduplicated.append(record_dict)
                processed_indices.add(i)
        
        return deduplicated
    
    def merge_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple records into one, prioritizing non-empty values."""
        if len(records) == 1:
            record = records[0].copy()
            if 'geometry' in record:
                del record['geometry']
            return record
        
        merged = records[0].copy()
        if 'geometry' in merged:
            del merged['geometry']
        
        for record in records[1:]:
            for key, value in record.items():
                if key in ['geometry']:
                    continue
                if key in ['latitude', 'longitude']:
                    continue  # Keep coordinates from first record
                if not merged.get(key) and value:
                    merged[key] = value
                elif key == 'raw_tags':
                    # Merge raw tags
                    try:
                        tags1 = json.loads(merged.get(key, '{}'))
                        tags2 = json.loads(value or '{}')
                        tags1.update(tags2)
                        merged[key] = json.dumps(tags1, ensure_ascii=False)
                    except:
                        pass
        
        return merged
    
    def fetch_lviv_districts(self) -> Optional[gpd.GeoDataFrame]:
        """Fetch Lviv district boundaries from OSM."""
        district_query = """
        [out:json][timeout:60];
        (
          area["name"="Львів"]["admin_level"="8"]["place"="city"]->.lviv;
          rel["admin_level"="9"](area.lviv);
        );
        out geom;
        """
        
        try:
            result = self.query_overpass(district_query)
            districts = []
            
            for element in result.get('elements', []):
                if element['type'] == 'relation' and 'geometry' in element:
                    tags = element.get('tags', {})
                    name = tags.get('name', f"District_{element['id']}")
                    
                    # Convert geometry to shapely polygon
                    try:
                        coords = []
                        for geom in element['geometry']:
                            if 'lat' in geom and 'lon' in geom:
                                coords.append((geom['lon'], geom['lat']))
                        
                        if len(coords) > 2:
                            from shapely.geometry import Polygon
                            poly = Polygon(coords)
                            districts.append({
                                'name': name,
                                'geometry': poly
                            })
                    except Exception as e:
                        print(f"Error processing district geometry: {e}")
                        continue
            
            if districts:
                return gpd.GeoDataFrame(districts, crs='EPSG:4326')
        
        except Exception as e:
            print(f"Could not fetch district data: {e}")
        
        return None
    
    def assign_districts(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assign city districts to records based on coordinates."""
        if not data:
            return data
        
        # Try to fetch district boundaries
        districts_gdf = self.fetch_lviv_districts()
        
        if districts_gdf is None or districts_gdf.empty:
            print("Could not load district boundaries, keeping original district assignments")
            return data
        
        # Create GeoDataFrame from data
        df = pd.DataFrame(data)
        gdf = gpd.GeoDataFrame(df)
        gdf['geometry'] = gdf.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
        gdf = gdf.set_crs(epsg=4326)
        
        # Spatial join to assign districts
        joined = gpd.sjoin(gdf, districts_gdf, how='left', predicate='within')
        
        # Update city_district for records that were successfully matched
        for i, row in joined.iterrows():
            if pd.notna(row.get('name_right')) and not data[i].get('city_district'):
                data[i]['city_district'] = row['name_right']
        
        return data
    
    def extract_data(self, query_file: str) -> List[Dict[str, Any]]:
        """Main data extraction method."""
        print("Loading Overpass query...")
        query = self.load_overpass_query(query_file)
        
        print("Querying Overpass API...")
        result = self.query_overpass(query)
        
        print(f"Processing {len(result.get('elements', []))} elements...")
        
        processed_data = []
        for element in result.get('elements', []):
            record = self.process_element(element)
            if record:
                processed_data.append(record)
        
        print(f"Processed {len(processed_data)} valid records")
        
        print("Deduplicating data...")
        deduplicated_data = self.deduplicate_data(processed_data)
        print(f"After deduplication: {len(deduplicated_data)} records")
        
        print("Assigning city districts...")
        final_data = self.assign_districts(deduplicated_data)
        
        return final_data
    
    def save_data(self, data: List[Dict[str, Any]], output_dir: str):
        """Save data to CSV and XLSX formats."""
        if not data:
            print("No data to save")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Reorder columns to match requirements
        columns_order = [
            'osm_id', 'name', 'amenity', 'cuisine', 'street', 'house_number',
            'postcode', 'city_district', 'latitude', 'longitude', 'phone',
            'website', 'email', 'opening_hours', 'wheelchair', 'source',
            'last_updated', 'raw_tags'
        ]
        
        # Ensure all columns exist
        for col in columns_order:
            if col not in df.columns:
                df[col] = ''
        
        df = df[columns_order]
        
        # Save CSV
        csv_path = os.path.join(output_dir, 'lviv_food_clubs.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Saved CSV: {csv_path}")
        
        # Save XLSX
        xlsx_path = os.path.join(output_dir, 'lviv_food_clubs.xlsx')
        df.to_excel(xlsx_path, index=False, engine='openpyxl')
        print(f"Saved XLSX: {xlsx_path}")
        
        # Save raw OSM data as JSON
        raw_data = [json.loads(record['raw_tags']) for record in data if record.get('raw_tags')]
        raw_json_path = os.path.join(output_dir, 'raw_osm.json')
        with open(raw_json_path, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        print(f"Saved raw OSM data: {raw_json_path}")
        
        print(f"\nDataset summary:")
        print(f"Total records: {len(df)}")
        print(f"Records with names: {len(df[df['name'].str.strip() != ''])}")
        print(f"Records with addresses: {len(df[df['street'].str.strip() != ''])}")
        print(f"Records with districts: {len(df[df['city_district'].str.strip() != ''])}")
        print(f"Amenity types: {df['amenity'].value_counts().to_dict()}")


def main():
    """Main function."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    query_file = os.path.join(script_dir, 'overpass_query.txt')
    output_dir = os.path.join(os.path.dirname(script_dir), 'data', 'lviv_food_clubs')
    
    print("Lviv Food Establishments and Clubs Data Extraction")
    print("=" * 50)
    print(f"Query file: {query_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    extractor = LvivDataExtractor()
    
    try:
        data = extractor.extract_data(query_file)
        extractor.save_data(data, output_dir)
        print("\nData extraction completed successfully!")
        
    except KeyboardInterrupt:
        print("\nExtraction cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during extraction: {e}")
        print("\nIf you're experiencing network issues, you can generate sample data instead:")
        print("python create_sample_data.py")
        sys.exit(1)


if __name__ == '__main__':
    main()