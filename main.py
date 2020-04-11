from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.contacts import GetContactsRequest
import configparser
import getpass
import asyncio
import datetime
from telethon.tl.functions.users import GetFullUserRequest
import time

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Import API credentials
api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])
phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)


def message_time_delta(name, time_delta):
    message = ""
    if time_delta <= datetime.timedelta(seconds=60):
        message += name + " is online"
    else:
        minutes_since = int(time_delta.total_seconds() / 60)
        if minutes_since > 60:
            hours_since, minutes_since = int(
                minutes_since / 60), minutes_since % 60 + 1
            if hours_since == 1:
                message += name + " was last seen 1h" + \
                    str(minutes_since) + " ago"
            else:
                message += name + " was last seen " + \
                    str(hours_since), "hours ago"
        else:
            if minutes_since == 1:
                message += name + " was last seen 1 minute ago"
            else:
                message += name + " was last seen " + \
                    str(minutes_since) + " minutes ago"
    return message


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

    username = config['Telegram']['looked_for_user']

    try:
        user = await client(GetFullUserRequest(username))
    except ValueError:
        print("No user with id", username, "was found\n")
        quit()

    name = user.user.first_name + " " + user.user.last_name
    while True:
        last_seen = user.user.status.was_online
        time_delta = datetime.datetime.now(
            tz=datetime.timezone.utc) - last_seen
        print(message_time_delta(name, time_delta))
        time.sleep(60)

with client:
    client.loop.run_until_complete(main(phone))
