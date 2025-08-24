"""
Simple Data Loader - Loads raw JSON and adds property_appraisal_type column
"""
import json
import pandas as pd
from typing import Dict, List

class PropertyDataLoader:
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        
    def load_raw_data(self) -> Dict:
        """Load raw JSON data from file"""
        with open(self.data_path, 'r') as file:
            return json.load(file)
            
    def extract_properties(self, raw_data: Dict) -> List[Dict]:
        """Extract subject and comparable properties, add property_appraisal_type"""
        properties = []
        
        # Add subject property
        if 'subject_property' in raw_data:
            subject = raw_data['subject_property'].copy()
            subject['property_appraisal_type'] = 'subject'
            properties.append(subject)
            
        # Add comparable properties
        if 'comparables' in raw_data:
            for comp in raw_data['comparables']:
                comp_data = comp.copy()
                comp_data['property_appraisal_type'] = 'comparable'
                properties.append(comp_data)
                
        return properties
        
    def load_and_prepare(self) -> pd.DataFrame:
        """Main method: load data and return DataFrame with property_appraisal_type"""
        raw_data = self.load_raw_data()
        properties = self.extract_properties(raw_data)
        df = pd.DataFrame(properties)
        return df