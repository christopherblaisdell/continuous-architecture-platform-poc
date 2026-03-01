# svc-guest-profiles

Guest profile management service for **NovaTrek Adventures**. Manages guest identity, contact information, medical notes, emergency contacts, and loyalty tier tracking.

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
| GET | /api/v1/guests | List guests (paginated) |
| GET | /api/v1/guests/{id} | Get guest by ID |
| POST | /api/v1/guests | Create a new guest profile |
| PUT | /api/v1/guests/{id} | Update a guest profile |
| GET | /api/v1/guests/search?email= | Search guest by email |
| GET | /api/v1/guests/search?phone= | Search guest by phone |

## Swagger UI

Available at `http://localhost:8082/swagger-ui.html` when running.

## Configuration

- Default port: **8082**
- Profiles: `local` (H2 in-memory), default (PostgreSQL)
- Actuator: `/actuator/health`, `/actuator/info`, `/actuator/metrics`

## Loyalty Tiers

| Tier | Description |
|------|-------------|
| EXPLORER | Default tier for new guests |
| ADVENTURER | Repeat guests with 3+ trips |
| TRAILBLAZER | Loyal guests with 10+ trips |
| SUMMIT | Top-tier guests with 25+ trips |
