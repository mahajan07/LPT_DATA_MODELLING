# LPT Adjustment Data Modelling

A simple Python module to load and normalize property data from JSON files, designed to streamline the initial steps of a data modeling workflow.

## Getting Started

**1. Clone the repository and install dependencies:**

```bash
git clone [https://github.com/mahajan07/LPT_DATA_MODELLING.git](https://github.com/mahajan07/LPT_DATA_MODELLING.git)
cd LPT_DATA_MODELLING
pip install pandas numpy
```
**2. Use the modules in your project:**
```bash
from src.adjustment_modeling.data_loader import PropertyDataLoader
from src.adjustment_modeling.normalizer import PropertyNormalizer

# Load data from a JSON file
loader = PropertyDataLoader('raw_data.json')
property_df = loader.load_data()

# Initialize the normalizer with the DataFrame
normalizer = PropertyNormalizer(property_df)

# Normalize a specific column (e.g., 'price')
normalized_df = normalizer.normalize_column('price')

print("Data loaded and normalized successfully:")
print(normalized_df.head())
```

```bash
File Scaffolding 
├── src.adjustment_modeling/
│   ├── data_loader.py      # Contains the PropertyDataLoader class
│   └── normalizer.py       # Contains the PropertyNormalizer class
├── Data
│   ├── raw_data.json       # raw data file
└── test_module.ipynb       # Jupyter notebook demonstrating usage
```
