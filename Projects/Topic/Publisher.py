import pika
import sys
import os

def send_message():
    print("type1.type2.type3.type4 ...")
    routing_key = input("Enter which subscribers the message is intended for (in appropriate format) type1.type2.type3 - ")
    message_body = input("Enter message body - ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange="topicExchange",
        exchange_type="topic"
    )
    channel.basic_publish(
        exchange="topicExchange",
        routing_key=routing_key,
        body=message_body
    )

    print(f"{routing_key} : {message_body}")

    connection.close()

if __name__ == "__main__":
    try:
        send_message()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)