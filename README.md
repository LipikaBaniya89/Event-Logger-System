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

