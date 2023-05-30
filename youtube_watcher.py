import logging
import sys
from confluent_kafka import SerializingProducer, serialization
import requests
from config import config
import json
from pprint import pformat
from confluent_kafka.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer

def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems",
                            params={
                                "key": google_api_key,
                                "playlistId": youtube_playlist_id,
                                "part": "contentDetails",
                                "pageToken": page_token
                            })

    payload = json.loads(response.text)

    logging.debug("GOT %s", payload)

    return payload


def fetch_videos_page(google_api_key, video_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos",
                            params={
                                "key": google_api_key,
                                "id": video_id,
                                "part": "snippet,statistics",
                                "pageToken": page_token
                            })

    payload = json.loads(response.text)

    logging.debug("GOT %s", payload)

    return payload


def fetch_playlist_items(google_api_key, youtube_playlist_id, page_token=None):
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key, youtube_playlist_id, next_page_token)


def fetch_videos(google_api_key, youtube_playlist_id, page_token=None):
    payload = fetch_videos_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_videos(google_api_key, youtube_playlist_id, next_page_token)

def summarize_video(video):
    
    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        # .get() <= not everything has a count associated; default == 0
        "views": int(video["statistics"].get("viewCount",0)),
        "likes": int(video["statistics"].get("likeCount",0)),
        "comments": int(video["statistics"].get("commentCount",0)),
    }

def on_delivery(err, record):
    pass




def main():
    logging.info("START")

    schema_registry_client = SchemaRegistryClient(config["schema_registry"])

    # encoding the data as binary and ship it up to the kafka cluster
    kafka_config = config["kafka"] | {
        "key.serializer": StringSerializer(),
        "value.serializer": AvroSerializer(schema_registry_client, schema_str),
    }
    producer = SerializingProducer(kafka_config)

    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    for video_item in fetch_playlist_items(google_api_key, youtube_playlist_id):
        video_id = video_item["contentDetails"]["videoId"]
        for video in fetch_videos(google_api_key, video_id):
            logging.info("GOT %s", pformat(summarize_video(video)))

            producer.produce(
                topic = 'youtube_videos', # topic in the kafka ksql cluster
                key = video_id,
                value = value,
                on_delivery = ondelivery
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())


def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems",
                            params={
                                "key": google_api_key,
                                "playlistId": youtube_playlist_id,
                                "part": "contentDetails",
                                "pageToken": page_token
                            })

    payload = json.loads(response.text)

    logging.debug("GOT %s", payload)

    return payload


def fetch_videos_page(google_api_key, video_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos",
                            params={
                                "key": google_api_key,
                                "id": video_id,
                                "part": "snippet,statistics",
                                "pageToken": page_token
                            })

    payload = json.loads(response.text)

    logging.debug("GOT %s", payload)

    return payload


def fetch_playlist_items(google_api_key, youtube_playlist_id, page_token=None):
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key, youtube_playlist_id, next_page_token)


def fetch_videos(google_api_key, youtube_playlist_id, page_token=None):
    payload = fetch_videos_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_videos(google_api_key, youtube_playlist_id, next_page_token)

def summarize_video(video):
    
    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        # .get() <= not everything has a count associated; default == 0
        "views": int(video["statistics"].get("viewCount",0)),
        "likes": int(video["statistics"].get("likeCount",0)),
        "comments": int(video["statistics"].get("commentCount",0)),
    }

def on_delivery(err, record):
    pass




def main():
    logging.info("START")

    schema_registry_client = SchemaRegistryClient(config["schema_registry"])

    # encoding the data as binary and ship it up to the kafka cluster
    kafka_config = config["kafka"] | {
        "key.serializer": StringSerializer(),
        "value.serializer": AvroSerializer(schema_registry_client, schema_str),
    }
    producer = SerializingProducer(kafka_config)

    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    for video_item in fetch_playlist_items(google_api_key, youtube_playlist_id):
        video_id = video_item["contentDetails"]["videoId"]
        for video in fetch_videos(google_api_key, video_id):
            logging.info("GOT %s", pformat(summarize_video(video)))

            producer.produce(
                topic = 'youtube_videos', # topic in the kafka ksql cluster
                key = video_id,
                value = value,
                on_delivery = ondelivery
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())