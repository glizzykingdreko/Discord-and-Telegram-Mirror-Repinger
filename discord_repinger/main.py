import logging
from discord import Client
from yaml import safe_load
from asyncio import run
from requests import post
from time import sleep
from sys import exit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('discord').setLevel(level=logging.WARNING)

try: DISCORD_TOKEN , CHANNELS = list(safe_load(open("settings.yaml")).values())
except Exception as e:
    logging.critical(f"Unable to load settings.yaml ({type(e).__name__}: {str(e)})")
    exit(0)

class TrampaRepinger(Client):
    async def on_ready(self):
        logging.info(f'Logged in') # in as {self.user}

    async def on_message(self, message):
        # Message from the user bot, ignoring
        if message.author == self.user: return

        # Load channel ID
        channel_id = message.channel.id

        # Message not from a monitored channel, ignoring
        if channel_id not in list(CHANNELS): return  

        # Parse into webhook 
        logging.info(f"New message detected - {message.channel.name}")
        hooks_data = []
        try:
            # Format message / embed as webhook
            username, avatar_url = None if not message.author else str(message.author).replace("#0000", ""), str(message.author.avatar_url)
            hooks_data.append({
                "content": None if not message.content else message.content, 
                "username": username,
                "avatar_url": avatar_url,
                "embeds": [{
                    "title": None if not embed.title else embed.title, 
                    "url": None if not embed.url else embed.url,
                    "description": None if not embed.description else embed.description, 
                    "color": None if not embed.color else embed.color.value,
                    "author": None if not embed.author else {"name": embed.author.name, "url": None if not embed.footer.icon_url else embed.footer.icon_url, "icon_url": None if not embed.footer.icon_url else embed.footer.icon_url},
                    "thumbnail": None if not embed.thumbnail else {"url": embed.thumbnail.url},
                    "fields": [{"name": fld.name, "value": fld.value, "inline": fld.inline} for fld in embed.fields],
                    "image": None if not embed.image else {"url": embed.image.url},
                    "footer": None if not embed.footer else {"text": embed.footer.text, "icon_url": None if not embed.footer.icon_url else embed.footer.icon_url},
                    "timestamp": None if not embed.timestamp else str(embed.timestamp)
                } for embed in message.embeds]
            }) 

            # Send any other type of file as link in a different webhook
            for attach in message.attachments: hooks_data.append({"username": username, "avatar_url": avatar_url, "content": attach.url})
        except Exception as e:
            # Unexcepted error parsing message. Will probably never happen
            logging.warning(f"Unable to load message ({type(e).__name__}: {str(e)})")
            return
        
        # Check and remove for empty ones just in case
        good_hooks = [hook for hook in hooks_data if hook['content'] or len(hook['embeds']) > 0] 
        
        # Send webhook
        for n, hook_data in enumerate(good_hooks, 1):
            logging.info(f"({n}/{len(good_hooks)}) Sending webhook...")
            while 1:
                try: response = post(CHANNELS.get(channel_id), json=hook_data).status_code
                except Exception as e:
                    logging.warning(f"Unable to send webhook ({type(e).__name__}: {str(e)})") 
                    # Let's sleep some seconds and then retry
                    sleep(3)
                    return
                else: break
            logging.info(f"({n}/{len(good_hooks)}) Webhook respomse -> {response}")


if __name__ == '__main__':
    logging.info("Starting...") 
    client = TrampaRepinger()
    run(client.run(DISCORD_TOKEN))