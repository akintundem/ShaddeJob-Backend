import logging
import pika
import time

logging.basicConfig(level=logging.INFO)

class RabbitMQManager:
    def __init__(self):
        self.connection = None
        self.channel = None

    def initialize_rabbitmq(self):
        while True:
            try:
                logging.info("We starting Rabbit Connection")
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                self.channel = self.connection.channel()
                logging.info("RabbitMQ is ready!")
                return
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Failed to connect to RabbitMQ: {e}")
                time.sleep(5)

    def get_channel(self):
        if self.channel is None or not self.channel.is_open:
            return None
        return self.channel

    def send_message(self, message, queue_name):
        try:
            ch = self.get_channel()
            ch.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Make message persistent
                )
            )
            logging.info(f"Sent message to RabbitMQ: {message}")
        except Exception as e:
            logging.error(f"Error sending message to RabbitMQ: {e}")

    def consumer(self, queue_name, on_message_callback):
        ch = self.get_channel()
        if ch is None:
            logging.error("RabbitMQ channel is not available")
            return

        ch.queue_declare(queue=queue_name, durable=True)
        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(queue=queue_name, on_message_callback=on_message_callback)

        logging.info('Waiting for messages. To exit press CTRL+C')
        try:
            ch.start_consuming()
        except KeyboardInterrupt:
            logging.info("Interrupted by user")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            if self.connection and self.connection.is_open:
                self.connection.close()
