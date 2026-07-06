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

## Recent changes (quick)

- Added device management endpoints for registration, heartbeat, disconnect, online listing, and status patch under `/api/v1/sensors`.
- Introduced repository + service + schema layers for sensor management (`app/repositories/sensor_repository.py`, `app/services/sensor_service.py`, `app/schemas/sensor_management.py`, `app/api/v1/endpoints/sensor_management.py`).
- Renamed model attribute `metadata` → `meta` to avoid SQLAlchemy Declarative API reserved-name conflict; column name remains `metadata` in the DB. Client payloads may still include `metadata` and the backend will normalize it to `meta`.
- Fixed `SignalSample` model: imported missing `String` and `ForeignKey`, and added a `ForeignKey("sensors.id")` on `sensor_id` to ensure referential integrity.
- Tests: unit tests pass locally: `3 passed, 1 warning`.

- Added a Discovery Engine for provider-based sensor discovery and discovery result management.

These edits were applied to support the communication layer (device registration and lifecycle), the new provider abstraction layer, and discovery workflow support.

## Discovery Engine (new)

WiSense now includes a dedicated Discovery Engine that discovers sensors from every registered provider. Discovery is provider-driven and returns mock discovered sensors for now; it does not communicate with hardware.

Discovery flow:

1. `DiscoveryService` calls every registered provider via `ProviderFactory`.
2. Each provider runs `discover()` and returns mock discovery rows.
3. `DiscoveryService` merges results and removes duplicates.
4. The frontend queries discovery providers, starts discovery, inspects latest results, and registers selected discovered sensors.

Discovery endpoints:

- `GET /api/v1/discovery/providers` — list supported provider names.
- `POST /api/v1/discovery/start` — run discovery across all providers.
- `GET /api/v1/discovery/results` — get the most recent discovery output.
- `POST /api/v1/discovery/register` — register a discovered sensor into the Sensor Platform.

This is intentionally a backend-only discovery engine; future hardware integration will be implemented inside provider `discover()` methods without changing the discovery endpoint contract.

## Provider architecture (new)

WiSense now includes a provider abstraction layer that isolates hardware-specific behavior from the backend. The provider layer is strictly a communication and capability abstraction — it does not implement firmware or device-side code.

Package: `app/providers`

Structure:

```
providers/
  __init__.py
  base/
    base_provider.py
  factory.py
  registry.py
  esp32/provider.py
  laptop/provider.py
  usb/provider.py
  dataset/provider.py
  simulator/provider.py
```

Purpose:
- `BaseSensorProvider` (abstract) defines the provider API: `connect`, `disconnect`, `discover`, `register`, `heartbeat`, `health`, `start_capture`, `stop_capture`, `get_capabilities`, `get_information`, `get_status`.
- `ProviderRegistry` allows providers to register themselves automatically (no central factory edits required to add providers).
- `ProviderFactory.get(provider_name, sensor_info)` returns a provider instance by looking up the registered provider class.
- Placeholder providers (`ESP32Provider`, `LaptopProvider`, `USBAdapterProvider`, `DatasetProvider`, `SimulatorProvider`) implement the abstract interface; where direct hardware operations would occur they raise `NotImplementedError`. They return mocked information for `get_information`, `get_capabilities`, and `get_status`.

Integration:
- `SensorService.register()` now instantiates the correct provider via `ProviderFactory` and attaches the provider instance to the returned `Sensor` object as a runtime-only attribute (`_provider`). No hardware communication is performed during registration.

Why this design:
- New providers can be added by creating a module under `app/providers/` and using the `@register_provider("name")` decorator. The factory does not need to change.
- The service layer remains the single place to initialize provider instances and to coordinate provider-driven workflows in future (captures, live health checks).


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
- `app/api/v1/endpoints/` — versioned REST endpoints for health/connect, sensor platform resources, and discovery.
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

- All successful API responses return a standardized wrapper:
  ```json
  {
    "success": true,
    "message": "...",
    "data": {},
    "pagination": null,
    "errors": null
  }
  ```
  - `data` holds the primary payload.
  - `pagination` accompanies list endpoints and includes `limit`, `offset`, `count`, and optional `total`.
  - `errors` contains validation or server error details when `success` is `false`.

