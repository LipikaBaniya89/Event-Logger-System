from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import pika
import json

app = FastAPI()

RABBITMQ_HOST = "rabbitmq"
QUEUE = "events"

class Event(BaseModel):
    source: str
    type: str
    payload: dict
    timestamp: str


def publish_to_queue(event_dict):
    print("Connecting to RabbitMQ...")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    # Ensure queue exists
    channel.queue_declare(queue=QUEUE, durable=True)

    message = json.dumps(event_dict)
    print("Publishing message:", message)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
    print("Message published successfully!")


@app.post("/events")
def receive_event(event: Event):
    event_dict = event.dict()
    event_id = str(uuid4())
    event_dict["eventId"] = event_id

    publish_to_queue(event_dict)

    return {"status": "queued", "eventId": event_id}
