import pika
import os
import sys

def read_message():
    print("EXAMPLE : type1.type2.type3.type4 ...")
    print("typeX can be replaced with # which means 0 or more words")
    print("typeX can be replaced with * which means 1 word")
    routing_key = input("Enter routing key in appropriate format - ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange="topicExchange",
        exchange_type="topic"
    )
    result = channel.queue_declare(
        queue = "",
        exclusive= True
    )
    queue_name = result.method.queue
    channel.queue_bind(
        queue=queue_name,
        exchange="topicExchange",
        routing_key=routing_key
    )


    def callback(ch, method, properties, body):
        print(f"{method.routing_key} : {body.decode()}")

    channel.basic_consume(
        queue= queue_name,
        on_message_callback= callback,
        auto_ack= True
    )
    channel.start_consuming()

if __name__ == "__main__":
    try:
        read_message()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)