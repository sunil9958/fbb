import logging
from pyrogram import Client, filters
import asyncio
import time
import random
import re
import requests
from web import keep_alive
from video import download_video, upload_video
from shortzy import Shortzy
from pymongo import MongoClient
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import present_user, add_user, full_userbase, del_user, db_verify_status, db_update_verify_status, is_premium, add_premium, remove_premium
import string
logging.basicConfig(level=logging.INFO)

mongo_url = 'mongodb+srv://Sunilvs2024:Sunilvs2024@cluster0.fdkbx.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(mongo_url)
db = client['Sunilvs2024']
channel_id = '@Diskwala_Links'
users_collection = db['users']
VERIFY_EXPIRE = 43200
IS_VERIFY = "True"
access_token = ''
username = 'Sunil_v99'
BOT_API_TOKEN = '7665684522:AAHPhv9J7br7vBkQWxs_DxjMZpXzSKG_5Eg'
API_ID = '1194196'
dump_id = '-1002172770176' # idhar kuch nhi dalna or hatana bhi nhi
fsub_id = '@Loot_and_Earn_Money'
API_HASH = '15d9b47380ff02c8ea404f623461a081'
SHORTLINK_URL = 'modijiurl.com'
SHORTLINK_API = '20bb8e8e7b6fb1ccfa4165aa4b55036c44f75ced'
ADMINS = 602583967
def addu(user_id):
    """
    Sends a request to add a user to the broadcast service.

    Args:
        access_token (str): The access token generated from @tele_servicebot.
        bot_token (str): The bot's token.
        user_id (str or int): The Telegram user ID to add.
    """
    url = "https://api.teleservices.io/Broadcast/adduser/"
    headers = {
        "content-type": "application/json"
    }
    body = {
        "access_token": access_token,
        "bot_token": BOT_API_TOKEN,
        "user_id": user_id
    }

    # Sending the POST request
    try:
        requests.post(url, json=body, headers=headers)
    except Exception as e:
        print("An error occurred:", e)
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_API_TOKEN)
def get_exp_time(seconds):
    periods = [('days', 86400), ('hours', 3600), ('mins', 60), ('secs', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name} '
    return result
async def get_shortlink(url, api, link):
    shortzy = Shortzy(api_key=api, base_site=url)
    link = await shortzy.convert(link)
    return link
def broadcast(cap):
    url = "https://api.teleservices.io/Broadcast/broadcast/"
    
    # Payload for the POST request
    payload = {
        "method": 'sendMessage',
        "text": cap,
        "type": "text",
        "access_token": access_token,
        "bot_token": BOT_API_TOKEN,
        "admin": ADMINS,
    }
    
    # Headers for the request
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send the request without handling the response
    try:
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print("An error occurred:", e)

@app.on_message(filters.command("broadcast") & filters.user(ADMINS))
def handle_broadcast(client, message):
    if len(message.command) > 1:
        broadcast_message = message.text.split(maxsplit=1)[1]
        broadcast(broadcast_message)
    else:
        message.reply_text("Please provide a message to broadcast, e.g., `/broadcast Your message here`.")
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    addu(user_id)
    # Add user to the database if not already present
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            logging.error(f"Failed to add user {user_id} to the database: {e}")

    # Fetch verification status
    verify_status = await db_verify_status(user_id)
    # Handle token verification
    text = message.text
    if "verify_" in text:
        _, token = text.split("_", 1)
        logging.info(f"Extracted token: {token}")
        if verify_status["verify_token"] != token:
            logging.warning(f"Invalid or expired token for user {user_id}")
            return await message.reply(
    "❌ **Token Invalid or Expired!**\n\n"
    "It seems your token is no longer valid. Don't worry—just click **/start** to try again and get a new token. 🔄"
)
        await db_update_verify_status(user_id, {**verify_status, 'is_verified': True, 'verified_time': time.time()})
        logging.info(f"User {user_id} verified successfully")
        return await message.reply(
    "✅ **Success! Your Token Has Been Verified!**\n\n"
    "Your token is now valid for the next **12 hours**. Enjoy uninterrupted access to all bot features! 🚀"
)
    # Handle premium user
    if await is_premium(user_id):
        return await handle_premium_user(client, message, user_mention)

    # Handle verified non-premium user
    if verify_status["is_verified"]:
        return await handle_verified_non_premium_user(client, message, user_mention)

    # Handle non-premium user verification
    return await handle_non_premium_user(client, message, verify_status, user_id, user_mention)
async def handle_premium_user(client, message, user_mention):
    """Handles the response for premium users."""
    reply_message = (
        f"👋 Hey there, {user_mention}!\n\n"
        "🚀 **Welcome to the Most Advanced TeraBox Downloader Bot!**\n\n"
        "🌟 **Why Choose Me?**\n"
        "- **Fastest and Most Powerful** downloader bot on Telegram ⚡️\n"
        "- **Completely FREE** forever—no hidden charges! 🆓\n"
        "- Download TeraBox files instantly and get them sent directly to you 🎥📁\n"
        "- Available **24/7**, anytime, anywhere ⏰\n\n"
        "💎 **You're enjoying premium access, unlocking all features and the best experience!**\n\n"
        "**Join our community and explore even more!** 👇"
    )
    join_button = InlineKeyboardButton("🌐 Join Community ❤️", url="https://t.me/teleservices_api")
    developer_button = InlineKeyboardButton("👨‍💻 Developer ⚡️", url="https://t.me/techscoder")
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button]])
    await message.reply_text(reply_message, reply_markup=reply_markup)
