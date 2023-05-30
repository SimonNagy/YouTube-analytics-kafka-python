from http.client import responses
import logging
import sys
import requests
import json
from config import config

def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
            "key": google_api_key,
            "playlistId": youtube_playlist_id,
            "part": "contentDetails",
            "pageToken": page_token
        })
    
    # JSON parsing
    payload = json.loads(response.text)
    
    logging.debug("GOT %s", payload)

    return payload

def fetch_playlist_items(google_api_key, youtube_playlist_id, page_token=None):

    # fetching one page
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token)

    # output all items given by payload
    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key, youtube_playlist_id, next_page_token)

def main():
    logging.info("START")
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    for video_item in fetch_playlist_items_page(google_api_key, youtube_playlist_id):
        logging.info("GOT %s", video_item)
    

    """
    When using the ::fetch_playlist_items_page:: this response is no longer needed

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            items = data["items"]
            for item in items:
                kind = item["kind"]
                item_id = item["id"]
                content_details = item["contentDetails"]
                etag = item["etag"]
                logging.debug("Kind: %s, ID: %s Content Details: %s, Etag: %s",
                               kind, item_id, content_details, etag)

        # Include page info section
        if "pageInfo" in data:
            page_info = data["pageInfo"]
            total_results = page_info["totalResults"]
            results_per_page = page_info["resultsPerPage"]
            logging.debug("Total Results: %d, Results Per Page: %d", total_results, results_per_page)
        else:
            logging.error("Page info not found in response data: %s", data)
    else:
        logging.error("Request failed with status code: %d", response.status_code)
        
    """

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
