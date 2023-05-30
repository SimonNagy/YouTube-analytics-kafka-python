from http.client import responses
import logging
import sys
import requests


def main():
    logging.info("START")
    
    response = requests.get("https://www.googleapis.com/youtube/v3/playlists", params={})

    logging.debug("GOT %s", response.content)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())