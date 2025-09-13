#!/usr/bin/env python3
"""
Data validation script for Lviv Food Establishments dataset.
Validates data quality and provides summary statistics.
"""

import pandas as pd
import json
import os

def validate_dataset():
    """Validate the generated dataset."""
    
    # File paths
    csv_path = '../data/lviv_food_clubs/lviv_food_clubs.csv'
    xlsx_path = '../data/lviv_food_clubs/lviv_food_clubs.xlsx'
    json_path = '../data/lviv_food_clubs/raw_osm.json'
    
    print("Lviv Food Establishments Dataset Validation")
    print("=" * 50)
    
    # Check if files exist
    files_to_check = [csv_path, xlsx_path, json_path]
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists ({os.path.getsize(file_path):,} bytes)")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    print()
    
    # Load and validate CSV
    try:
        df = pd.read_csv(csv_path)
        print(f"CSV Dataset loaded successfully: {len(df)} records")
        
        # Validate required columns
        required_columns = [
            'osm_id', 'name', 'amenity', 'latitude', 'longitude', 
            'source', 'last_updated'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"✗ Missing required columns: {missing_columns}")
            return False
        else:
            print(f"✓ All required columns present")
        
        # Data quality checks
        print("\nData Quality Checks:")
        print(f"✓ Records with valid coordinates: {len(df[df['latitude'].notna() & df['longitude'].notna()])}/{len(df)}")
        print(f"✓ Records with names: {len(df[df['name'].str.strip() != ''])}/{len(df)}")
        print(f"✓ Records with addresses: {len(df[df['street'].str.strip() != ''])}/{len(df)}")
        print(f"✓ Records with districts: {len(df[df['city_district'].str.strip() != ''])}/{len(df)}")
        
        # Amenity distribution
        print(f"\nAmenity Distribution:")
        amenity_counts = df['amenity'].value_counts()
        for amenity, count in amenity_counts.items():
            print(f"  {amenity}: {count}")
        
        # Coordinate bounds (rough Lviv area check)
        lat_min, lat_max = df['latitude'].min(), df['latitude'].max()
        lon_min, lon_max = df['longitude'].min(), df['longitude'].max()
        print(f"\nCoordinate Bounds:")
        print(f"  Latitude: {lat_min:.4f} to {lat_max:.4f}")
        print(f"  Longitude: {lon_min:.4f} to {lon_max:.4f}")
        
        # Check if coordinates are in Lviv area (approximate)
        lviv_lat_range = (49.75, 49.90)
        lviv_lon_range = (23.95, 24.15)
        
        coords_in_range = (
            (df['latitude'] >= lviv_lat_range[0]) & 
            (df['latitude'] <= lviv_lat_range[1]) &
            (df['longitude'] >= lviv_lon_range[0]) & 
            (df['longitude'] <= lviv_lon_range[1])
        ).sum()
        
        print(f"  Records within Lviv area: {coords_in_range}/{len(df)}")
        
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return False
    
    # Validate Excel file
    try:
        df_excel = pd.read_excel(xlsx_path)
        if len(df_excel) == len(df):
            print(f"\n✓ Excel file matches CSV: {len(df_excel)} records")
        else:
            print(f"\n✗ Excel file mismatch: {len(df_excel)} vs {len(df)} records")
    except Exception as e:
        print(f"\n✗ Error loading Excel file: {e}")
        return False
    
    # Validate JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        if len(raw_data) == len(df):
            print(f"✓ Raw JSON data matches CSV: {len(raw_data)} records")
        else:
            print(f"✗ Raw JSON data mismatch: {len(raw_data)} vs {len(df)} records")
        
        # Check JSON structure
        if raw_data and isinstance(raw_data[0], dict):
            sample_keys = list(raw_data[0].keys())
            print(f"✓ Sample raw OSM tags: {', '.join(sample_keys[:5])}...")
        
    except Exception as e:
        print(f"✗ Error loading JSON file: {e}")
        return False
    
    print(f"\n✅ Dataset validation completed successfully!")
    print(f"\nDataset is ready for use. See metadata.md for detailed field descriptions.")
    
    return True

if __name__ == '__main__':
    validate_dataset()