- Health
  - `GET /api/v1/health` — simple liveness and basic checks.

- Connect (frontend/ngrok helper)
  - `GET /api/v1/connect` — returns a stable connectivity payload useful for frontend integration and ngrok validation.

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

### Sensor management (registration & lifecycle)

The backend exposes device management endpoints under `/api/v1/sensors` to support multiple providers (ESP32, laptop, USB adapters, Intel CSI, dataset replay, and future providers). These endpoints form the communication layer only — firmware and device-side code are out of scope.

- `POST /api/v1/sensors/register` — Register or update a sensor.
  - Purpose: Devices call this once on boot (or ops call it from provisioning) to create or reconcile a `Sensor` record.
  - Identification: If the payload includes `id`, that record is preferred. Otherwise the server attempts to match `serial_number` first, then `mac_address`.
  - Request schema: `SensorRegister` (fields: `name`, `provider`, optional `serial_number`, `mac_address`, `firmware_version`, `hardware_version`, `ip_address`, `location`, `room_id`, `metadata`).
  - Response: API wrapper containing a `SensorResponse` payload.
  - Status codes: 201 Created on new or updated object, 400 on validation errors.

- `POST /api/v1/sensors/heartbeat` — Heartbeat from devices.
  - Purpose: Devices periodically POST heartbeats to signal liveness. Accepts one of `sensor_id`, `serial_number`, or `mac_address` to identify the device.
  - Request schema: `SensorHeartbeat` (fields: `sensor_id`, `serial_number`, `mac_address`, optional ISO `timestamp`, optional `status`).
  - Behavior: Updates `last_seen` to the provided timestamp (or server UTC now) and sets `status` to `ONLINE` by default unless `status` provided.
  - Response: `SensorResponse` (updated sensor).
  - Status codes: 200 OK, 404 if the sensor cannot be found by provided identifiers.

- `POST /api/v1/sensors/disconnect` — Explicit disconnect.
  - Purpose: Devices or management tools call to mark a sensor offline in case of graceful shutdown or managed disconnect.
  - Request schema: `SensorDisconnect` (`sensor_id` | `serial_number` | `mac_address`).
  - Behavior: Sets `status` to `OFFLINE` and updates `last_seen`.
  - Response: `SensorResponse`.
  - Status codes: 200 OK, 404 if not found.

- `GET /api/v1/sensors/online` — List currently online sensors.
  - Purpose: Query currently online sensors for UI or tooling.
  - Query params: `within_seconds` (int, default 300), `limit`, `offset`.
  - Behavior: Returns sensors with `status == ONLINE` or with `last_seen` within the `within_seconds` window.
  - Response: List[`SensorResponse`].
  - Status codes: 200 OK.

- `PATCH /api/v1/sensors/status` — Patch status for a sensor.
  - Purpose: Administrative endpoint to set sensor status to `OFFLINE`, `ERROR`, `ONLINE`, etc.
  - Request schema: `SensorStatusPatch` (`sensor_id` | `serial_number` | `mac_address`, `status`).
  - Response: `SensorResponse`.
  - Status codes: 200 OK, 404 if sensor not found.

All management endpoints are documented (summary + description) in the code and will appear in Swagger UI at `/docs`.

## Files added/modified for sensor management

The following files were added or updated to implement the device management communication layer. Below each file is a concise explanation of what's in it and why it changed.

- `app/repositories/sensor_repository.py` (modified)
  - Added helper methods:
    - `get_by_serial(serial_number)` / `get_by_mac(mac_address)` — lookup by secondary identifiers.
    - `register_or_update(data: dict)` — create or update a sensor record based on `id`, `serial_number`, or `mac_address`.
    - `update_heartbeat(sensor, last_seen, status)` — update `last_seen` and optionally status.
    - `set_status(sensor, status)` — set explicit status and refresh record.
    - `get_online(within_seconds, limit, offset)` — return sensors considered online (status==ONLINE or recently seen).
  - Purpose: Keep all persistence logic and commit/refresh semantics inside the repository so services and API code remain simple.

