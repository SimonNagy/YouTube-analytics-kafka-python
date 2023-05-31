# apache-kafka-python
 Reference repository for Apache Kafka with python

Data streaming application, to subscibe to a newsletter without an alert API.

Kafka cluster registered at Confluent Cloud. 
KSQL database

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