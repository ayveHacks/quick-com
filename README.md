# GigProtect AI

AI-powered parametric insurance platform for quick-commerce delivery partners (Blinkit, Zepto, Instamart).

## What This Build Demonstrates

- OTP-based worker registration/login
- Real-time/simulated disruption monitoring every 15 minutes
- AI risk + reliability scoring with required formulas
- Dynamic premium and coverage policy generation
- Zero-touch claim generation (no manual claim endpoint)
- Instant payout simulation to UPI
- Multi-layer fraud detection and fraud logs
- Worker and admin dashboards with charts

## Monorepo Structure

```text
QuickCommerce-Insurance-AI/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   |-- deps.py
|   |   |   `-- v1/
|   |   |       |-- router.py
|   |   |       `-- endpoints/
|   |   |           |-- auth.py
|   |   |           |-- worker.py
|   |   |           |-- policy.py
|   |   |           |-- disruption.py
|   |   |           |-- admin.py
|   |   |           `-- simulation.py
|   |   |-- core/
|   |   |   |-- config.py
|   |   |   `-- security.py
|   |   |-- db/
|   |   |   |-- mongodb.py
|   |   |   `-- indexes.py
|   |   |-- services/
|   |   |   |-- otp_service.py
|   |   |   |-- risk_engine.py
|   |   |   |-- premium_engine.py
|   |   |   |-- policy_service.py
|   |   |   |-- disruption_provider.py
|   |   |   |-- monitoring_service.py
|   |   |   |-- claim_engine.py
|   |   |   |-- fraud_engine.py
|   |   |   |-- analytics_service.py
|   |   |   `-- seed_service.py
|   |   |-- tasks/
|   |   |   `-- scheduler.py
|   |   |-- models/
|   |   |-- utils/
|   |   `-- main.py
|   |-- scripts/
|   |   |-- seed_demo_data.py
|   |   `-- sample_workers.json
|   |-- requirements.txt
|   |-- .env.example
|   `-- Dockerfile
|-- frontend/
|   |-- app/
|   |   |-- page.tsx
|   |   |-- worker/
|   |   |   |-- page.tsx
|   |   |   |-- claims/page.tsx
|   |   |   `-- disruptions/page.tsx
|   |   `-- admin/page.tsx
|   |-- components/
|   |   |-- ui/
|   |   `-- charts/
|   |-- lib/
|   |-- types/
|   |-- package.json
|   |-- tailwind.config.ts
|   |-- next.config.mjs
|   |-- .env.local.example
|   `-- Dockerfile
|-- docs/
|-- docker-compose.yml
`-- README.md
```

## Mathematical Engines Implemented

### Risk Engine

For 10 disruption types:

- `P_rain = RainyDays / TotalDays`
- `P_flood = FloodEvents / TimePeriod`
- `P_traffic = CongestionHours / WorkingHours`
- plus: heat, pollution, curfew, strike, store_outage, server_outage, power_outage

`RiskScore = sum(P_i * W_i)`

`ES = sum(P_i) / N`

### Reliability Score

`RS = (ActivityScore + CompletionScore + WorkHistoryScore + FraudScore) / 4`

- `ActivityScore = WeeklyWorkingHours / MaxHours`
- `CompletionScore = CompletedOrders / AssignedOrders`
- `WorkHistoryScore = min(ExperienceMonths / 24, 1)`
- `FraudScore = 1 - FraudFlags`

### Dynamic Premium and Coverage

- `CF = 0.3 + (0.2 * RS) + (0.1 * ES)`
- `CoverageAmount = WeeklyIncome * CF`
- `BaseRate = 0.015 + (0.02 * RiskScore)`
- `Premium = WeeklyIncome * CF * BaseRate * (1 + RiskScore)`

Enhancements:

- If `RiskScore < 0.3`: premium down, coverage up
- If `RiskScore > 0.6`: premium up, coverage up

Policy constraints:

- Duration: 7 days
- Max claims per week: 8
- Remaining coverage tracked after every approved payout

### Zero-Touch Claims

- `ExpectedOrders = AvgOrdersPerHour * Duration`
- `WorkLossRatio = (ExpectedOrders - ActualOrders) / ExpectedOrders`
- Eligibility: `WorkLossRatio >= 0.5`

Payout:

- `DailyIncome = WeeklyIncome / 7`
- `PF = 0.8 + (0.2 * RS) + (0.1 * ES)`
- `PayoutPercent = Severity * PF`
- `DurationFactor = DurationHours / 24`
- `Payout = DailyIncome * PayoutPercent * DurationFactor`

### Fraud Risk Score

Signals included:

- GPS/location consistency
- Speed validation
- IP vs GPS mismatch
- Activity mismatch
- Historical anomaly

`FRS = f(LocationConsistency, DeviceSignals, NetworkSignals, Activity)`

Rules:

- `FRS >= 0.8` -> blocked
- `0.6 <= FRS < 0.8` -> under review
- `< 0.6` -> approve and payout

## Backend Setup (FastAPI + MongoDB)

1. Create virtual environment and install dependencies:

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure environment:

```bash
copy .env.example .env
```

3. Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend docs:

- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

## Frontend Setup (Next.js + TypeScript + Tailwind)

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Configure env:

```bash
copy .env.local.example .env.local
```

3. Run frontend:

```bash
npm run dev
```

Open:

- [http://localhost:3000](http://localhost:3000)

## Docker Setup

From repository root:

```bash
docker compose up --build
```

Services:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)
- MongoDB: `mongodb://localhost:27017`

## End-to-End Demo Flow

1. Open Admin dashboard (`/admin`) and click `Seed Demo Data`.
2. Go to Worker dashboard (`/worker`).
3. Use sample phone (for example `9000000001`) and click `Request OTP`.
4. Use returned simulation OTP to login.
5. Worker dashboard shows active policy, risk, premium, coverage, disruptions, and claims.
6. In Admin, click `Run Monitoring Now` or trigger a manual disruption.
7. Claims are auto-created. Eligible + low-FRS claims show payout notifications:
   - `INSTANT PAYOUT: Rs XXX credited to UPI ...`

## Key API Endpoints

### Auth

- `POST /api/v1/auth/request-otp`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`

### Worker

- `GET /api/v1/workers/me`
- `GET /api/v1/workers/me/dashboard`
- `GET /api/v1/workers/me/claims`
- `GET /api/v1/workers/me/disruptions`

### Policy

- `GET /api/v1/policies/me/active`
- `POST /api/v1/policies/me/refresh`

### Monitoring and Simulation

- `POST /api/v1/simulation/seed`
- `POST /api/v1/simulation/run-monitoring`
- `POST /api/v1/simulation/trigger-disruption`

### Admin

- `GET /api/v1/admin/metrics`
- `GET /api/v1/admin/disruption-analytics`
- `GET /api/v1/admin/fraud-alerts`
- `GET /api/v1/admin/claims`
- `POST /api/v1/admin/run-monitoring`

## Notes

- Manual claim submission is intentionally not implemented to enforce zero-touch claims.
- External API keys are optional. If unavailable, robust simulation mode is used.
- Scheduler runs every 15 minutes by default (`SCHEDULER_INTERVAL_MINUTES`).

## Future Improvements

- Add real OTP provider and payment rails
- Add role-based admin auth and audit trails
- Use Kafka/Celery for high-throughput asynchronous processing
- Add online ML models for risk and fraud drift detection
- Multi-city geospatial scaling with zone clustering and stream processing
- Policy underwriting experiments with reinforcement learning

