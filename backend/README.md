# WiSense Backend — Detailed Implementation & Guide

This file documents the current, actionable state of the WiSense backend (FastAPI service). It is intended as the single source of truth for developers working on the backend. As the codebase evolves, this README will be updated to reflect changes (services, endpoints, migrations, and development workflows).

## Short Summary

- Web framework: FastAPI
- ORM: SQLAlchemy 2.x (declarative mappings)
- Data validation: Pydantic v2
- DB migrations: Alembic (autogenerate-ready)
- Tests: pytest
- Pattern: Repository → Service → API (thin services, explicit repositories)

The backend implements a Sensor Platform foundation (Sensors, Rooms, Capabilities, SignalSamples) with CRUD-first APIs, request-scoped DB sessions, and developer-first CORS handling for ngrok/frontend testing.

## Repository layout (important files)

- `app/main.py` — FastAPI `app` instantiation, lifespan handlers, exception handlers, developer CORS middleware and OPTIONS preflight handling.
- `app/config/settings.py` — Pydantic v2 `Settings` and helpers; reads `.env` for local dev.
- `app/core/logging.py` — logging configuration used by the app.
- `app/database/session.py` — `engine`, `SessionLocal`, and `get_db` dependency.
- `app/database/base.py` — SQLAlchemy declarative `Base` used by models.
- `app/models/` — SQLAlchemy models: `sensor.py`, `room.py`, `capability.py`, `signalsample.py`.
- `app/schemas/` — Pydantic v2 schemas for create/update/response shapes.
- `app/repositories/` — DB access layer: one repository per model; handles commits and queries.
- `app/services/` — business orchestration layer; currently thin wrappers over repositories.
- `app/api/v1/endpoints/` — versioned REST endpoints for health/connect and all sensor platform resources.
- `app/api/v1/router.py` — aggregates v1 routers for inclusion in `main.py`.
- `docs/RUVIEW_ANALYSIS.md` — high level architecture analysis & notes.

Refer to the module docstrings and function signatures for more implementation details.

## Models & Data Shapes

- `Sensor` — UUID primary key, provider/type/status enums, optional `room_id`, metadata; relationships to `Capability` and `SignalSample`.
- `Room` — UUID primary key, name, building/floor, description.
- `Capability` — capability name, `sensor_id` foreign key, enabled flag.
- `SignalSample` — time-series sample with `sensor_id`, timestamp (timezone-aware), RSSI/channel/frequency and optional raw payload.

All models use timezone-aware `DateTime` columns and `UUID` primary keys (PostgreSQL `uuid` dialect type when configured). Models were authored to be Alembic-autogenerate-friendly.

## APIs (current, curated list)

Base path: `/api/v1`

- Health
  - `GET /api/v1/health` — simple liveness and basic checks.

- Connect (frontend/ngrok helper)
  - `POST /api/v1/connect` — returns header and body helpful for ngrok / browser preflight validation.

- Sensors
  - `POST /api/v1/sensors/` — create sensor. Body: `SensorCreate` schema.
  - `GET /api/v1/sensors/` — list sensors (params: `limit`, `offset`).
  - `GET /api/v1/sensors/search` — search by `name` and/or `provider`.
  - `GET /api/v1/sensors/{id}` — get sensor by UUID.
  - `PUT /api/v1/sensors/{id}` — update sensor (partial via `SensorUpdate`).
  - `DELETE /api/v1/sensors/{id}` — delete sensor.

- Rooms
  - CRUD under `/api/v1/rooms/` (same pattern as sensors).

- Capabilities
  - CRUD under `/api/v1/capabilities/` (capabilities belong to sensors).

- Signal samples
  - `POST /api/v1/signals/` — create a signal sample.
  - `GET /api/v1/signals/` — list samples (filter: `sensor_id`, `start`, `end`, pagination).
  - `GET /api/v1/signals/{id}` — get sample by UUID.

Request/response schema details are defined in `app/schemas/` and use Pydantic v2 `ConfigDict(from_attributes=True)` to permit returning ORM objects directly where appropriate.

## Database setup & migrations

1. Ensure `DATABASE_URL` is configured (in `.env` or environment). Example (Postgres):

```text
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/wisense_db
```

2. Create Alembic migration (local dev):

```bash
cd backend
alembic revision --autogenerate -m "add sensor platform models"
alembic upgrade head
```

Note: Alembic config loads the app models via `env.py` (project-specific). If autogenerate misses types, confirm `app.database.base.Base` is imported by Alembic env.

## Running locally (developer quick-start)

Windows PowerShell example:

```powershell
# from repository root
cd "WiSense/backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/wisense_db" # or set via PowerShell $env:DATABASE_URL
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

OpenAPI docs: `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc) while the app runs.

## Testing

Run tests with `pytest` from the `backend` directory:

```bash
pytest -q
```

Current tests cover the health/connect endpoints; tests for sensor/platform endpoints are planned.

## Logging

- Structured logging is configured in `app/core/logging.py`. The app uses this configuration via FastAPI lifespan events.
- For dev, logs are human-friendly. For production, forward structured logs to your aggregator (ELK, Grafana Loki, etc.).

## CORS and ngrok notes

- During development there was an intermittent preflight issue when routing through ngrok and custom frontends. To accommodate this, a developer-mode CORS middleware and catch-all `OPTIONS` route were added to `app/main.py`. The middleware specifically preserves the `ngrok-skip-browser-warning` header to allow ngrok's browser warning bypass.
- For production, revert to `fastapi.middleware.cors.CORSMiddleware` configured with a strict origin allowlist and `allow_credentials`/`allow_headers` as required.

## Security & Production Concerns

- No authentication or authorization is implemented yet. Do not expose this API to the internet without adding auth (JWT/OAuth2), rate-limiting, and API keys where appropriate.
- Validate payload sizes carefully for signal samples and raw payload fields.
- Consider DB sizing and partitioning for time-series signal data (SignalSample) if sampling volume is high.

## Development conventions

- Repositories handle raw DB operations and commit/refresh semantics.
- Services orchestrate transactions/business logic and are the place to add validation/side-effects in future.
- Endpoints should remain thin; complex flows should move into services.

## Contribution & Maintenance

To contribute:

1. Create a feature branch.
2. Add/modify tests covering behavior.
3. Run `pytest` locally.
4. Create an Alembic migration if DB models changed.

When updating code that affects APIs, models, or migrations, update this README to reflect:

- new endpoints or changed request/response shapes,
- migration instructions and new required environment variables,
- any runtime/infrastructure changes (Docker, Kubernetes manifests, or CI steps).

I will proactively update this README when I modify the code in this repository during our session. If you want automated enforcement, we can add a small CI check that fails PRs which change API signatures but do not update a docs file or test suite.

## Troubleshooting

- If migration autogenerate fails: ensure the app imports `app.models` in `alembic/env.py` or point Alembic `target_metadata` to `app.database.base.Base.metadata`.
- If environment variables are not read: confirm `.env` exists and `app/config/settings.py` is configured to load it in dev.

## Next actions recommended

1. Generate Alembic migration locally and apply to your dev DB.
2. Add unit/integration tests for the new endpoints and services.
3. Add basic auth and enable it behind a feature flag for internal testing.

---

File location: `WiSense/backend/README.md`

If you'd like, I will now:
- add pytest tests for the sensor endpoints, or
- scaffold an Alembic migration file here (note: running migrations requires a DB connection)

