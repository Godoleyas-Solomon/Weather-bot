import requests
from telethon.sync import TelegramClient, events
from config import *


# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Bot started.')

@client.on(events.NewMessage(pattern='^/weather'))
async def weather(event):
    command, *city_words = event.message.text.split(' ')
    city = ' '.join(city_words)

    headers = {'key': api_key}
    response = requests.get(base, headers=headers, params={'q': city})
    data = response.json()

    if response.status_code == 200:
        city_desc = {
            'city': data['location']['name'],
            'country': data['location']['country'],
            'region': data['location']['region'],
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'wind': data['current']['wind_kph'],
            'time': data['location']['localtime']
        }


        response_text = f"Weather information for city🌆: {city_desc['city']}:\n\n" \
                        f"Country: {city_desc['country']}\n" \
                        f"Region🌍: {city_desc['region']}\n" \
                        f"Temperature🌡: {city_desc['temperature']}°C\n" \
                        f"Condition🍆: {city_desc['condition']}\n" \
                        f"Wind💨: {city_desc['wind']} kph\n" \
                        f"Time⌚: {city_desc['time']}"
        await event.respond(response_text)
    else:
        await event.respond("City not found")

with client:
    client.run_until_disconnected()