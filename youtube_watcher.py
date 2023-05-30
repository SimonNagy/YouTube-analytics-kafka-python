from http.client import responses
import logging
import sys
import requests
import json
from config import config

def main():
    logging.info("START")
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
        "key": google_api_key,
        "playlistId": youtube_playlist_id,
        "part": "snippet",
        "maxResults": 50  # Maximum number of results per page (adjust as needed)
    })

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            items = data["items"]
            for item in items:
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_title = item["snippet"]["title"]
                logging.debug("Video ID: %s, Video Title: %s", video_id, video_title)
        else:
            logging.error("Items key not found in response data: %s", data)
    else:
        logging.error("Request failed with status code: %d", response.status_code)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