async def handle_verified_non_premium_user(client, message, user_mention):
    """Handles the response for verified non-premium users."""
    reply_message = (
        f"👋 Hey there, {user_mention}!\n\n"
        "🚀 **Welcome to the Most Advanced TeraBox Downloader Bot!**\n\n"
        "🌟 **Enjoy the Free Version!**\n"
        "- **Fast and Reliable** downloader bot on Telegram ⚡️\n"
        "- **Free to use**, supported by our community 🆓\n"
        "- Download TeraBox files and access essential features 🎥📁\n"
        "- Available **24/7**, but with some limitations ⏰\n\n"
        "💎 **Want to unlock premium access and get the best experience?**\n"
        "Upgrade to premium for unlimited features, faster downloads, and priority support! 🌟\n\n"
        "**Join our community and learn more!** 👇"
    )
    join_button = InlineKeyboardButton("🌐 Join Community ❤️", url="https://t.me/teleservices_api")
    upgrade_button = InlineKeyboardButton("💎 Upgrade to Premium ⚡️", url="https://t.me/techscoder")
    reply_markup = InlineKeyboardMarkup([[join_button, upgrade_button]])
    await message.reply_text(reply_message, reply_markup=reply_markup)
async def handle_non_premium_user(client, message, verify_status, user_id, user_mention):
    """Handles the response for non-premium users requiring verification."""
    # Generate and assign a new verification token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    logging.info(f"{token}")
    link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{username}?start=verify_{token}')
    await db_update_verify_status(user_id, {**verify_status, 'verify_token': token, 'link': link})
    message_text = (
        f"🔒 **Verification Required!**\n\n"
        "To access the bot, complete the simple verification process using the link below.\n\n"
        "🔗 Click the button to verify:\n"
    )
    token_button = InlineKeyboardButton("🔑 Verify Now", url=link)
    tutorial_button = InlineKeyboardButton("📚 How to Verify", url="https://t.me/TeleServices_Bots/96")
    reply_markup = InlineKeyboardMarkup([[token_button], [tutorial_button]])
    await message.reply_text(message_text, reply_markup=reply_markup)

