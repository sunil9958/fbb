import requests
import aria2p
from datetime import datetime
from status import format_progress_bar
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, time
import logging


aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)
async def download_video(url, reply_msg, user_mention, user_id):
    response = requests.get(f"http://ashlynn.serv00.net/terapre.php/?url={url}")
    response.raise_for_status()
    data = response.json()

    resolutions = data["response"][0]["resolutions"]
    fast_download_link = resolutions["Fast Download"]
    hd_video_link = resolutions["HD Video"]
    thumbnail_url = data["response"][0]["thumbnail"]
    video_title = data["response"][0]["title"]

    try:
        # Attempt to download the video from the "Fast Download" link.
        download = aria2.add_uris([fast_download_link])
        start_time = datetime.now()

        while not download.is_complete:
            download.update()
            percentage = download.progress
            done = download.completed_length
            total_size = download.total_length
            speed = download.download_speed
            eta = download.eta
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()

            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=done,
                total_size=total_size,
                status="Downloading",
                eta=eta,
                speed=speed,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=download.gid
            )
            await reply_msg.edit_text(progress_text)
            await asyncio.sleep(2)

        if download.is_complete:
            file_path = download.files[0].path

            thumbnail_path = "thumbnail.jpg"
            thumbnail_response = requests.get(thumbnail_url)
            with open(thumbnail_path, "wb") as thumb_file:
                thumb_file.write(thumbnail_response.content)

            await reply_msg.edit_text("ᴜᴘʟᴏᴀᴅɪɴɢ...")

            return file_path, thumbnail_path, video_title
        else:
            raise Exception("Download failed")
    except Exception as e:
        logging.error(f"Download failed: {e}")
        # If download fails, send buttons for manual download links
        join_button = InlineKeyboardButton("🌐 Fast Download", url=fast_download_link)
        hd_button = InlineKeyboardButton("📺 HD Video", url=hd_video_link)
        reply_markup = InlineKeyboardMarkup([[join_button, hd_button]])

        await reply_msg.reply_text(
            "❌ **Oops, something went wrong with the download!**\n\n"
            "You can manually choose the server to download the video from the links below:",
            reply_markup=reply_markup
        )
        return None, None, None  # Indicate that download failed by returning None values


async def upload_video(client, file_path, thumbnail_path, video_title, reply_msg, collection_channel_id, user_mention, user_id, message):
    file_size = os.path.getsize(file_path)
    uploaded = 0
    start_time = datetime.now()
    last_update_time = time.time()

    async def progress(current, total):
        nonlocal uploaded, last_update_time
        uploaded = current
        percentage = (current / total) * 100
        elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
        
        if time.time() - last_update_time > 2:
            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=current,
                total_size=total,
                status="Uploading",
                eta=(total - current) / (current / elapsed_time_seconds) if current > 0 else 0,
                speed=current / elapsed_time_seconds if current > 0 else 0,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=""
            )
            try:
                await reply_msg.edit_text(progress_text)
                last_update_time = time.time()
            except Exception as e:
                logging.warning(f"Error updating progress message: {e}")

    with open(file_path, 'rb') as file:
        collection_message = await client.send_video(
            chat_id=message.chat.id,
            video=file,
            caption=f"✨ {video_title}\n👤 ʟᴇᴇᴄʜᴇᴅ ʙʏ : {user_mention}\n📥 ᴜsᴇʀ ʟɪɴᴋ: tg://user?id={user_id}",
            thumb=thumbnail_path,
            progress=progress
        )
        await asyncio.sleep(1)
        await message.delete()
        await message.reply_sticker("CAACAgIAAxkBAAEZdwRmJhCNfFRnXwR_lVKU1L9F3qzbtAAC4gUAAj-VzApzZV-v3phk4DQE")

    await reply_msg.delete()

    os.remove(file_path)
    os.remove(thumbnail_path)
    return collection_message.id