- `app/services/sensor_service.py` (modified)
  - Added management methods:
    - `register(data: dict)` — delegates to repository `register_or_update`.
    - `heartbeat(sensor_id|serial_number|mac_address, timestamp, status)` — resolves identifier and updates heartbeat.
    - `disconnect(...)` — resolves identifier and marks `OFFLINE`.
    - `patch_status(...)` — resolves identifier and sets provided status.
    - `get_online(...)` — query online sensors via repository.
  - Purpose: Orchestrates identifier resolution and higher-level flows; single place for future business rules (rate-limiting, audit logs).

- `app/schemas/sensor_management.py` (added)
  - New Pydantic schemas for management endpoints: `SensorRegister`, `SensorHeartbeat`, `SensorDisconnect`, `SensorStatusPatch`.
  - Purpose: Validate incoming requests and produce clear OpenAPI payload documentation.

- `app/api/v1/endpoints/sensor_management.py` (added)
  - New endpoint module that exposes the five management routes under `/api/v1/sensors/`:
    - `/register`, `/heartbeat`, `/disconnect`, `/online`, `/status` (PATCH).
  - Each route includes `summary` and `description` so they appear properly in Swagger.
  - Uses `get_db` dependency and `SensorService` to perform operations.

- `app/api/v1/router.py` (modified)
  - Includes the new `sensor_management` router so endpoints are mounted under `/api/v1`.

## Frontend considerations (how UI will display devices)

- Device discovery and listing:
  - The frontend should call `GET /api/v1/sensors/online` to populate the live device list. Use `within_seconds` to tune staleness.
- Device identity and details:
  - Each `SensorResponse` contains provider, status, last_seen, firmware/hardware versions, and optional `room_id` to enable mapping in UI.
- Heartbeat-driven UI updates:
  - When a heartbeat arrives, the backend updates `last_seen` and `status`. The frontend can poll or use server-sent events / WebSocket later (not implemented) to get real-time updates.

## Example payloads

- Register (POST `/api/v1/sensors/register`):

```json
{
  "name": "esp32-sensor-1",
  "provider": "esp32",
  "serial_number": "ESP32-0001",
  "mac_address": "aa:bb:cc:dd:ee:ff",
  "firmware_version": "1.2.3",
  "hardware_version": "revA",
  "ip_address": "192.168.1.55",
  "location": "lab-1"
}
```

- Heartbeat (POST `/api/v1/sensors/heartbeat`):

```json
{
  "serial_number": "ESP32-0001",
  "timestamp": "2026-07-06T12:34:56.789Z"
}
```

- Disconnect (POST `/api/v1/sensors/disconnect`):

```json
{
  "mac_address": "aa:bb:cc:dd:ee:ff"
}
```

- Patch status (PATCH `/api/v1/sensors/status`):

```json
{
  "sensor_id": "<uuid>",
  "status": "ERROR"
}
```

## Example standard response

```json
{
  "success": true,
  "message": "Sensors retrieved successfully.",
  "data": [
    {
      "id": "00000000-0000-0000-0000-000000000001",
      "name": "lab-temperaturesensor",
      "provider": "esp32",
      "sensor_type": "WiFi",
      "status": "ONLINE",
      "created_at": "2026-07-06T12:00:00Z",
      "updated_at": "2026-07-06T12:00:00Z"
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "count": 1,
    "total": null
  },
  "errors": null
}
```

## Security note

These management endpoints are sensitive. Add authentication and rate-limiting (e.g., token-based device auth, API keys, or mTLS) before accepting traffic from untrusted networks.

## Next steps

1. Add tests for new endpoints and repository/service flows (I can scaffold these).
2. Optionally add device authentication (signed registration tokens or pre-shared keys).
3. Consider a real-time push architecture (WebSocket or SSE) for immediate frontend updates.

---

File location: `WiSense/backend/README.md`


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

