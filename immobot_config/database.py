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
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create sample database if file doesn't exist
            sample_data = [
                {
                    "id": "prop1",
                    "rooms": 2,
                    "price": 5000,
                    "currency": "MAD",
                    "city": "Casablanca",
                    "available": True,
                    "amenities": {
                        "fr": ["parking", "wifi", "sécurité", "climatisation"],
                        "en": ["parking", "wifi", "security", "air conditioning"],
                        "ar": ["موقف سيارات", "واي فاي", "أمن", "تكييف"],
                        "da": ["parking", "wifi", "surveillance", "climatiseur"]
                    },
                    "photos": ["photo1.jpg", "photo2.jpg"],
                    "description": {
                        "fr": "Bel appartement moderne au centre-ville",
                        "en": "Beautiful modern apartment in city center",
                        "ar": "شقة جميلة وعصرية في وسط المدينة",
                        "da": "Appartement zwin o jdid f centre ville"
                    },
                    "address": {
                        "fr": "Maarif",
                        "en": "Maarif",
                        "ar": "المعاريف",
                        "da": "Maarif"
                    }
                },
                {
                    "id": "prop2",
                    "rooms": 3,
                    "price": 7000,
                    "currency": "MAD",
                    "city": "Rabat",
                    "available": True,
                    "amenities": {
                        "fr": ["parking", "piscine", "salle de sport", "sécurité"],
                        "en": ["parking", "pool", "gym", "security"],
                        "ar": ["موقف سيارات", "مسبح", "صالة رياضية", "أمن"],
                        "da": ["parking", "piscine", "sport", "surveillance"]
                    },
                    "photos": ["photo3.jpg", "photo4.jpg"],
                    "description": {
                        "fr": "Grand appartement avec vue sur mer",
                        "en": "Large apartment with sea view",
                        "ar": "شقة كبيرة مع إطلالة على البحر",
                        "da": "Appartement kbir o 3ando vue 3la l-bhar"
                    },
                    "address": {
                        "fr": "Hassan",
                        "en": "Hassan",
                        "ar": "حسان",
                        "da": "Hassan"
                    }
                }
            ]
            self._save_database(sample_data)
            return sample_data