# Telegram-Check

Here is a Python script I developed to send yourself a Telegram message anytime a contact of your choice gets online.

You will need a few you things to set it up :

## 1. Create an app and save API credentials

Create a Telegram app [here](https://my.telegram.org/apps), fill in the form and look for `api_id` and `api_hash` . The idea is not to store them in clear in your code, so create a `config.ini` file in the same directory, with the following structure :

``` 
[Telegram]
# no need for quotes

# you can get telegram development credentials in telegram API Development Tools
api_id = xxxxxxx
api_hash = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# use your full phone number including + and country code
phone = xxxxxxxxxxxx
username = xxxxxxxxxxxx

# Can be anything : phone number, Telegram username, UserID, ...
looked_for_user = xxxxxxxxxx
```

Fill it with your own `api_id` and `api_hash` , fill in your phone number and Telegram username as well. Make sure to check that the user you want to know if it is online is **part of your contacts list**

## 2. Setup your Python environment

You will need a few extensions, and the main one is [Telethon](https://docs.telethon.dev/en/latest/#), a Python library to converse with Telegram API in an easy way. Install all dependencies running these command from a terminal (make sure you have `pip` installed)

``` 
pip install telethon
pip install configparser
```

Everything is ready, just run it navigating to the folder where `main.py` is located and type the following command in terminal :

``` 
python main.py
```

