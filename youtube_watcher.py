from http.client import responses
import logging
import sys
import requests
from config import config

def main():
    logging.info("START")
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    response = requests.get("https://www.googleapis.com/youtube/v3/playlists", params={
        "key": google_api_key,
        "id": youtube_playlist_id,
        })

    logging.debug("GOT %s", response.content)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())