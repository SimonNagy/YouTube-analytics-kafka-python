# Youtube Analytics with Kafka-python

In this project, I've built a program, which utilizes the confluent_kafka python libary in order to collect and stream data to a Confluent Kafka cluster ksql database, and notify the user on Telegram, when a video gets liked. 

### Technologies
* confluent_kafka Python libary
* Google Cloud YouTube playlist API
* Confluent Kafka cluster
* k-sql datbase
* Telegram BOT API

## General overview of the python application

The application is built from two files: `youtube_watcher.py`, which contains all the functions, and is the entry point of the program (can be started from the console with `py youtube_watcher.py`), and `config.py`, which is a simple configuration file. The config file contains no keys / passwords in this repository.

### `youtube_watcher.py`

This file contains 6 functions, as 
* `:fetch_playlist_items_page:` which produces a json response in a payload object. This function calls the config file, and fetches the GCP API credentials, than returns data about the playlist in `contentDetails` format,
* `:fetch_videos_page:` which produces a json response in a payload object, containing the `snippet` and `statistics` formats. This function also operates by a `page_token` variable, which is important in the paging part of the programme,
* `:fetch_playlist_items:` which is responsible for the paging. This function yields all results, and proceeds to the `nextPageToken`,
* `:fetch_videos:` which yields all video from the `payload["items"]`,
* `:summarize_video:` which summarizes data, so it can be passed to the `:main:` function, and
* `:main:`, which combines the retrieval of the playlist items, and videos, logging the details, and producing the summarized data to a Kafka topic.

## Confluent 

### Creating the table
create ksql stream for youtube videos

confluent_kafka
fastavro

select-emit-changes -- emit changes from the youtube videos table

### Creating the comparison table

creating last-previous table to compare changes in likes/comments etc.

### Detecting changes in real time

detect changes in real time -- emit changes + track if previous and current likes are equal

## Telegram
creating a telegram bot to manage notifications, when there are changes in the paramteres
- creating the bot
- pinging the bot, then fetching chatid with curl
- creating the outbox stream to handle messages to telegram (confluent)

## Connector -- data integration
- HTTP sink connector in confluent
    - https://api.telegram.org/bot<token>/sendMessage
    - input record value format == avro
    - request method: POST
    - https header == content-type: application/json
    - request body format == json
insert the png here

## Final pipeline to connect youtube analytics and telegram
- creating the youtube changes stream
- final task: breach the gap between the telegram stream and the youtube changes stream
- writing the query to forward from kafka to telegram (PNG)