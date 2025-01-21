from enum import Enum
from typing import Dict, Optional
import re

class Language(Enum):
    FR = "fr"
    EN = "en"
    AR = "ar"
    DA = "da"  # Darija

class LanguageManager:
    TRANSLATIONS = {
        "greeting": {
            "fr": "Bonjour! Je suis un bot qui peut vous aider à trouver une chambre selon vos critères. Pour commencer, combien de chambres recherchez-vous?",
            "en": "Hello! I'm a bot that can help you find a room according to your criteria. To start with, how many rooms are you looking for?",
            "ar": "مرحبا! أنا بوت يمكنني مساعدتك في العثور على غرفة وفقًا لمعاييرك. للبدء، كم عدد الغرف التي تبحث عنها؟",
            "da": "salam m3ak immobot ana n9der n3awnek tl9a dar ila knti baghi tkri. bach nbdaw golya 3afak chhal mn bit bghiti fdar?"
        },
        "no_ask_rooms": {
            "fr": "Je n'ai pas compris le nombre de chambres. Veuillez indiquer un nombre (exemple: 2 chambres).",
            "en": "I didn't understand the number of rooms. Please indicate a number (example: 2 rooms).",
            "ar": "لم أفهم عدد الغرف. يرجى تحديد عدد (مثال: 2 ).",
            "da": "Mafahmtch 3afak chhal mn bit bghiti fdar. 3awd 9olya men 3afak (matalan: 2 byot)."

        },
        "ask_budget": {
            "fr": "Quel est votre budget maximum (en dirham ou dollars)?",
            "en": "What is your maximum budget (in dirhams or dollars)?",
            "ar": "ما هي ميزانيتك القصوى (بالدرهم أو الدولار)؟",
            "da": "Ch7al 3ndek f budget dyalek (b derham wla dollar)?"
        },
        "no _ask_budget":{
            "fr": "Je n'ai pas compris le budget. Veuillez l'indiquer en dirham (exemple: 1500 dh).",
            "en": "I didn't understand the budget. Please indicate it in dirham (example: 1500 dh).",
            "ar": "لم أفهم الميزانية. يرجى تحديدها بالدرهم (مثال: 1500 درهم).",
            "da": "Mafahmtch lbudget li 9lti. 3awd 9olya men fadlek b derham (matalan: 1500 dh)."
        },
        "ask_city": {
            "fr": "Dans quelle ville recherchez-vous?",
            "en": "In which city are you looking?",
            "ar": "في أي مدينة تبحث؟",
            "da": "F ina mdina katqalleb?"
        },
        "no_ask city":{
            "fr": "Je n'ai pas compris la ville. Veuillez réessayer.",
            "en": "I didn't understand the city. Please try again.",
            "ar": "لم أفهم المدينة. يرجى المحاولة مرة أخرى.",
            "da": "Mafahmtch ina mdina 9sdti. 3awd 9olya men fadlek."

        },
        "no_results": {
            "fr": "Désolé, aucun logement ne correspond à vos critères.",
            "en": "Sorry, no accommodation matches your criteria.",
            "ar": "عذراً، لا يوجد سكن يطابق معاييرك.",
            "da": "Smeh liya, mal9ina 7ta chi dar kifma bghiti."
        },
        "error": {
            "fr": "Une erreur s'est produite. Veuillez réessayer.",
            "en": "An error occurred. Please try again.",
            "ar": "حدث خطأ. يرجى المحاولة مرة أخرى.",
            "da": "Kayn chi mochkil. 3awd men fadlek."
        }
    }

    GREETINGS = {
        "fr": ["bonjour", "salut", "bonsoir", "bnj","oui","ok",],
        "en": ["hi", "hello", "hey", "good morning","yes","yeah","ok","okay","sure"],
        "ar": ["مرحبا", "السلام عليكم", "صباح الخير", "سلام","السلام","حسنا","نعم"],
        "da": ["salam", "slm", "sabah lkhir", "labas","ok","wakha","safi"]
    }

    # Mots clés pour détecter le darija
    DARIJA_WORDS = [
        "ch7al", "wa9t", "bghit", "kanqalleb","kan9lb", "3nd", "m3a", "dyal", "dyalk","slm","khasni"
        "kayn", "zwin", "zwina", "kbir", "kbira", "sghir", "sghira","salam", "slm", "sabah lkhir", "labas","ok","wakha","safi","ana",
    ]

    @staticmethod
    def detect_language(message: str) -> Language:
        message_lower = message.lower()
        
        # Detect Darija
        for word in LanguageManager.DARIJA_WORDS:
            if word in message_lower:
                return Language.DA
                
        # Detect Arabic
        if re.search(r'[\u0600-\u06FF]', message):
            return Language.AR
            
        # Detect French
        french_patterns = r'\b(bonjour|salut|recherche|chambre|prix|slt|bnj|oui|je|tu|peut|jai)\b'
        if re.search(french_patterns, message_lower):
            return Language.FR
            
        return Language.EN

    @staticmethod
    def get_message(key: str, lang: Language) -> str:
        return LanguageManager.TRANSLATIONS[key][lang.value]

    @staticmethod
    def is_greeting(message: str) -> bool:
        msg_lower = message.lower().strip()
        all_greetings = []
        for greetings in LanguageManager.GREETINGS.values():
            all_greetings.extend(greetings)
        return msg_lower in all_greetings

    @staticmethod
    def extract_number(message: str, lang: Language) -> Optional[int]:
        patterns = {
            "fr": r'(\d+)\s*(chambre?|chambres?|pièces?)',
            "en": r'(\d+)\s*(for|rooms?|bedrooms?|bedroom?|room?|pieces?)',
            "ar": r'(\d+)\s*(غرف|غرفة)',
            "da": r'(\d+)\s*(bit|biyout|byout|chombrat|chambre|غرفة)'  # Ajout des mots en darija
        }
        
        match = re.search(patterns[lang.value], message.lower())
        return int(match.group(1)) if match else None

    @staticmethod
    def extract_budget(message: str) -> Optional[int]:
        # Support pour le darija ajouté (dh, derham, drahm)
        pattern = r'(\d+)\s*(dollars?|dirham|dh|derham|drahm|usd|\$|درهم|دولار)'
        match = re.search(pattern, message.lower())
        return int(match.group(1)) if match else None
        
    @staticmethod
    def extract_city(message: str, lang: Language) -> Optional[str]:
        pattern =r'(?:in|a|at|for|dans|f|fi|fmdint|fmdinat|à|في|فى|ف)\s+([A-Za-z\s]+?)(?=\s+|$|,|\sin|\sat)'
        match = re.search(pattern, message.lower(), re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

