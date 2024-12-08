import os
import sys
import pika

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost"),
    )
    channel = connection.channel()

    channel.queue_declare(queue="Round-Robin")

    def callback(ch, method, properties, body):
        print(f"Received : {body.decode()}")

    channel.basic_consume(
        queue="Round-Robin",
        on_message_callback=callback,
        auto_ack=True,
    )

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)