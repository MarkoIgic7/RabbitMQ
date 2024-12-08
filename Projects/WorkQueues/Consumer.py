import pika
import os
import sys
import time


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue="workers")

    def callbackFunc(ex,method, properties, body):
        print(f"Received : {body.decode()}")
        time.sleep(body.count(b'.')) #Counts number of ".", and sleeps that time (seconds)
        channel.basic_ack(delivery_tag=method.delivery_tag) # This is equal to auto_ack = True (in basic_consume())

        #If auto_ack is set, message won't be deleted if an error occurs


    channel.basic_qos(prefetch_count=1) # Consumer receives message only after it processed previous, if not -> RoundRobin
    channel.basic_consume(
        queue="workers",
        on_message_callback=callbackFunc)

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
