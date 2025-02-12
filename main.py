import json
import asyncio
from pyrogram import Client, filters
from playwright.async_api import async_playwright

# Telegram Bot Credentials
API_ID = "28795512"  # Replace with your Telegram API ID
API_HASH = "c17e4eb6d994c9892b8a8b6bfea4042a"  # Replace with your Telegram API Hash
BOT_TOKEN = "7589052839:AAGPMVeZpb63GEG_xXzQEua1q9ewfNzTg50"  # Replace with your Bot Token

app = Client("youtube_cookies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def get_youtube_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless mode enabled
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.youtube.com/")
        await asyncio.sleep(10)  # Allow some time for page load

        cookies = await context.cookies()
        await browser.close()

        return cookies

@app.on_message(filters.command("getcookies"))
async def send_cookies(client, message):
    await message.reply_text("Logging into YouTube... Please wait!")

    cookies = await get_youtube_cookies()
    cookies_json = json.dumps(cookies, indent=4)

    with open("youtube_cookies.json", "w") as f:
        f.write(cookies_json)

    await message.reply_document("youtube_cookies.json", caption="Here are your YouTube cookies!")

    await message.reply_text("Cookies Extracted Successfully! ✅")

app.run()
