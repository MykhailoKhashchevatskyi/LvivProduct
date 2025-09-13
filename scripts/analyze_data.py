#!/usr/bin/env python3
"""
Simple data analysis script for Lviv Food Establishments dataset.
Generates basic statistics and insights.
"""

import pandas as pd
import json
from collections import Counter

def analyze_dataset():
    """Analyze the Lviv food establishments dataset."""
    
    csv_path = '../data/lviv_food_clubs/lviv_food_clubs.csv'
    
    print("Lviv Food Establishments Dataset Analysis")
    print("=" * 50)
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Dataset loaded: {len(df)} establishments")
        print()
        
        # Basic statistics
        print("📊 BASIC STATISTICS")
        print("-" * 20)
        print(f"Total establishments: {len(df)}")
        print(f"Establishments with names: {len(df[df['name'].fillna('').astype(str).str.strip() != ''])}")
        print(f"Establishments with phone: {len(df[df['phone'].fillna('').astype(str).str.strip() != ''])}")
        print(f"Establishments with website: {len(df[df['website'].fillna('').astype(str).str.strip() != ''])}")
        print(f"Establishments with opening hours: {len(df[df['opening_hours'].fillna('').astype(str).str.strip() != ''])}")
        print()
        
        # Amenity types
        print("🏪 ESTABLISHMENT TYPES")
        print("-" * 20)
        amenity_counts = df['amenity'].value_counts()
        for amenity, count in amenity_counts.items():
            percentage = (count / len(df)) * 100
            print(f"{amenity.capitalize()}: {count} ({percentage:.1f}%)")
        print()
        
        # Districts
        print("🏘️ DISTRICT DISTRIBUTION")
        print("-" * 20)
        district_counts = df['city_district'].value_counts()
        for district, count in district_counts.items():
            percentage = (count / len(df)) * 100
            print(f"{district}: {count} ({percentage:.1f}%)")
        print()
        
        # Cuisine types
        print("🍽️ CUISINE TYPES")
        print("-" * 20)
        all_cuisines = []
        for cuisine_str in df['cuisine'].fillna(''):
            if cuisine_str.strip():
                # Split multiple cuisines separated by semicolons
                cuisines = [c.strip() for c in cuisine_str.split(';')]
                all_cuisines.extend(cuisines)
        
        if all_cuisines:
            cuisine_counts = Counter(all_cuisines)
            for cuisine, count in cuisine_counts.most_common():
                print(f"{cuisine}: {count}")
        else:
            print("No cuisine information available")
        print()
        
        # Accessibility
        print("♿ ACCESSIBILITY")
        print("-" * 20)
        wheelchair_counts = df['wheelchair'].value_counts()
        for access, count in wheelchair_counts.items():
            if access:
                percentage = (count / len(df)) * 100
                print(f"{access.capitalize()}: {count} ({percentage:.1f}%)")
        print()
        
        # Geographic center
        print("📍 GEOGRAPHIC CENTER")
        print("-" * 20)
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        print(f"Center point: {center_lat:.4f}, {center_lon:.4f}")
        print(f"Latitude range: {df['latitude'].min():.4f} to {df['latitude'].max():.4f}")
        print(f"Longitude range: {df['longitude'].min():.4f} to {df['longitude'].max():.4f}")
        print()
        
        # Notable establishments
        print("⭐ SAMPLE ESTABLISHMENTS")
        print("-" * 20)
        # Show a few examples with different amenity types
        for amenity_type in ['restaurant', 'cafe', 'bar', 'nightclub']:
            sample = df[df['amenity'] == amenity_type]
            if not sample.empty:
                est = sample.iloc[0]
                print(f"{amenity_type.capitalize()}: {est['name']}")
                if est['street'] and est['house_number']:
                    print(f"  Address: {est['street']}, {est['house_number']}")
                if est['phone']:
                    print(f"  Phone: {est['phone']}")
                print()
        
        print("💡 INSIGHTS")
        print("-" * 20)
        
        # Most common amenity
        most_common_amenity = amenity_counts.index[0]
        print(f"• Most common establishment type: {most_common_amenity} ({amenity_counts.iloc[0]} locations)")
        
        # District with most establishments
        most_popular_district = district_counts.index[0]
        print(f"• District with most establishments: {most_popular_district} ({district_counts.iloc[0]} locations)")
        
        # Accessibility stats
        accessible_count = len(df[df['wheelchair'] == 'yes'])
        if accessible_count > 0:
            print(f"• Wheelchair accessible establishments: {accessible_count} ({(accessible_count/len(df)*100):.1f}%)")
        
        # Business hours coverage
        hours_count = len(df[df['opening_hours'].fillna('').astype(str).str.strip() != ''])
        print(f"• Establishments with opening hours info: {hours_count} ({(hours_count/len(df)*100):.1f}%)")
        
        print()
        print("📄 For detailed field descriptions, see: data/lviv_food_clubs/metadata.md")
        print("📊 For the complete dataset, see: data/lviv_food_clubs/lviv_food_clubs.xlsx")
        
    except Exception as e:
        print(f"Error analyzing dataset: {e}")
        return False
    
    return True

if __name__ == '__main__':
    analyze_dataset()