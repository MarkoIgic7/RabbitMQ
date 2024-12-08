import pika
import os
import sys

# Subscriber can receive messages ONLY after it has been started
def main():
    print("Starts listening")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange="manager",
        exchange_type="fanout"
    )
    result = channel.queue_declare(
        queue="",
        exclusive=True #enables queue to be deleted after closing the connection. Subscriber will listen only when it is run
    )
    queue_name = result.method.queue
    channel.queue_bind(
        exchange="manager",
        queue=queue_name,
        routing_key=""
    )
    def callback(ch, method, properties, body):
        print(f"Subscriber received : {body.decode()}")

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