@app.on_message(filters.command("check"))
async def check_command(client, message):
    user_id = message.from_user.id

    verify_status = await db_verify_status(user_id)
    logging.info(f"Verify status for user {user_id}: {verify_status}")

    if verify_status['is_verified']:
        expiry_time = get_exp_time(VERIFY_EXPIRE - (time.time() - verify_status['verified_time']))
        await message.reply(
    f"✅ **Token Verified!**\n\n"
    f"Your token is valid and will remain active for **{expiry_time}**.\n\n"
    "Enjoy uninterrupted access to the bot's features! 🚀"
)

    else:
        await message.reply(
    "⚠️ **Token Not Verified or Expired!**\n\n"
    "It seems your token is either invalid or has expired. Don't worry—you can easily generate a new one! 🕒\n\n"
    "🔄 Simply type **/start** to begin the verification process and regain access.\n\n"
    "💡 **Tip:** Verifying your token takes just a few moments and unlocks all premium features for you!"
)


async def is_user_member(client: Client, user_id: int) -> bool:
    try:
        # Ensure the channel_id is correctly passed as username or chat ID
        channel = await client.get_chat(channel_id)

        # Fetch the member's status in the channel
        member = await client.get_chat_member(channel.id, user_id)
        
        # Log the member's status
        logging.info(f"User {user_id} membership status in {channel_id}: {member.status}")

        # Check if the user is a member, admin, or owner
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error checking membership status for user {user_id} in channel {channel_id}: {e}")
        return False

def is_terabox_link(link):
    keywords = ["terabox", "terafileshare", "1024tera", "terasharelink", "xnxx"]
    return any(keyword in link.lower() for keyword in keywords)
@app.on_message(filters.command("plan") & filters.incoming)
async def send_pro_plan(client: Client, message: Message):
    user_mention = message.from_user.mention
    plan_text = f"""
Hᴇʏ! {user_mention}

Pʀɪᴄᴇ 💸 » ₹𝟻𝟶  
⚠️ Pʟᴀɴ ᴠᴀʟɪᴅɪᴛʏ ɪs » 𝟹𝟶 ᴅᴀʏs

Yᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ᴘᴀʏ ₹50 INR ᴛᴏ ʙᴜʏ ᴛʜᴇ Pʀᴏ ᴘʟᴀɴ.

Pᴀʏ Vɪᴀ Uᴘɪ » **xxxxxxx@ybl**

Nᴏᴛᴇ:  
Pʟᴇᴀsᴇ Dᴏɴ'ᴛ Fᴏʀɢᴇᴛ Tᴏ Vᴇʀɪғʏ Tʜᴇ Pᴀʏᴍᴇɴᴛ Bʏ Sᴇɴᴅɪɴɢ Tʜᴇ Sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ Tʜᴇ Bᴏᴛ Oᴡɴᴇʀ.

🌟 Pʀᴏ Usᴇʀ Fᴇᴀᴛᴜʀᴇs:  
1. Aᴄᴄᴇss ᴀᴅᴠᴀɴᴄᴇᴅ ғᴇᴀᴛᴜʀᴇs ᴏғ ᴛʜᴇ ʙᴏᴛ.  
2. Dᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏs ғʀᴏᴍ TᴇʀᴀBᴏx ʟɪɴᴋs.  
3. Uᴘʟᴏᴀᴅ ғɪʟᴇs ᴜᴘ ᴛᴏ 2GB.  
4. Nᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ ᴛᴏᴋᴇɴ ᴇᴠᴇʀʏ 24 ʜᴏᴜʀs.  
5. Pʀɪᴏʀɪᴛʏ sᴜᴘᴘᴏʀᴛ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇs.

Fᴏʀ ᴀɴʏ Pʀᴏʙʟᴇᴍ ᴀɴᴅ ᴅᴏᴜʙᴛ ᴛᴀʟᴋ ᴛᴏ Aᴅᴍɪɴ
"""
    # Inline keyboard with button
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📤 Send Screenshot", url="https://t.me/techscoder")
            ]
        ]
    )

    # Send the message
    await message.reply_text(plan_text, reply_markup=keyboard)

