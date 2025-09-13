#!/usr/bin/env python3
"""
Create sample dataset for Lviv Food Establishments and Clubs
This creates a representative sample dataset for demonstration purposes.
"""

import json
import os
import pandas as pd
from datetime import datetime

def create_sample_data():
    """Create a sample dataset with realistic Lviv establishments."""
    
    sample_data = [
        {
            'osm_id': 'node/123456789',
            'name': 'Café Central',
            'amenity': 'cafe',
            'cuisine': 'coffee_shop;european',
            'street': 'площа Ринок',
            'house_number': '1',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8414,
            'longitude': 24.0315,
            'phone': '+380322974747',
            'website': 'https://cafe-central.lviv.ua',
            'email': 'info@cafe-central.lviv.ua',
            'opening_hours': 'Mo-Su 08:00-22:00',
            'wheelchair': 'yes',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Café Central',
                'amenity': 'cafe',
                'cuisine': 'coffee_shop;european',
                'addr:street': 'площа Ринок',
                'addr:housenumber': '1',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380322974747',
                'website': 'https://cafe-central.lviv.ua',
                'email': 'info@cafe-central.lviv.ua',
                'opening_hours': 'Mo-Su 08:00-22:00',
                'wheelchair': 'yes'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'way/987654321',
            'name': 'Ресторан Бернардацький',
            'amenity': 'restaurant',
            'cuisine': 'ukrainian;european',
            'street': 'вул. Валова',
            'house_number': '8',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8425,
            'longitude': 24.0285,
            'phone': '+380322975555',
            'website': 'https://bernardazki.lviv.ua',
            'email': '',
            'opening_hours': 'Mo-Su 12:00-23:00',
            'wheelchair': 'limited',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Ресторан Бернардацький',
                'amenity': 'restaurant',
                'cuisine': 'ukrainian;european',
                'addr:street': 'вул. Валова',
                'addr:housenumber': '8',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380322975555',
                'website': 'https://bernardazki.lviv.ua',
                'opening_hours': 'Mo-Su 12:00-23:00',
                'wheelchair': 'limited'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'node/456789123',
            'name': 'Львівська мануфактура кави',
            'amenity': 'cafe',
            'cuisine': 'coffee_shop',
            'street': 'вул. Катедральна',
            'house_number': '6',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8432,
            'longitude': 24.0298,
            'phone': '+380322761717',
            'website': '',
            'email': 'info@lviv-coffee.com',
            'opening_hours': 'Mo-Su 07:30-21:00',
            'wheelchair': 'no',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Львівська мануфактура кави',
                'amenity': 'cafe',
                'cuisine': 'coffee_shop',
                'addr:street': 'вул. Катедральна',
                'addr:housenumber': '6',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380322761717',
                'email': 'info@lviv-coffee.com',
                'opening_hours': 'Mo-Su 07:30-21:00',
                'wheelchair': 'no'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'node/789123456',
            'name': 'Pravda Beer Theatre',
            'amenity': 'bar',
            'cuisine': 'beer',
            'street': 'вул. Личаківська',
            'house_number': '15',
            'postcode': '79008',
            'city_district': 'Личаківський район',
            'latitude': 49.8345,
            'longitude': 24.0423,
            'phone': '+380977765432',
            'website': 'https://pravda.beer',
            'email': 'hello@pravda.beer',
            'opening_hours': 'Mo-Th 16:00-01:00; Fr-Sa 16:00-02:00; Su 16:00-24:00',
            'wheelchair': 'yes',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Pravda Beer Theatre',
                'amenity': 'bar',
                'cuisine': 'beer',
                'addr:street': 'вул. Личаківська',
                'addr:housenumber': '15',
                'addr:postcode': '79008',
                'addr:city_district': 'Личаківський район',
                'phone': '+380977765432',
                'website': 'https://pravda.beer',
                'email': 'hello@pravda.beer',
                'opening_hours': 'Mo-Th 16:00-01:00; Fr-Sa 16:00-02:00; Su 16:00-24:00',
                'wheelchair': 'yes'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'node/321654987',
            'name': 'McDonalds',
            'amenity': 'fast_food',
            'cuisine': 'burger',
            'street': 'пр. Свободи',
            'house_number': '23',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8383,
            'longitude': 24.0232,
            'phone': '+380800750750',
            'website': 'https://mcdonalds.ua',
            'email': '',
            'opening_hours': '24/7',
            'wheelchair': 'yes',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'McDonalds',
                'amenity': 'fast_food',
                'cuisine': 'burger',
                'brand': 'McDonalds',
                'addr:street': 'пр. Свободи',
                'addr:housenumber': '23',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380800750750',
                'website': 'https://mcdonalds.ua',
                'opening_hours': '24/7',
                'wheelchair': 'yes'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'way/147258369',
            'name': 'Amadeus',
            'amenity': 'nightclub',
            'cuisine': '',
            'street': 'вул. Чорновола',
            'house_number': '7',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8456,
            'longitude': 24.0267,
            'phone': '+380974123456',
            'website': '',
            'email': '',
            'opening_hours': 'Fr-Sa 22:00-06:00',
            'wheelchair': 'no',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Amadeus',
                'amenity': 'nightclub',
                'addr:street': 'вул. Чорновола',
                'addr:housenumber': '7',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380974123456',
                'opening_hours': 'Fr-Sa 22:00-06:00',
                'wheelchair': 'no'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'node/963852741',
            'name': 'Пузата Хата',
            'amenity': 'restaurant',
            'cuisine': 'ukrainian',
            'street': 'вул. Городоцька',
            'house_number': '42',
            'postcode': '79018',
            'city_district': 'Шевченківський район',
            'latitude': 49.8289,
            'longitude': 24.0187,
            'phone': '+380673334455',
            'website': 'https://puzatahata.ua',
            'email': '',
            'opening_hours': 'Mo-Su 09:00-22:00',
            'wheelchair': 'yes',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Пузата Хата',
                'amenity': 'restaurant',
                'cuisine': 'ukrainian',
                'brand': 'Пузата Хата',
                'addr:street': 'вул. Городоцька',
                'addr:housenumber': '42',
                'addr:postcode': '79018',
                'addr:city_district': 'Шевченківський район',
                'phone': '+380673334455',
                'website': 'https://puzatahata.ua',
                'opening_hours': 'Mo-Su 09:00-22:00',
                'wheelchair': 'yes'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'node/741852963',
            'name': 'Vetek',
            'amenity': 'pub',
            'cuisine': 'beer;pub_food',
            'street': 'вул. Вірменська',
            'house_number': '35',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8401,
            'longitude': 24.0334,
            'phone': '+380322971234',
            'website': '',
            'email': '',
            'opening_hours': 'Mo-Su 12:00-02:00',
            'wheelchair': 'limited',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Vetek',
                'amenity': 'pub',
                'cuisine': 'beer;pub_food',
                'addr:street': 'вул. Вірменська',
                'addr:housenumber': '35',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380322971234',
                'opening_hours': 'Mo-Su 12:00-02:00',
                'wheelchair': 'limited'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'node/159357486',
            'name': 'Gelato Cafe',
            'amenity': 'ice_cream',
            'cuisine': 'ice_cream',
            'street': 'вул. Дорошенка',
            'house_number': '12',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8445,
            'longitude': 24.0278,
            'phone': '',
            'website': '',
            'email': '',
            'opening_hours': 'Mo-Su 10:00-21:00',
            'wheelchair': 'yes',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Gelato Cafe',
                'amenity': 'ice_cream',
                'cuisine': 'ice_cream',
                'addr:street': 'вул. Дорошенка',
                'addr:housenumber': '12',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'opening_hours': 'Mo-Su 10:00-21:00',
                'wheelchair': 'yes'
            }, ensure_ascii=False)
        },
        {
            'osm_id': 'way/753951864',
            'name': 'Baczewski Restaurant',
            'amenity': 'restaurant',
            'cuisine': 'polish;european;galician',
            'street': 'вул. Армянська',
            'house_number': '2',
            'postcode': '79000',
            'city_district': 'Галицький район',
            'latitude': 49.8418,
            'longitude': 24.0312,
            'phone': '+380322971717',
            'website': 'https://baczewski.com.ua',
            'email': 'info@baczewski.com.ua',
            'opening_hours': 'Mo-Su 12:00-24:00',
            'wheelchair': 'yes',
            'source': 'OpenStreetMap',
            'last_updated': datetime.now().isoformat(),
            'raw_tags': json.dumps({
                'name': 'Baczewski Restaurant',
                'amenity': 'restaurant',
                'cuisine': 'polish;european;galician',
                'addr:street': 'вул. Армянська',
                'addr:housenumber': '2',
                'addr:postcode': '79000',
                'addr:city_district': 'Галицький район',
                'phone': '+380322971717',
                'website': 'https://baczewski.com.ua',
                'email': 'info@baczewski.com.ua',
                'opening_hours': 'Mo-Su 12:00-24:00',
                'wheelchair': 'yes'
            }, ensure_ascii=False)
        }
    ]
    
    return sample_data

def main():
    # Create sample data
    data = create_sample_data()
    
    # Create output directory
    output_dir = '../data/lviv_food_clubs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Column order
    columns_order = [
        'osm_id', 'name', 'amenity', 'cuisine', 'street', 'house_number',
        'postcode', 'city_district', 'latitude', 'longitude', 'phone',
        'website', 'email', 'opening_hours', 'wheelchair', 'source',
        'last_updated', 'raw_tags'
    ]
    
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
    raw_data = [json.loads(record['raw_tags']) for record in data]
    raw_json_path = os.path.join(output_dir, 'raw_osm.json')
    with open(raw_json_path, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print(f"Saved raw OSM data: {raw_json_path}")
    
    print(f"\nSample dataset summary:")
    print(f"Total records: {len(df)}")
    print(f"Records with names: {len(df[df['name'].str.strip() != ''])}")
    print(f"Records with addresses: {len(df[df['street'].str.strip() != ''])}")
    print(f"Records with districts: {len(df[df['city_district'].str.strip() != ''])}")
    print(f"Amenity types: {df['amenity'].value_counts().to_dict()}")

if __name__ == '__main__':
    main()