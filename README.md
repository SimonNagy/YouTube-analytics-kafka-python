# Youtube Analytics with Confluent_kafka

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

In the next step, a full configuration of Confluent cloud is needed. First of all, I've created a new environemnt, and a Kafka cluster in that environment. Further steps are done in the Kafka cluster.

### Creating a table and a ksql stream for YouTube Analytics

First, I've created a ksql table to store the data fetched from YouTube. This table contains the following attributes: video_id (varchar, key), title (varchar), comments (int), views (int), likes (int)

Next, I've created a stream, so I can send data into ksql. In the stream, the `KAFKA_TOPIC` youtube_videos is defined, and the `value_format` is avro.

![](.\docs/01_create_ksql_stream.png)

The correct establishment of the table, and the stream can be checked by selecting everything, and emitting changes, which results in an infinitely running query.

![](.\docs/02_select_emit_changes.png)

### Creating the comparison table

The next step was to create a comparison table, so that changes on YouTube can be detected. There are three attributes, which can be tracked: likes, comments, and views. For this purpose, I've created the `youtube_changes` table, in the `KAFKA_TOPIC` of youtube_changes. 

![](.\docs/03_create_latest_previous_table.png)

This table contains the number of views, likes and comments, before and after a refresh. This is selected by using the `latest_by_offset` function, and checking the first and second index value of the attributes.

### Detecting changes in real time

Using the previously created table, I've set up a stream, which can detect changes in the latest and previous values. First of all, the successful definition and operation of this table can be checked, as

![](.\docs/04_message_change_tracking.png)

The changed records are displayed as the result of this query. By running this query as `EMIT CHANGES` we can detect chaged real time, by tracking if the previous values and the last values are equal.

## Telegram

The aim of this step is to create a Telegram bot to notify the user, when changes occur in the paramters of the video(s) in the playlist. 

First, I've created a Telegram bot, and collected the ID of the bot. Then I've pinged my bot in order to generate traffic, so I can check the chatId using curl.

![](.\docs\05_telegram_chat_fetchid_jq.png)

Using the chatID, I've created an outbox stream to handle messages from Confluent cloud to the Telegram bot.

![](.\docs/06_setting_up_telegram_outbox_stream.png)

The outbox stream has two attributes: `chat_id`, and `text` that I would like to transfer. It is stored in its dedicated `KAFKA_TOPIC`.

## Connector -- data integration
- HTTP sink connector in confluent
    - `https://api.telegram.org/bot<token>/sendMessage`
    - input record value format == avro
    - request method: POST
    - https header == content-type: application/json
    - request body format == json
insert the png here

## Final pipeline to connect youtube analytics and telegram
- creating the youtube changes stream
- final task: breach the gap between the telegram stream and the youtube changes stream

The next step is to create the stream, which is capable of handling the change records, and can be used in the next steps to forward the changes as messages.

![](.\docs/05_create_ksql_stream_youtubechanges.png)


- writing the query to forward from kafka to telegram (PNG)