@app.on_message(filters.command("add") & filters.user(ADMINS))
async def handle_add_premium(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please specify the user ID. Usage: /add <user_id>")
        return

    try:
        user_id = int(message.command[1])
        await add_premium(user_id)
        await message.reply(f"User with ID {user_id} has been granted premium status.")
    except ValueError:
        await message.reply("Invalid user ID format.")

# Command handler for removing premium
@app.on_message(filters.command("rm")& filters.user(ADMINS))
async def handle_remove_premium(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please specify the user ID. Usage: /rm <user_id>")
        return

    try:
        user_id = int(message.command[1])
        await remove_premium(user_id)
        await message.reply(f"Premium status has been removed for user ID {user_id}.")
    except ValueError:
        await message.reply("Invalid user ID format.")

# Command handler for checking premium status
@app.on_message(filters.command("cp") & filters.user(ADMINS))
async def handle_check_premium(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please specify the user ID. Usage: /cp <user_id>")
        return

    try:
        user_id = int(message.command[1])
        is_premium_status = await is_premium(user_id)
        status_text = "has premium" if is_premium_status else "does not have premium"
        await message.reply(f"User with ID {user_id} {status_text}.")
    except ValueError:
        await message.reply("Invalid user ID format.")
@app.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats_command(client, message):
    total_users = users_collection.count_documents({})
    verified_users = users_collection.count_documents({"verify_status.is_verified": True})
    unverified_users = total_users - verified_users

    status = f"""
<b>📊 <u>Verification Statistics</u></b>

👥 <b>Total Users:</b> <code>{total_users}</code>  
✅ <b>Verified Users:</b> <code>{verified_users}</code>  
❌ <b>Unverified Users:</b> <code>{unverified_users}</code>  

💡 <i>Keep growing and ensure more users complete their verification for the best experience!</i>
"""

    await message.reply(status)
    return

def extract_links(text):
    url_pattern = r'(https?://[^\s]+)'  # Regex to capture http/https URLs
    links = re.findall(url_pattern, text)
    return links

@app.on_message(filters.text)
async def handle_message(client, message: Message):
    if message.from_user and message.from_user.is_bot:
        return

    user_id = message.from_user.id

    # Check if the user is already present in the database
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            logging.error(f"Failed to add user {user_id} to the database: {e}")

    user_mention = message.from_user.mention
    
    verify_status = await db_verify_status(user_id)

    # Check verification expiration
    if verify_status["is_verified"] and VERIFY_EXPIRE < (time.time() - verify_status["verified_time"]):
        await db_update_verify_status(user_id, {**verify_status, 'is_verified': False})
        verify_status['is_verified'] = False
        logging.info(f"Verification expired for user {user_id}")

    if not verify_status["is_verified"]:
        await message.reply_text("🔒 To access the bot, please verify your identity. Click /start to begin the verification process.")
        return

    is_member = await is_user_member(client, user_id)

    if not is_member:
        join_button = InlineKeyboardButton("Join ❤️🚀", url="https://t.me/Ashlynn_Repository")
        reply_markup = InlineKeyboardMarkup([[join_button]])
        await message.reply_text("✳️ To keep things secure and make sure only real users are accessing the bot, please subscribe to the channel below first.", reply_markup=reply_markup)
        return

    links = extract_links(message.text)
    
    if not links:
        await message.reply_text("Please send a valid link.")
        return

    for terabox_link in links:
        if not is_terabox_link(terabox_link):
            await message.reply_text(f"{terabox_link} is not a valid Terabox link.")
            continue
            
    reply_msg = await message.reply_text("🔄 Retrieving your TeraBox video. Your content is on the way, just a moment!")

    try:
        file_path, thumbnail_path, video_title = await download_video(terabox_link, reply_msg, user_mention, user_id)
        
        if file_path and thumbnail_path:  # Only proceed to upload if download was successful
            await upload_video(client, file_path, thumbnail_path, video_title, reply_msg, dump_id, user_mention, user_id, message)
        else:
            # If the download failed, reply accordingly and provide alternative download options.
            await reply_msg.delete()
    except Exception as e:
        logging.error(f"Error handling message: {e}")

if __name__ == "__main__":
    # keep_alive()
    app.run()
