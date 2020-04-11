from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.contacts import GetContactsRequest
import configparser
import getpass
import asyncio
import datetime
from telethon.tl.functions.users import GetFullUserRequest

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
    contacts = []
    contacts_req = await client(GetContactsRequest(hash=0))
    contacts.append(contacts_req.saved_count)
    contacts.extend(contacts_req.users)

    print("You have", contacts[0], "contacts in Telegram\n")
    while True:
        username = input("Enter username/phone number : ")
        try:
            user = await client(GetFullUserRequest(username))
            break
        except ValueError:
            print("No user with name", username, "was found\n")

    last_seen = user.user.status.was_online
    time_delta = datetime.datetime.now(tz=datetime.timezone.utc) - last_seen
    name = user.user.first_name + " " + user.user.last_name
    if time_delta <= datetime.timedelta(seconds=60):
        print(name, "is online")
    else:
        minutes_since = int(time_delta.total_seconds() / 60)
        if minutes_since > 60:
            hours_since, minutes_since = int(
                minutes_since / 60), minutes_since % 60 + 1
            if hours_since == 1:
                print(name + " was last seen 1h" + str(minutes_since) + " ago")
            else:
                print(name, "was last seen", hours_since, "hours ago")
        else:
            if minutes_since == 1:
                print(name, "was last seen 1 minute ago")
            else:
                print(name, "was last seen", minutes_since, "minutes ago")


with client:
    client.loop.run_until_complete(main(phone))
