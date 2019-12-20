# Get Government Data
This module posts the data from the [government data](https://fdc.nal.usda.gov/fdc-datasets) into the database.

The posting is controlled via the database schema, and `convert.json`.

## convert.json

The json file is keyed by the government file name. 

The file contains one other fields: 

`model` is the table name.

### Sample
```json
{
  "food.csv": {
    "model": "food"
  }
}
```
