import json
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Property:
    id: str
    rooms: int
    price: float
    currency: str
    city: str
    available: bool
    address: str
    amenities: List[str]
    photos: List[str]
    description: Dict[str, str]
    agent: int
    created_at: str = datetime.now().isoformat()

class PropertyDatabase:
    def __init__(self, file_path: str = './rooms_database.json'):
        self.file_path = file_path
        self.properties = self._load_database()

    def _load_database(self) -> List[Dict]:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    def find_properties(self, criteria: Dict) -> List[Dict]:
        matches = []
        for prop in self.properties:
            if self._matches_criteria(prop, criteria):
                matches.append(prop)
        return matches

    def _matches_criteria(self, property: Dict, criteria: Dict) -> bool:
        try:
            if criteria.get('budget') and property['price'] > float(criteria['budget']):
                return False
            
            if criteria.get('rooms') and property['rooms'] != int(criteria['rooms']):
                return False
            
            if criteria.get('city') and property['city'].lower() != str(criteria['city']).lower():
                return False
            
            return True
        except (ValueError, TypeError) as e:
            print(f"Erreur dans _matches_criteria : {e}")
            return False