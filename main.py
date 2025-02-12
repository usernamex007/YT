import os
import json
import pickle
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from pyrogram import Client, filters

# Telegram Bot Credentials
API_ID = "28795512"  # Replace with your Telegram API ID
API_HASH = "c17e4eb6d994c9892b8a8b6bfea4042a"  # Replace with your Telegram API Hash
BOT_TOKEN = "7589052839:AAGPMVeZpb63GEG_xXzQEua1q9ewfNzTg50"  # Replace with your Bot Token

app = Client("youtube_cookies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

CLIENT_SECRETS_FILE = "client_secret.json"  # Google OAuth Client Secret File
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_youtube_cookies():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    credentials = flow.run_local_server(port=8080)

    # Save credentials for future use
    with open("youtube_token.pickle", "wb") as token:
        pickle.dump(credentials, token)

    cookies = {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_expiry": credentials.expiry.isoformat(),
    }

    with open("youtube_cookies.json", "w") as file:
        json.dump(cookies, file, indent=4)

    return cookies


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "👋 **Welcome to YouTube Cookies Bot!**\n\n"
        "🔹 Use /login to generate YouTube Cookies.\n"
        "🔹 Use /getcookies to get your cookies file.\n"
        "🔹 Use /help to see how it works. 😊"
    )


@app.on_message(filters.command("help"))
async def help_command(_, message):
    await message.reply_text(
        "🛠 **How to Get YouTube Cookies?**\n\n"
        "1️⃣ Use `/login` to start the authentication process.\n"
        "2️⃣ Click on the provided **Google Login Link** and sign in.\n"
        "3️⃣ After successful login, the bot will generate cookies.\n"
        "4️⃣ Use `/getcookies` to download your cookies file.\n\n"
        "⚡ **Tip:** Make sure you have added a valid `client_secret.json` file!"
    )


@app.on_message(filters.command("login"))
async def login(_, message):
    await message.reply_text("🔗 Open this link to login:\n\nhttp://localhost:8080/")
    cookies = get_youtube_cookies()
    await message.reply_text(f"✅ **YouTube Cookies Generated!**\n\n{cookies}")


@app.on_message(filters.command("getcookies"))
async def get_cookies(_, message):
    if os.path.exists("youtube_cookies.json"):
        await message.reply_document("youtube_cookies.json", caption="📂 **Your YouTube Cookies**")
    else:
        await message.reply_text("❌ No cookies found. Use /login first!")


app.run()
