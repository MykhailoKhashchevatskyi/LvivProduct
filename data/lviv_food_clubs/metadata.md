# Lviv Food Establishments and Clubs Dataset - Metadata

## Dataset Overview

This dataset contains comprehensive information about food establishments and clubs in Lviv, Ukraine, extracted from OpenStreetMap via the Overpass API.

## Data Source

- **Primary Source**: OpenStreetMap (OSM)
- **API**: Overpass API (https://overpass-api.de/)
- **License**: ODbL (Open Database License) - © OpenStreetMap contributors
- **Attribution**: Data: © OpenStreetMap contributors, ODbL

## Extraction Details

- **Extraction Date**: Generated automatically during script execution
- **Geographic Scope**: Administrative boundary of Lviv city
- **OSM Admin Level**: 8 (city level)
- **Query Method**: Overpass QL

## Data Fields

| Field Name | Description | Data Type | Source |
|------------|-------------|-----------|---------|
| `osm_id` | OSM element identifier with type prefix (node/way/relation) | String | OSM element ID |
| `name` | Name of the establishment | String | OSM `name` tag |
| `amenity` | Type of amenity or facility | String | OSM `amenity` or `tourism` tag |
| `cuisine` | Type of cuisine served | String | OSM `cuisine` tag |
| `street` | Street name | String | OSM `addr:street` tag |
| `house_number` | Building number | String | OSM `addr:housenumber` tag |
| `postcode` | Postal code | String | OSM `addr:postcode` tag |
| `city_district` | District within Lviv | String | OSM `addr:city_district` or spatial assignment |
| `latitude` | Geographic latitude (WGS84) | Float | OSM coordinates or computed centroid |
| `longitude` | Geographic longitude (WGS84) | Float | OSM coordinates or computed centroid |
| `phone` | Phone number | String | OSM `phone` or `contact:phone` tags |
| `website` | Website URL | String | OSM `website` or `contact:website` tags |
| `email` | Email address | String | OSM `email` or `contact:email` tags |
| `opening_hours` | Opening hours specification | String | OSM `opening_hours` tag |
| `wheelchair` | Wheelchair accessibility | String | OSM `wheelchair` tag |
| `source` | Data source identifier | String | Always "OpenStreetMap" |
| `last_updated` | Timestamp of data extraction | String (ISO 8601) | Generated during extraction |
| `raw_tags` | Complete OSM tags as JSON | String (JSON) | All OSM tags for the element |

## Amenity Types Included

The dataset includes establishments with the following OSM tags:

### Food Establishments
- `amenity=restaurant` - Full-service restaurants
- `amenity=cafe` - Cafes and coffee shops
- `amenity=fast_food` - Fast food outlets
- `amenity=food_court` - Food courts
- `amenity=ice_cream` - Ice cream shops
- `amenity=takeaway` - Takeaway food outlets

### Drinking Establishments
- `amenity=bar` - Bars and cocktail lounges
- `amenity=pub` - Pubs and taverns
- `amenity=biergarten` - Beer gardens

### Nightlife and Entertainment
- `amenity=nightclub` - Nightclubs
- `amenity=stripclub` - Strip clubs
- `amenity=social_centre` - Social centers (if relevant to nightlife)
- `tourism=nightclub` - Tourist-oriented nightclubs

## Data Processing

### Coordinate Handling
- **Nodes**: Direct latitude/longitude from OSM
- **Ways/Relations**: Computed centroid of the geometry
- **Projection**: WGS84 (EPSG:4326)

### Deduplication
- **Method**: Proximity-based with name matching
- **Distance Threshold**: 10 meters
- **Name Matching**: Case-insensitive, handles empty names
- **Merging Strategy**: Prioritizes non-empty values, combines OSM tags

### District Assignment
- **Primary**: OSM `addr:city_district` tag
- **Fallback**: Spatial intersection with OSM administrative boundaries
- **Method**: Point-in-polygon analysis using district boundary relations

## Data Quality Notes

### Completeness
- All records have valid coordinates
- Name fields may be empty for some establishments
- Address components depend on OSM data completeness
- District assignment may be incomplete due to boundary data availability

### Accuracy
- Coordinates are accurate to OSM precision
- Address information reflects OSM tagging quality
- Business information (hours, contact) may be outdated

### Limitations
- Data reflects OSM state at time of extraction
- Some establishments may be missing from OSM
- Commercial establishments may change frequently
- Opening hours and contact information may be outdated

## License and Attribution

This dataset is derived from OpenStreetMap data and is subject to the ODbL (Open Database License).

**Required Attribution**: 
- Data: © OpenStreetMap contributors, ODbL
- When using this data, you must:
  1. Attribute OpenStreetMap and its contributors
  2. Share any derivative works under ODbL
  3. Include a copy of or link to the ODbL license

**ODbL License**: https://opendatacommons.org/licenses/odbl/

## Usage Guidelines

1. **Attribution**: Always include OpenStreetMap attribution
2. **Share-Alike**: Distribute derivative works under ODbL
3. **Updates**: Consider refreshing data periodically as OSM is continuously updated
4. **Validation**: Verify critical information independently for commercial use

## File Formats

- **CSV**: `lviv_food_clubs.csv` - Standard comma-separated values
- **Excel**: `lviv_food_clubs.xlsx` - Microsoft Excel format with formatted columns
- **JSON**: `raw_osm.json` - Complete OSM tag data for advanced analysis

## Contact and Updates

For questions about this dataset or to request updates, please refer to the repository documentation or contact the maintainer.

**Generated**: Automatically during data extraction
**Tool**: fetch_lviv_osm.py
**Repository**: https://github.com/MykhailoKhashchevatskyi/LvivProduct