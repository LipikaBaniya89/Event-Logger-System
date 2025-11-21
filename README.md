# Event-Logger-System
A lightweight Event Logger Service that accepts application events via an API, queues them using a message broker, and stores them in a database asynchronously. This simulates a real-world architecture for logging, analytics, or telemetry systems.

## How to run the project
### Clone the repository

```
git clone https://github.com/<your-username>/event-logger.git
cd event-logger
```

### Build and run the containers
```
docker-compose up --build
```

### After startup:
- API : http://localhost:8000
- RabbitMQ UI : http://localhost:15672
- PostgreSQL : localhost:5432
- Consumer : logs show real-time events


## Testing the API
### Send an event

```
curl -X POST http://localhost:8000/events -H "Content-Type: application/json" -d '{"source": "test", "type": "test", "payload": {"test": "test"}, "timestamp": "2022-01-01T00:00:00"}'
```

### Example response
```
{
    "status": "queued",
    "eventId": "12345678-1234-1234-1234-123456789012"
}
```

## Tech Stack
- FastAPI : Web framework for building APIs
- RabbitMQ : Message broker for queuing events
- PostgreSQL : Database for storing events
- Docker : Containerization platform
- Docker Compose : Container orchestration tool
- Python : Programming language
- JSON : Data format
- /health endpoint, RabbitMQ UI

## Reason

1. FastAPI 
- Modern & High performance Python web framework
- Automatic request validation using Pydantic
- Suitable for lightweight microservices

2. RabbitMQ
- Lightweight message broker and easy to setup in Docker
- Persistent queues 
- Simple Learning Curve
- Good for async + decoupled architectures

3. PostgreSQL
- Reliable and Battle tested
- JSONB Support
- Easy to connect with Python Libraries

4. Docker
- Environment Consistency 
- Lightweight
- Runs RabbitMQ/Postgre withour installing locally

5. Docker Compose
- Simple Orchestration all 4 services with one command
- Clear Separation of Services
- Easy networking

6. Python
- Fast Development and readable
- Rich Libraries for messaging & DBs
- Great for Prototyping

7. JSON
- Universal Data Format
- Easy to parse
- Schema Flexible
- Works well with PostgreSQL JSONB

8. /health endpoint, RabbitMQ UI
- Rabbit MQ Management 
- Debug Friendly
- Lighteweight Monitporing
