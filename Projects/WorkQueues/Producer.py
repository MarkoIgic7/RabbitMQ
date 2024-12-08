import pika
import sys
import os

def send_message():
    message = ''.join(sys.argv[1:])
    print(message)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue="workers")
    channel.basic_publish(
        exchange='',
        routing_key="workers",
        body=message,
    )
    connection.close()


if __name__ == "__main__":
    try:
        send_message()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)