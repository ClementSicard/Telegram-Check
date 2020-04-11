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
perso_api_id = config['Telegram']['api_id']
perso_api_hash = str(config['Telegram']['api_hash'])
perso_phone = config['Telegram']['phone']
perso_username = config['Telegram']['username']

persoClient = TelegramClient(perso_username, perso_api_id, perso_api_hash)


async def main(phone):
    await persoClient.start()
    print("Client Created")
    # Ensure you're authorized
    if await persoClient.is_user_authorized() == False:
        await persoClient.send_code_request(phone)
        try:
            await persoClient.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await persoClient.sign_in(password=getpass.getpass(prompt='Password: '))

    me = await persoClient.get_me()
    contacts = []
    contacts_req = await persoClient(GetContactsRequest(hash=0))
    contacts.append(contacts_req.saved_count)
    contacts.extend(contacts_req.users)

    print("You have", contacts[0], "contacts in Telegram\n")
    while True:
        username = input("Enter username/phone number : ")
        try:
            user = await persoClient(GetFullUserRequest(username))
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


with persoClient:
    persoClient.loop.run_until_complete(main(perso_phone))
