from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import configparser
import json
import getpass
import asyncio

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Import API credentials
api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])
phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)


async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=getpass.getpass(prompt='Password: '))

    me = await client.get_me()


with client:
    client.loop.run_until_complete(main(phone))
