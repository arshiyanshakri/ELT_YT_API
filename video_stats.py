import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")    ## To set path of .env file

API_KEY=os.getenv("API_KEY")         ## TO get API Key from .env file
CHANNEL_HANDLE = "MrBeast"

def get_PlaylistID():
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

    response = requests.get(url)
    try:

        # print(response)
        response.raise_for_status()     ## Try 200 as response
        data = response.json()          ## Convert response to JSON
        # print(data)
        # print(json.dumps(data, indent=4))

        channel_items = data['items'][0]
        playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']    ## Picks PlaytistID

        print(playlist_id)
        return playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":             ## This helps to prevent code execution from any other module
    get_PlaylistID()
