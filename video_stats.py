import requests
import json
import os 
from dotenv import load_dotenv
from datetime import date

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

    video_ids = []       ##List for storing all videos of the youtuber
    pageToken = None     ##variable to contain token of next page of 50 videos
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playListId}&key={API_KEY}"
    
    try:
        while True:
            url = base_url
            if pageToken:       ## if page token is none
                url = url + f"&pageToken={pageToken}"

            response = requests.get(url)

            response.raise_for_status()     ## Try 200 as response
            data = response.json()          ## Convert response to JSON

            for item in data.get('items',[]):      ## To get object of video_ids from JSON
                video_id= item['contentDetails']['videoId']   
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
    
        return  video_ids
            
    except requests.exceptions.RequestException as e:
        raise e


def extracted_video_data(video_ids):
    extracted_data = []

    # Batches are required because API limit is set to 50 per call.

    def batch_list(video_id_list, batch_size):      ## To convert entire set of videos into batches
        for video_id in range(0, len(video_id_list),batch_size):
            yield video_id_list[video_id : video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):   ## 1 batch = list of 50 videos
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            
            response = requests.get(url)

            response.raise_for_status()     ## Try 200 as response
            data = response.json()          ## Convert response to JSON

            for item in  data.get('items',[]):
                video_id = item['id'] 
                snippet = item['snippet']
                contentDetails  = item['contentDetails']
                stats = item['statistics']

                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": stats.get('viewCount',None),
                    "likeCount": stats.get('likeCount',None),
                    "commentCount": stats.get('commentCount',None)
                }
                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path,"w", encoding="utf-8") as json_outfile:    
        # Writes inside the file path and include specl characters
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False )


if __name__ == "__main__":             ## This helps to prevent code execution from any other module
    playListId = get_PlaylistID()
    video_ids = get_video_ids(playListId)
    yt_data = extracted_video_data(video_ids)
    save_to_json(yt_data)
