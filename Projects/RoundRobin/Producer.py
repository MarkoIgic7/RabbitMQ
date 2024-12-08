import pika
import sys
import os

# First argument is message that is set to be sent
def send_message():
    message = sys.argv[1]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue="Round-Robin")

    channel.basic_publish(
        exchange="",
        routing_key="Round-Robin",
        body=message
    )
    print(f"Producer sent : {message}")

    channel.close()

if __name__ == "__main__":
    try:
        send_message()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

