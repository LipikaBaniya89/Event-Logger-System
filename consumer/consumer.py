print("=== CONSUMER SCRIPT LOADED ===")

import pika, psycopg2, json, os, time
from datetime import datetime

print("Imports loaded successfully")

QUEUE = "events"
RABBIT = os.getenv("RABBITMQ_HOST", "rabbitmq")
DB = os.getenv("DB_HOST", "db")

print("Waiting for DB and RabbitMQ...")
time.sleep(10)

# Connect DB
print("Connecting to DB...")
while True:
    try:
        conn = psycopg2.connect(
            host=DB, 
            database="eventsdb",
            user="eventuser", 
            password="eventpass"
        )
        break
    except Exception as e:
        print("DB not ready, retrying...", e)
        time.sleep(3)

print("DB connected!")

cursor = conn.cursor()
print("DB connection successful")

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    eventId VARCHAR(100) PRIMARY KEY,
    source VARCHAR(100),
    type VARCHAR(100),
    payload JSONB,
    timestamp TIMESTAMP,
    receivedAt TIMESTAMP DEFAULT NOW()
)
""")
conn.commit()
print("Table ensured")

# Connect RabbitMQ
print("Connecting to RabbitMQ...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT)
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)
print("Connected to RabbitMQ queue:", QUEUE)

def handler(ch, method, properties, body):
    print("Received raw message:", body)

    event = json.loads(body)

    required = ["eventId", "source", "type", "payload", "timestamp"]
    for f in required:
        if f not in event:
            print("Invalid event missing:", f)
            ch.basic_ack(method.delivery_tag)
            return

    print("Validated event:", event)

    # Insert into DB
    cursor.execute("""
        INSERT INTO events (eventId, source, type, payload, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        event["eventId"],
        event["source"],
        event["type"],
        json.dumps(event["payload"]),
        event["timestamp"]
    ))

    conn.commit()
    print("Stored event:", event["eventId"])
    ch.basic_ack(method.delivery_tag)

channel.basic_consume(queue=QUEUE, on_message_callback=handler)
print("Consumer ready. Waiting for messages...")
channel.start_consuming()
