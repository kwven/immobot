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