import json
import os
from pika import BlockingConnection, ConnectionParameters

from innotter.settings import PUBLISH_QUEUE, RABBITMQ_HOST

connection = BlockingConnection(
    ConnectionParameters(
        host=RABBITMQ_HOST,
        heartbeat=600,
        blocked_connection_timeout=300
    )
)
channel = connection.channel()
channel.queue_declare(queue=PUBLISH_QUEUE)


def publish(message: dict) -> None:
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('PUBLISH_QUEUE'),
        body=json.dumps(message)
    )