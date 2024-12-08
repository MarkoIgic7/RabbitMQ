import pika
import sys
import os

#Application sends message to all Subscribers (Fanout Exchange)
def send_message():
    message = input("Input message to send all Subscribers - ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="manager",exchange_type="fanout")

    channel.basic_publish(
        exchange="manager",
        routing_key="",
        body=message
    )
    print(f"Mesage sent : {message}")
    connection.close()

if __name__ == "__main__":
    try:
        send_message()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
