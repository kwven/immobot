# ImmoBot - WhatsApp Real Estate Assistant

ImmoBot is a multilingual WhatsApp chatbot designed to help users find real estate properties based on their preferences. It supports multiple languages including French (FR), English (EN), Arabic (AR), and Moroccan Darija (DA).

## Features

- 🌐 Multilingual support (French, English, Arabic, Moroccan Darija)
- 🏠 Property search based on multiple criteria (rooms, budget, city)
- 💬 Natural language processing for user interactions
- 🔒 Secure webhook implementation with signature verification
- 📝 Detailed property information including amenities and photos

## Prerequisites

Before running the bot, make sure you have:

1. Python 3.7 or higher installed
2. A WhatsApp Business API account
3. Facebook Developer account with WhatsApp integration set up
4. Required environment variables (see Configuration section)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kwven/immobot.git
cd immobot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
check req.txt file to understand
```

## Configuration

1. Create a `.env` file in the root directory with the following variables:
```
you can check exp.env file to understand
here is a documentation to understand how to work with whatsapp API

https://developers.facebook.com/docs/whatsapp/cloud-api
```

2. Set up your property database by creating a `rooms_database.json` file with the following structure:
```json
[
  {
    "id": "unique_id",
    "rooms": 2,
    "price": 5000,
    "currency": "MAD",
    "city": "Casablanca",
    "available": true,
    "address": "Example Address",
    "amenities": {
      "en": ["Parking", "Pool"],
      "fr": ["Parking", "Piscine"],
      "ar": ["موقف سيارات", "مسبح"],
      "da": ["Parking", "Piscine"]
    },
    "photos": ["photo_url_1", "photo_url_2"],
    "description": {
      "en": "Property description in English",
      "fr": "Description en français",
      "ar": "وصف بالعربية",
      "da": "Description en darija"
    },
    "agent": "agent_phone_number"
  }
]
```

## Running the Bot
1. Set up webhook URL in your WhatsApp Business API settings:
```
you can use port of vscode to test or you should get a domain name to get messages like ngrok or vercel

https://your-domain/webhook
```

2. start with first_test.py:
```python
# Run first_test.py
python first_test.py
```
Receive & Reply to Messages:
Send a message to your WhatsApp number. The bot will:
send you a hello for testing 
you should reply to the bot 
after that you will get hi immobot

3.Start the Flask server:
```bash
python run.py
```

## Bot Flow

1. User sends a greeting message
2. Bot detects language and asks for number of rooms
3. User specifies rooms, bot asks for budget
4. User specifies budget, bot asks for preferred city
5. Bot searches database and returns matching properties
6. User can restart the search by sending a greeting message

## Security Features

- Webhook signature verification using SHA256
- Environment variable configuration
- Request validation and sanitization
- Error handling and logging

## Error Handling

The bot includes comprehensive error handling:
- Input validation for all user responses
- Secure webhook verification
- Database connection error handling
- API response validation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- WhatsApp Business API
- Flask framework
- Python community

## Support

For support, email lamrania765@gmail.com or create an issue in the repository.