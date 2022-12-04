
from imgurpython import ImgurClient
from pathlib import Path
from os.path import exists
from json import loads, dumps
from typing import Union

class ImagesManager:
    def __init__(self, client_id: str, client_secret: str) -> None: 
        # Inizialize Imgur Client
        self.client = ImgurClient(client_id, client_secret)

        # Create images folder if needed
        Path(f"./images/temp").mkdir(parents=True, exist_ok=True)

        # Create (if don't exists) and load manager file
        if not exists("./images/manager.json"): self.update_manager({})
        self.stored_channel_images = loads(open("./images/manager.json", "r").read())
        pass
    
    def update_manager(self, data: dict) -> None: 
        m = open("./images/manager.json", "w") 
        m.write(dumps(data))
        m.close()

    def load_channel_image(self, channel_id: Union[str, int]) -> Union[str, bool]:
        return self.stored_channel_images.get(str(channel_id))
    
    def upload_channel_image(self, channel_id: Union[str, int], image_path: str) -> str:
        
        # Check if already loaded on Imgur just in case
        saved = self.load_channel_image(channel_id)
        if saved: return saved

        # Upload on Imgur
        url = self.client.upload_from_path(image_path)['link']
        self.stored_channel_images[str(channel_id)] = url 
        self.update_manager(self.stored_channel_images)
        return url
    
    def upload_image(self, image_path: str) -> str: 
        # Upload on Imgur
        url = self.client.upload_from_path(image_path)['link'] 

        # Delete the downloaded file and return Imgur url
        Path(image_path).unlink()
        return url