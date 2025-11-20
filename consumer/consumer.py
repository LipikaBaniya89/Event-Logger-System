print("=== CONSUMER SCRIPT LOADED ===")

# ===============================
# IMPORTS
# ===============================

# Import necessary libraries
import pika, psycopg2, json, os, time
from datetime import datetime

#Console log
print("Imports loaded successfully")

# ===============================
# CONFIGURATION
# ===============================

# RabbitMQ queue name
QUEUE = "events"

# Hostname for RabbitMQ.
RABBIT = os.getenv("RABBITMQ_HOST", "rabbitmq")

# Hostname for PostgreSQL database.
DB = os.getenv("DB_HOST", "db")

print("Waiting for DB and RabbitMQ...")
time.sleep(10)

# --------------------------------------------------------
# CONNECT TO POSTGRES DATABASE
# --------------------------------------------------------
print("Connecting to DB...")

#prevents consumer from failing if DB is not up yet
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

# Create cursor to execute queries
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

# --------------------------------------------------------
# CONNECT TO RABBITMQ AND START CONSUMING
# --------------------------------------------------------

print("Connecting to RabbitMQ...")

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT)
)

# Channel to communicate with RabbitMQ
channel = connection.channel()

# Ensure queue exists
channel.queue_declare(queue=QUEUE, durable=True)
print("Connected to RabbitMQ queue:", QUEUE)

# --------------------------------------------------------
# MESSAGE HANDLER FUNCTION
# Runs each time a message arrives in the queue
# --------------------------------------------------------

#function to handle incoming messages
def handler(ch, method, properties, body):
    print("Received raw message:", body)

    # Parse JSON message
    event = json.loads(body)

    # Validate required fields
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

    # Acknowledge message
    ch.basic_ack(method.delivery_tag)

# --------------------------------------------------------
# START LISTENING TO QUEUE
# --------------------------------------------------------

# Start consuming messages from the queue
channel.basic_consume(queue=QUEUE, on_message_callback=handler)
print("Consumer ready. Waiting for messages...")
channel.start_consuming()
