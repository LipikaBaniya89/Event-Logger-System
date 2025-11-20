#import necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import pika
import json

# Initialize FastAPI app
app = FastAPI()

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
QUEUE = "events"

# Define the event model (JSON)
class Event(BaseModel):
    source: str
    type: str
    payload: dict
    timestamp: str

# Function to publish message to RabbitMQ
def publish_to_queue(event_dict):
    print("Connecting to RabbitMQ...")

    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    # Create a channel
    channel = connection.channel()

    # Ensure queue exists
    channel.queue_declare(queue=QUEUE, durable=True)

    # Convert event dictionary to JSON string
    message = json.dumps(event_dict)
    print("Publishing message:", message)

    # Publish message to the queue
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    # Close the connection
    connection.close()
    print("Message published successfully!")

# API endpoint to receive events
@app.post("/events")
def receive_event(event: Event):
    # Convert event to dictionary and add unique eventId
    event_dict = event.dict()
    event_id = str(uuid4())
    event_dict["eventId"] = event_id

    # Publish event to RabbitMQ
    publish_to_queue(event_dict)

    # Return response with eventId
    return {"status": "queued", "eventId": event_id}
