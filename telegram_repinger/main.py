from telethon import TelegramClient, events
import logging
from images_manager import ImagesManager
from random import randint
from yaml import safe_load
from asyncio import run
from requests import post
from time import sleep
from sys import exit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telegram').setLevel(level=logging.WARNING)

try: TELEGRAM_DATA, IMGUR_DATA, CHANNELS = list(safe_load(open("settings.yaml")).values())
except Exception as e:
    logging.critical(f"Unable to load settings.yaml ({type(e).__name__}: {str(e)})")
    exit(0)

image_manager = False if not IMGUR_DATA["id"] else ImagesManager(IMGUR_DATA["id"], IMGUR_DATA["secret"])
client = TelegramClient("glizzy-monitor", TELEGRAM_DATA["id"], TELEGRAM_DATA["hash"]) 

@client.on(events.NewMessage())
async def handler(event):  
    try: channel_id = event.peer_id.channel_id
    except: return # Private message, ignoring
    
    # Message not from a monitored channel, ignoring
    if channel_id not in list(CHANNELS): return  
    
    channel_name = event.chat.title
    logging.info(f"New message detected - {channel_name}") 
    try:
        hook_data = { 
            "content": None if not hasattr(event.message, "message") else event.message.message,
            "username": channel_name
        } 
        if image_manager:
            # Load channel image
            avatar_url = image_manager.load_channel_image(channel_id)
            if not avatar_url: 
                avatar_url = image_manager.upload_channel_image(
                    channel_id, await client.download_profile_photo(channel_id, f"./images/{channel_id}")
                )
            hook_data["avatar_url"] = avatar_url

            # Check and load image
            if event.photo:
                image = image_manager.upload_image(await client.download_media(event.media, f"./images/img-{randint(1, 9 * 10e12)}") )
                actual_content = hook_data['content']
                if actual_content: hook_data['content'] = f"{actual_content}\n\n{image}"
                else: hook_data['content'] = image  
    except Exception as e:
        # Unexcepted error parsing message. Will probably never happen
        logging.warning(f"Unable to load message ({type(e).__name__}: {str(e)})")
        return 
        
    # Send webhook
    logging.info("Sending webhook...") 
    while 1:
        try: response = post(CHANNELS.get(channel_id), json=hook_data).status_code
        except Exception as e:
            logging.warning(f"Unable to send webhook ({type(e).__name__}: {str(e)})") 
            # Let's sleep some seconds and then retry
            sleep(3)
            return
        else: break
    logging.info(f"Webhook respomse -> {response}")



async def start_telegram() -> None:
    await client.start()  
    logging.info(f"Listening...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    run(start_telegram())