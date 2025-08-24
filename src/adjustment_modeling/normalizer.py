"""
DATA FRAME DESIGN Normalizer
Converts raw Zillow data to standardized fields for adjustment modeling

GREEN FIELDS (Direct from data):
- Address, Long, Lat, Sale Price, Gross Living Area, Date of Sale/Time
- Beds, Baths, Lot Area, Design and Appeal, Year Built
- Garage/Carport, Porch, Patio/Deck, Fireplace(s), Fence, Pool, Room Count

BLUE FIELDS (Calculated):
- Price per Square Foot, Age
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any

class PropertyNormalizer:
    
    def normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main normalization method - converts raw Zillow to standard fields"""
        normalized_df = pd.DataFrame()
        
        # Keep property type classification
        normalized_df['property_appraisal_type'] = df['property_appraisal_type']
        
        # GREEN FIELDS - Direct mappings from Zillow raw data
        normalized_df = self._add_green_fields(df, normalized_df)
        
        # BLUE FIELDS - Calculated from green fields
        normalized_df = self._add_blue_fields(normalized_df)
        
        return normalized_df
    
    def _add_green_fields(self, raw_df: pd.DataFrame, norm_df: pd.DataFrame) -> pd.DataFrame:
        """Add GREEN fields - direct mappings from raw Zillow data"""
        
        # Address & Location
        norm_df['address'] = raw_df['streetAddress'] + ', ' + raw_df['city'] + ', ' + raw_df['state'] + ' ' + raw_df['zipcode'].astype(str)
        norm_df['longitude'] = raw_df['longitude']
        norm_df['latitude'] = raw_df['latitude']
        
        # Sale Information
        norm_df['sale_price'] = raw_df['price'].fillna(raw_df['lastSoldPrice'])
        norm_df['date_of_sale'] = pd.to_datetime(raw_df['dateSoldString'], errors='coerce')
        
        # Physical Characteristics
        norm_df['gross_living_area'] = raw_df['livingArea']
        norm_df['beds'] = raw_df['bedrooms']
        norm_df['baths'] = raw_df['bathrooms']
        norm_df['lot_area'] = raw_df['lotSize']
        norm_df['year_built'] = raw_df['yearBuilt']
        
        # Design and Appeal (from construction materials and exterior features)
        norm_df['design_and_appeal'] = raw_df.apply(self._assess_design_appeal, axis=1)
        
        # Features - using hierarchical logic for conflicting data
        norm_df['garage_carport'] = raw_df.apply(self._normalize_garage, axis=1)
        norm_df['porch'] = raw_df.apply(self._normalize_porch_patio, axis=1)
        norm_df['patio_deck'] = raw_df.apply(self._normalize_porch_patio, axis=1)  # Same logic for both
        norm_df['fireplaces'] = raw_df.apply(self._normalize_fireplace, axis=1)
        norm_df['fence'] = raw_df.apply(self._normalize_fence, axis=1)
        norm_df['pool'] = raw_df.apply(self._normalize_pool, axis=1)
        norm_df['room_count'] = raw_df.apply(self._count_rooms, axis=1)
        
        return norm_df
    
    def _add_blue_fields(self, norm_df: pd.DataFrame) -> pd.DataFrame:
        """Add BLUE fields - calculated from green fields"""
        
        # Price per Square Foot
        norm_df['price_per_square_foot'] = norm_df.apply(
            lambda row: round(row['sale_price'] / row['gross_living_area'], 2) 
            if pd.notna(row['sale_price']) and pd.notna(row['gross_living_area']) and row['gross_living_area'] > 0
            else None, axis=1
        )
        
        # Age (calculated from year_built)
        current_year = datetime.now().year
        norm_df['age'] = norm_df['year_built'].apply(
            lambda x: current_year - x if pd.notna(x) else None
        )
        
        return norm_df
    
    # Helper methods for field transformations
    def _assess_design_appeal(self, row: pd.Series) -> str:
        """Assess design and appeal from construction materials and exterior features"""
        materials = row.get('constructionMaterials', [])
        exterior = row.get('exteriorFeatures', [])
        structure = row.get('structureType', '')
        
        appeal_score = 0
        
        # Material quality
        if isinstance(materials, list):
            if 'masonry' in materials:
                appeal_score += 2
        
        # Exterior features
        if isinstance(exterior, list):
            if 'Stone' in exterior:
                appeal_score += 2
        
        # Structure type
        if 'Ranch' in str(structure):
            appeal_score += 1
        
        if appeal_score >= 3:
            return 'Above Average'
        elif appeal_score >= 1:
            return 'Average'
        else:
            return 'Below Average'
    
    def _normalize_garage(self, row: pd.Series) -> str:
        """Normalize garage information using hierarchical logic"""
        # Priority 1: Check parkingFeatures array for explicit garage mention
        parking_features = row.get('parkingFeatures', [])
        if isinstance(parking_features, list) and parking_features:
            for feature in parking_features:
                if feature and 'garage' in str(feature).lower():
                    # Try to extract number from feature text
                    if 'attached' in str(feature).lower():
                        return "2 Car Garage"  # Default for attached
                    return "1 Car Garage"
        
        # Priority 2: Use specific garage capacity if available and > 0
        if pd.notna(row.get('garageParkingCapacity')) and row['garageParkingCapacity'] > 0:
            return f"{int(row['garageParkingCapacity'])} Car Garage"
        
        # Priority 3: Use general parking capacity if > 0
        if pd.notna(row.get('parkingCapacity')) and row['parkingCapacity'] > 0:
            return f"{int(row['parkingCapacity'])} Car Garage"
        
        # Priority 4: Check boolean flags
        if row.get('hasGarage') or row.get('hasAttachedGarage'):
            return "1 Car Garage"
        
        # Default: No garage
        return "No Garage"
    
    def _normalize_fireplace(self, row: pd.Series) -> int:
        """Normalize fireplace count using hierarchical logic"""
        # Priority 1: Use explicit fireplace count if available and > 0
        if pd.notna(row.get('fireplaces')) and row['fireplaces'] > 0:
            return int(row['fireplaces'])
        
        # Priority 2: Check boolean flag
        if row.get('hasFireplace'):
            return 1
        
        # Priority 3: Check fireplace features
        fireplace_features = row.get('fireplaceFeatures')
        if pd.notna(fireplace_features) and str(fireplace_features).lower() != 'none':
            return 1
        
        # Default: No fireplace
        return 0
    
    def _normalize_pool(self, row: pd.Series) -> str:
        """Normalize pool information using hierarchical logic"""
        # Priority 1: Check poolFeatures for explicit pool description
        pool_features = row.get('poolFeatures')
        if pd.notna(pool_features) and str(pool_features).lower() not in ['none', 'null', '']:
            return "Yes"
        
        # Priority 2: Check boolean flags
        if row.get('hasPrivatePool') or row.get('hasSpa'):
            return "Yes"
        
        # Priority 3: Check if pool features explicitly says no
        if pd.notna(pool_features) and str(pool_features).lower() == 'none':
            return "No"
        
    def _normalize_porch_patio(self, row: pd.Series) -> str:
        """Normalize porch/patio information using hierarchical logic"""
        # Priority 1: Check patioAndPorchFeatures
        patio_porch = row.get('patioAndPorchFeatures')
        if pd.notna(patio_porch) and str(patio_porch).lower() not in ['none', 'null', '']:
            return str(patio_porch)
        
        # Priority 2: Check description for patio/porch mentions
        description = row.get('description', '')
        if isinstance(description, str):
            desc_lower = description.lower()
            if 'porch' in desc_lower:
                return 'Porch'
            elif 'patio' in desc_lower:
                return 'Patio'
            elif 'deck' in desc_lower:
                return 'Deck'
        
        # Default: None
        return 'None'
    
    def _normalize_fence(self, row: pd.Series) -> str:
        """Normalize fence information using hierarchical logic"""
        # Priority 1: Check fencing field
        fencing = row.get('fencing')
        if pd.notna(fencing) and str(fencing).lower() not in ['none', 'null', '']:
            return str(fencing)
        
        # Priority 2: Check description for fence mentions
        description = row.get('description', '')
        if isinstance(description, str):
            desc_lower = description.lower()
            if 'fence' in desc_lower or 'fencing' in desc_lower:
                if 'privacy' in desc_lower:
                    return 'Privacy Fence'
                else:
                    return 'Fence'
        
        # Default: None
        return 'None'
    
    # Default: No pool
        return "No"
    
    def _count_rooms(self, row: pd.Series) -> int:
        """Count total rooms using hierarchical logic"""
        room_count = 0
        
        # Priority 1: Use explicit room counts if available
        bedrooms = row.get('bedrooms')
        bathrooms = row.get('bathrooms')
        
        if pd.notna(bedrooms) and bedrooms > 0:
            room_count += int(bedrooms)
        
        if pd.notna(bathrooms) and bathrooms > 0:
            room_count += int(bathrooms)
        
        # Priority 2: Add additional rooms from rooms array
        rooms_list = row.get('rooms', [])
        if isinstance(rooms_list, list) and rooms_list:
            # Count unique room types to avoid double counting
            unique_room_types = set()
            for room in rooms_list:
                if isinstance(room, dict) and 'roomType' in room:
                    room_type = room['roomType']
                    if room_type not in ['Bedroom', 'Bathroom']:  # Avoid double counting
                        unique_room_types.add(room_type)
            room_count += len(unique_room_types)
        
        # Priority 3: If no rooms found, try to infer from description
        if room_count == 0:
            description = row.get('description', '')
            if isinstance(description, str):
                # Simple extraction from description
                import re
                bed_match = re.search(r'(\d+)\s+bed', description.lower())
                bath_match = re.search(r'(\d+)\s+bath', description.lower())
                
                if bed_match:
                    room_count += int(bed_match.group(1))
                if bath_match:
                    room_count += int(bath_match.group(1))
        
        return room_count if room_count > 0 else None