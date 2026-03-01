# svc-reservations

Core booking and reservation service for **NovaTrek Adventures** -- an outdoor recreation company offering hiking, kayaking, climbing, and camping trips.

## Prerequisites

- Java 17+
- Maven 3.9+
- PostgreSQL 15+ (or use local profile with H2)

## Build and Run

```bash
# Build
mvn clean package

# Run with local H2 database
mvn spring-boot:run -Dspring-boot.run.profiles=local

# Run with PostgreSQL
mvn spring-boot:run
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/reservations | List reservations (paginated) |
| GET | /api/v1/reservations/{id} | Get reservation by ID |
| POST | /api/v1/reservations | Create a new reservation |
| PUT | /api/v1/reservations/{id} | Update a reservation |
| PATCH | /api/v1/reservations/{id}/status | Update reservation status |
| GET | /api/v1/reservations/search | Search by guestId, tripId, status |

## Swagger UI

Available at `http://localhost:8081/swagger-ui.html` when running.

## Configuration

- Default port: **8081**
- Profiles: `local` (H2 in-memory), default (PostgreSQL)
- Actuator: `/actuator/health`, `/actuator/info`, `/actuator/metrics`
