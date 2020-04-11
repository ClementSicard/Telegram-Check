from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.users import GetFullUserRequest
import configparser
import getpass
import datetime
import time

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Import API credentials
api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])
phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Set time delays, in seconds
DELAY = 1600
WAITING_TIME = 60

client = TelegramClient(username, api_id, api_hash)


def print_time_delta(name, time_delta):
    if time_delta <= datetime.timedelta(seconds=60):
        print(name + " is online")
    else:
        minutes_since = int(time_delta.total_seconds() / 60)
        if minutes_since > 60:
            hours_since, minutes_since = int(
                minutes_since / 60), minutes_since % 60
            if hours_since == 1:
                print(name + " was last seen 1h" +
                      str(minutes_since) + " ago")
            else:
                print(name + " was last seen " +
                      str(hours_since), " hours ago")
        else:
            if minutes_since == 1:
                print(name + " was last seen 1 minute ago")
            else:
                print(name + " was last seen " +
                      str(minutes_since) + " minutes ago")


async def main(phone):
    try:
        print("""
  ______       __                                             ______ __                 __  
 /_  __/___   / /___   ____ _ _____ ____ _ ____ ___          / ____// /_   ___   _____ / /__
  / /  / _ \ / // _ \ / __ `// ___// __ `// __ `__ \ ______ / /    / __ \ / _ \ / ___// //_/
 / /  /  __// //  __// /_/ // /   / /_/ // / / / / //_____// /___ / / / //  __// /__ / ,<   
/_/   \___//_/ \___/ \__, //_/    \__,_//_/ /_/ /_/        \____//_/ /_/ \___/ \___//_/|_|  
                    /____/                                                                  
""")
        await client.start()
        print("Client successfully created!")
        # Ensure you're authorized
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=getpass.getpass(prompt='Password: '))
        print("Successfully logged in!\n")

        username = config['Telegram']['looked_for_user']

        try:
            user = await client(GetFullUserRequest(username))
        except ValueError:
            print("No user with id", username, "was found\n")
            quit()

        name = user.user.first_name + " " + user.user.last_name
        already_sent = False

        print("Start of the loop. [CTRL + C] to exit !")
        # Persistent loop of the program
        while True:
            last_seen = user.user.status.was_online
            time_delta = datetime.datetime.now(
                tz=datetime.timezone.utc) - last_seen

            print_time_delta(name, time_delta)

            if not already_sent and time_delta <= datetime.timedelta(seconds=DELAY):
                await client.send_message("me", name + " is now online.")
                print("Message sent.")
                already_sent = True

            elif already_sent and time_delta > datetime.timedelta(seconds=DELAY):
                already_sent = False

            time.sleep(WAITING_TIME)
    except KeyboardInterrupt:
        await client.disconnect()
        quit()

with client:
    client.loop.run_until_complete(main(phone))
