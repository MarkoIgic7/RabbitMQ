import pika
import sys
import os

# This app can only consume messages that are sent after app (Subscriber) has been started
# If message is sent, and then this app (Subscriber) is started, Subscriber won't consume it
def main():
    routing_key = input("Input routing key of subscriber - ")
    print(f"This application will receive messages that are sent to"
          f": {routing_key}")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange="router",
        exchange_type="direct"
    )
    result = channel.queue_declare(
        queue="",
        exclusive=True
    )
    queue_name = result.method.queue
    channel.queue_bind(
        queue=queue_name,
        exchange="router",
        routing_key=routing_key
    )

    def callback(ch, method, properties, body):
        print(f"{method.routing_key} : {body.decode()}")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
