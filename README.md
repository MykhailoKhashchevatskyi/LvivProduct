# LvivProduct

A comprehensive dataset of food establishments and clubs in Lviv, Ukraine, extracted from OpenStreetMap.

## Dataset Overview

This repository contains a curated dataset of restaurants, cafes, bars, clubs, and other food-related establishments in Lviv, sourced from OpenStreetMap via the Overpass API.

**Data Source**: © OpenStreetMap contributors, ODbL  
**Last Updated**: Generated automatically during extraction  
**Geographic Scope**: Lviv city administrative boundary

## Quick Start

### Download the Dataset

The dataset is available in two formats:
- **Excel**: [`data/lviv_food_clubs/lviv_food_clubs.xlsx`](data/lviv_food_clubs/lviv_food_clubs.xlsx)
- **CSV**: [`data/lviv_food_clubs/lviv_food_clubs.csv`](data/lviv_food_clubs/lviv_food_clubs.csv)

### Data Fields

Each record includes:
- **Location**: Name, address, coordinates, district
- **Type**: Amenity type, cuisine
- **Contact**: Phone, website, email
- **Details**: Opening hours, wheelchair accessibility
- **Metadata**: OSM ID, source, extraction date

See [`data/lviv_food_clubs/metadata.md`](data/lviv_food_clubs/metadata.md) for complete field documentation.

## Reproducing the Dataset

### Prerequisites

1. **Python 3.8+** with pip
2. **Required packages**:
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

### Running the Extraction

```bash
# Navigate to scripts directory
cd scripts

# Install dependencies
pip install -r requirements.txt

# Run the extraction script
python fetch_lviv_osm.py
```

The script will:
1. Query OpenStreetMap via Overpass API
2. Process and deduplicate the data
3. Assign city districts using spatial analysis
4. Generate CSV, XLSX, and JSON output files

### Customizing the Query

Edit [`scripts/overpass_query.txt`](scripts/overpass_query.txt) to modify:
- Geographic boundaries
- Amenity types to include
- Additional OSM tags to extract

## Data Processing Details

### Extraction Process
1. **Query**: Overpass QL query for Lviv administrative boundary
2. **Filtering**: Food establishments and nightlife venues
3. **Geocoding**: Coordinate extraction or centroid calculation
4. **Deduplication**: 10-meter proximity with name matching
5. **District Assignment**: Spatial join with OSM district boundaries

### Quality Assurance
- All records have valid coordinates
- Duplicate removal based on location and name
- Address standardization where possible
- District assignment for location context

## License and Attribution

### Data License
This dataset is derived from OpenStreetMap and is licensed under the **ODbL (Open Database License)**.

**Required Attribution**: Data: © OpenStreetMap contributors, ODbL

### Usage Requirements
When using this data, you must:
1. **Attribute** OpenStreetMap and its contributors
2. **Share-alike** any derivative works under ODbL
3. **Include** ODbL license information

**ODbL License**: https://opendatacommons.org/licenses/odbl/

### Code License
The extraction scripts are available under the MIT License.

## Contributing

### Updating the Dataset
To refresh the dataset with current OSM data:
```bash
cd scripts
python fetch_lviv_osm.py
```

### Improving the Scripts
- Report issues or suggest improvements via GitHub Issues
- Submit pull requests for bug fixes or enhancements
- Follow existing code style and documentation standards

## Data Limitations

- **Currency**: Reflects OSM state at extraction time
- **Completeness**: Limited to OSM coverage and tagging quality
- **Accuracy**: Business details may become outdated
- **Scope**: Only includes establishments tagged in OSM

For commercial use, consider verifying critical information independently.

## Contact

For questions, suggestions, or collaboration opportunities, please use GitHub Issues or contact the repository maintainer.

---

*This dataset is part of the LvivProduct project, providing open data resources for Lviv's business and cultural landscape.*