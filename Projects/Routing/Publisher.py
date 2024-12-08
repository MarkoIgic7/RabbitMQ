import pika
import sys
import os

# If message is sent to routing key, which has no subscriber,message will be discarded
def publish_message():
    log_type = input("Input which type of message you want to send (Error/Info/Warning) - ")
    message_body = input("Input message you want to send - ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange="router",
        exchange_type="direct"
    )

    channel.basic_publish(
        exchange="router",
        routing_key=log_type,
        body=message_body
    )
    connection.close()

if __name__ == "__main__":
    try:
        publish_message()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
