import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")    ## To set path of .env file

API_KEY=os.getenv("API_KEY")         ## TO get API Key from .env file
CHANNEL_HANDLE = "MrBeast"

maxResults = 50

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
    

def get_video_ids(playListId):

    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playListId}&key={API_KEY}"
    
    try:

        while True:
            url = base_url
            if pageToken:
                url = url + f"&pageToken={pageToken}"

            response = requests.get(url)

            response.raise_for_status()     ## Try 200 as response
            data = response.json()          ## Convert response to JSON

            for item in data.get('items',[]):
                video_id= item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
    
        return  video_ids
            
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":             ## This helps to prevent code execution from any other module
    playListId = get_PlaylistID()
    get_video_ids(playListId)
