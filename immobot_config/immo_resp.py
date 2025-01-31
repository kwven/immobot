from typing import Dict, Optional
from immobot_config.language import LanguageManager, Language

from immobot_config.database import PropertyDatabase

class immoBot:
    def __init__(self):
        self.lang_manager = LanguageManager()
        self.database = PropertyDatabase()
        self.current_state = "GREETING"
        self.current_language = Language.FR
        self.user_info = {
            'budget': None,
            'rooms': None,
            'city': None,
            'amenities': []
        }
    def process_message(self, message: str) -> str:
        try:
            # Detect language at the start of conversation
            if self.current_state == "GREETING":
                self.current_language = self.lang_manager.detect_language(message)

            response = self._handle_state(message)
            return self._format_response(response)

        except Exception as e:
            print(f"Error: {str(e)}")
            return self.lang_manager.get_message("error", self.current_language)

    def _handle_state(self, message: str) -> str:
        if self.current_state == "GREETING":
            if self.lang_manager.is_greeting(message):
                self.current_state = "ASK_ROOMS"
                return self.lang_manager.get_message("greeting", self.current_language)
            return self.lang_manager.get_message("no_ask_rooms", self.current_language)

        elif self.current_state == "ASK_ROOMS":
            rooms = self.lang_manager.extract_number(message, self.current_language)
            if rooms:
                self.user_info['rooms'] = rooms
                self.current_state = "ASK_BUDGET"
                return self.lang_manager.get_message("ask_budget", self.current_language)
            return self.lang_manager.get_message("no_ask_rooms", self.current_language)

        elif self.current_state == "ASK_BUDGET":
            budget = self.lang_manager.extract_budget(message)
            if budget:
                self.user_info['budget'] = budget
                self.current_state = "ASK_CITY"
                return self.lang_manager.get_message("ask_city", self.current_language)
            return self.lang_manager.get_message("no_ask_budget", self.current_language)

        elif self.current_state == "ASK_CITY":
            # Extract city from message
            city = self.lang_manager.extract_city(message, self.current_language)  # Ajout du paramètre language
            if city:
                self.user_info['city'] = city
                return self.search_properties()
            return self.lang_manager.get_message("no_ask_city", self.current_language)


    def _format_response(self, response: str) -> str:
        """Adds appropriate emojis and formatting based on language"""
        if self.current_language == Language.DA:
            # Add more friendly emojis for darija responses
            return response.replace("Error", "Mochkil 🤔").replace("Sorry", "Smeh liya 😕")
        return response
    def format_property(self, prop: Dict) -> str:
        currency = "DH" if prop['currency'] == "MAD" else "$"
        
        if self.current_language == Language.DA:
            return  (
                f"kayn had dar fiha {prop['rooms']} byout ojat f {prop['city']}\n"
                f" l'hay:  {prop['address']}\n"
                f"💰 Taman dylha : {prop['price']}{currency}\n"
                f"✨ oKayn fiha hta {', '.join(prop['amenities']['da'])}\n"
                f"📝hado m3lomat idafya 3liha: {prop['description']["da"]}\n"
                f"📸 hado tsawr dyal dar mn ldakhl: {', '.join(prop['photos'])}\n"
                f"hada num dyal l'wakil {prop['agent']}\n"
                )
        elif self.current_language == Language.FR:
            return (
                f"une appartement avec {prop['rooms']} chambres à {prop['city']}\n"
                f"Quartier: {prop['address']}\n"
                f"💰 Prix: {prop['price']}{currency}\n"
                f"✨ Il est équipé de: {', '.join(prop['amenities']['fr'])}\n"
                f"📝voila plus de détails: {prop['description']["fr"]}\n"
                f"📸 voila des photo de l'appartement: {', '.join(prop['photos'])}\n"
                f"voila le numéro de l'agent {prop.get('agent', 'non disponible')}\n"
            )
        elif self.current_language == Language.EN:
            return (
                f"I found a property with {prop['rooms']} rooms in {prop['city']}\n"
                f"📍 Area: {prop['address']}\n"
                f"💰 Price: {prop['price']}{currency}\n"
                f"✨ Amenities: {', '.join(prop['amenities']['en'])}\n"
                f"📝 Additional details:  {prop['description']["en"]}\n"
                f"📸 Here are some photos of the property: {', '.join(prop['photos'])}\n"
                f"here is the agent number {prop.get('agent', 'non disponible')}\n"
            )
        else:  # Arabic
            return (
                f"🏠 {prop['rooms']} غرف في {prop['city']}\n"
                f"📍 الحي: {prop['address']}\n"
                f"💰 السعر: {prop['price']}{currency}\n"
                f"✨ المرافق: {', '.join(prop['amenities']['ar'])}\n"
                f"📝 تفاصيل إضافية: {prop['description']["ar"]}\n"
                f"📸 بعض الصور للعقار:  {', '.join(prop['photos'])}\n"
                f"هذا رقم الوكيل {prop.get('agent', 'non disponible')}\n"
            )
        
    def search_properties(self) -> str:
        properties = self.database.find_properties(self.user_info)
        if not properties:
            self.reset_state()
            return f"{self.lang_manager.get_message("no_results", self.current_language)}"
        else:
            response = []
            for prop in properties:
                response.append(self.format_property(prop))
                self.reset_state()
            if self.current_language == Language.EN:
                return "Here are the properties that match your criteria:\n\n" + "\n\n".join(response) + "\nif you want to restart say okey"
            elif self.current_language == Language.AR:
                return "ها هي العقارات التي تتطابق مع معاييرك:\n\n" + "\n\n".join(response) + "\nاذا كنت تريد اعادة البداية قل حسنا"
            elif self.current_language == Language.FR:
                return "Voici les propriétés qui correspondent à vos critères:\n\n" + "\n\n".join(response) + "\nSi vous voulez recommencer, dites oui"

            elif self.current_language == Language.DA:
                return "hahoma les apparetement li 9it lik :\n\n" + "\n\n".join(response) + "\nlaknti baghi t3awd t9leb 9oliya safi "

    def reset_state(self) -> None:
        self.current_state = "GREETING"
        self.user_info = {
            'budget': None,
            'rooms': None,
            'city': None,
            'amenities': []
        }
