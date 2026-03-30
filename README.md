# InnerEdge: AI-Powered Smart Money Concepts Trading Journal & Liquidity Intelligence Platform

## Project Overview

**InnerEdge** is a production-ready SaaS backend for CFD traders that combines:
- **Smart Money Concepts (SMC)** analysis engine based on Atif Hussain's liquidity-driven philosophy
- **CFD-specific risk management** with leverage, margin, and swap cost tracking
- **AI behavioral insights** (NOT predictions) on trader performance patterns
- **Subscription billing** via Stripe for SaaS monetization

---

## Architecture

### Tech Stack
- **Framework**: Django 6.0 + Django REST Framework
- **Real-time**: Django Channels + Redis  
- **Database**: PostgreSQL (Psycopg)
- **Async Tasks**: Celery + Redis
- **Payments**: Stripe API
- **Deployment**: Docker + Gunicorn + Nginx

### API Modules (7 Core Domains)

1. **Accounts** (`/api/accounts/`)
   - User profiles with CFD risk preferences
   - Default leverage, margin thresholds, base currency
   - Endpoints: `GET/POST /api/accounts/profiles/`

2. **Market** (`/api/market/`)
   - Assets, OHLCV candles, CFD conditions (spreads, swaps, margin %)
   - **Liquidity zones** (buy-side/sell-side detection)
   - **Sweep events** (liquidity harvesting signals)
   - **Daily bias** (market structure + bias determination)
   - **FVG** (Fair Value Gaps) - secondary confluence
   - **Order Blocks** - secondary confluence
   - Endpoints: Assets, Candles, Zones, Sweeps, Bias, FVG, OB

3. **Journal** (`/api/journal/`)
   - Trade logging with entry, exit, SL, TP, position size, leverage, margin used
   - Setup tagging (FVG, OB, Liquidity Sweep, etc.)
   - Swap fees, commissions, PnL in both account and base currency
   - Trade notes and screenshots
   - Analytics: win rate, average R multiple, gross profit/loss
   - Endpoints: Trades, Tags, Notes, Analytics snapshots

4. **Intel** (`/api/intel/`)
   - **Behavioral metrics** (daily averages: leverage, swap ratio, win rates)
   - **Behavioral insights** (AI-generated, non-predictive)
     - Examples: over-leverage detection, swap cost impact, directional bias analysis
   - Endpoints: Metrics, Insights with generation trigger

5. **Paper** (`/api/paper/`)
   - Virtual CFD accounts with simulated margin and equity
   - Paper positions with leverage, swaps, PnL tracking
   - Margin level calculation and stop-out alerts
   - Endpoints: Accounts, Positions with recalculation

6. **Alerts** (`/api/alerts/`)
   - User-defined alert rules (liquidity builds, sweeps, margin risk, leverage warnings, swap impacts)
   - Alert events with severity levels (Info, Warning, Critical)
   - WebSocket consumer for real-time push notifications
   - Endpoints: Rules, Events with mark-as-read actions

7. **Billing** (`/api/billing/`)
   - Plans (Free, Pro, Premium)
   - Subscriptions with Stripe integration
   - Invoices synced from Stripe
   - Stripe webhook handling for subscription lifecycle events
   - Checkout session generation
   - Endpoints: Plans, Subscriptions, Invoices, `/stripe/webhook/`

---

## Philosophy Integration: Atif Hussain's Smart Money Concepts

The platform encodes **liquidity-first trading philosophy**:

1. **Liquidity Zones** - Detect equal highs/lows where institutions park stop orders
2. **Liquidity Sweeps** - Identify when price breaks zones, signaling stop-hunt and reversal
3. **Daily Bias** - Compute directional bias from higher-timeframe market structure (HH/HL, LH/LL)
4. **Entry Zones** - Map reversal entry areas post-sweep
5. **FVG + Order Blocks** - Used as **secondary confluence only**, not primary signals

**Non-Predictive AI**: The behavioral engine generates insights on trader behavior and risk patterns, never claims to predict market direction.

---

## Key Features

### Market Data Engine
- Broker adapters: IG, OANDA, Binance (extensible)
- Candle ingestion with spread and swap metadata
- Liquidity detection and sweep event generation (async tasks)

### CFD-Specific Tracking
- Position size, leverage, margin requirements, overnight swaps
- Margin level % and stop-out risk alerts
- PnL in both account currency and base currency

### Trading Journal Analytics
- Win rate, average R multiple, profit factor
- Directional bias analysis (long vs. short performance)
- Setup tagging for pattern recognition

### Real-Time Alerts
- WebSocket-based alert streaming to connected clients
- Configurable rules and severity levels

### SaaS Monetization
- Multi-tier subscription plans
- Stripe checkout integration
- Invoice history and billing management

---

## Directory Structure

```
InnerEdge/
├── config/
│   ├── settings.py (DRF, Channels, Celery, PostgreSQL config)
│   ├── urls.py (API routing)
│   ├── asgi.py (HTTP + WebSocket)
│   ├── wsgi.py
│   ├── celery.py
│   └── routing.py (WebSocket routing)
├── accounts/
│   ├── models.py (TraderProfile)
│   ├── views.py (ViewSets)
│   ├── serializers.py
│   ├── urls.py
│   ├── signals.py (auto-create profile on user registration)
│   └── migrations/
├── market/
│   ├── models.py (Asset, Candle, LiquidityZone, SweepEvent, DailyBias, FVG, OrderBlock)
│   ├── views.py (ViewSets + analysis endpoints)
│   ├── serializers.py
│   ├── urls.py
│   ├── tasks.py (Celery tasks for ingestion and pipeline)
│   ├── services/
│   │   ├── liquidity.py (zone, sweep, bias, FVG, OB detection)
│   │   ├── brokers.py (adapter interface)
│   │   └── ingestion.py (candle fetching and storage)
│   └── migrations/
├── journal/
│   ├── models.py (Trade, TradeNote, SetupTag, TradeAnalyticsSnapshot)
│   ├── views.py (ViewSets + analytics)
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
├── intel/
│   ├── models.py (BehaviorMetricDaily, BehaviorInsight)
│   ├── views.py (ViewSets + generation endpoint)
│   ├── serializers.py
│   ├── urls.py
│   ├── services/
│   │   └── behavioral.py (insight generation logic)
│   └── migrations/
├── paper/
│   ├── models.py (PaperAccount, PaperPosition)
│   ├── views.py (ViewSets)
│   ├── serializers.py
│   ├── urls.py
│   ├── services/
│   │   └── simulator.py (margin level recalculation)
│   └── migrations/
├── alerts/
│   ├── models.py (AlertRule, AlertEvent)
│   ├── views.py (ViewSets + Stripe webhook)
│   ├── serializers.py
│   ├── urls.py
│   ├── consumers.py (WebSocket consumer)
│   └── migrations/
├── billing/
│   ├── models.py (Plan, Subscription, Invoice)
│   ├── views.py (ViewSets + Stripe webhook)
│   ├── serializers.py
│   ├── urls.py
│   ├── services/
│   │   └── stripe_api.py (Stripe helpers)
│   └── migrations/
├── Dockerfile (Python 3.12 slim)
├── docker-compose.yml (web, worker, redis, postgres, nginx)
├── gunicorn.conf.py
├── nginx/default.conf
├── entrypoint.sh
├── requirements.txt
├── .env.example
├── PROJECT_SETUP.md
└── README.md (this file)
```

---

## Local Development Setup

### 1. Clone and install

```bash
git clone <REPO>
cd InnerEdge
```

### 2. Virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Environment file

```bash
cp .env.example .env
# Edit .env with your Stripe API keys and database settings
export DJANGO_DEBUG=1
export DB_ENGINE=sqlite  # or postgresql
```

### 4. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create admin user

```bash
python manage.py createsuperuser
```

### 6. Run local servers

**Web server** (Terminal 1):
```bash
python manage.py runserver
```

**Celery worker** (Terminal 2):
```bash
celery -A config worker -l info
```

**Redis** (if not in Docker):
```bash
redis-server
```

### 7. Test API

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/accounts/profiles/
```

---

## Docker Deployment

### Build and run with Docker Compose

```bash
docker compose up --build
```

This starts:
- **web** (Django on Gunicorn:8000)
- **worker** (Celery)
- **redis** (cache and message broker)
- **db** (PostgreSQL)
- **nginx** (reverse proxy on port 80)

### Access

- API: `http://localhost/api/`
- Admin: `http://localhost/admin/`

---

## Key API Endpoints

### Accounts
- `POST /api/accounts/profiles/` - Create profile
- `GET /api/accounts/profiles/{id}/` - Retrieve profile
- `PATCH /api/accounts/profiles/{id}/` - Update profile

### Market
- `GET/POST /api/market/assets/` - Asset CRUD
- `POST /api/market/assets/{id}/run-liquidity/` - Trigger SMC analysis
- `GET /api/market/liquidity-zones/` - Query zones
- `GET /api/market/sweep-events/` - Query sweeps
- `GET /api/market/fvg/` - Query FVGs
- `GET /api/market/order-blocks/` - Query order blocks
- `GET /api/market/daily-bias/` - Query daily bias

### Journal
- `GET/POST /api/journal/trades/` - Trade CRUD
- `GET /api/journal/trades/analytics/` - Win rate, PnL stats
- `GET/POST /api/journal/tags/` - Setup tags
- `GET/POST /api/journal/notes/` - Trade notes

### Intel
- `GET /api/intel/insights/` - List behavior insights
- `POST /api/intel/insights/generate/` - Trigger insight generation

### Paper
- `GET/POST /api/paper/accounts/` - Virtual account CRUD
- `POST /api/paper/accounts/{id}/recalculate/` - Recalculate margin

### Alerts
- `GET/POST /api/alerts/rules/` - Alert rule CRUD
- `GET /api/alerts/events/` - Alert event history
- `POST /api/alerts/events/{id}/mark-read/` - Mark notification as read

### Billing
- `GET /api/billing/plans/` - List subscription plans (public)
- `GET/POST /api/billing/subscriptions/` - User subscription CRUD
- `POST /api/billing/subscriptions/checkout/` - Generate Stripe checkout
- `GET /api/billing/invoices/` - Past invoices
- `POST /api/billing/stripe/webhook/` - Stripe webhook handler

---

## Celery Tasks

### Market Pipeline

```python
from market.tasks import run_liquidity_pipeline, ingest_asset_candles

# Ingest fresh candles
ingest_asset_candles.delay(asset_id=1, timeframe="H1", limit=500)

# Run SMC analysis
run_liquidity_pipeline.delay(asset_id=1, timeframe="H1")
```

---

## Stripe Integration

### 1. Configure env

```bash
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 2. Webhook endpoint

Configure Stripe dashboard to send events to: `https://yourdomain.com/api/billing/stripe/webhook/`

### 3. Event handling

Webhook handler automatically:
- Mirrors invoices to database
- Updates subscription status
- Manages plan transitions

---

## Authentication

Currently, the system expects **session-based** or **token authentication** via DRF defaults:
- `SessionAuthentication` (for session-based clients)
- `BasicAuthentication` (for API testing)

For production, add:
```python
'rest_framework.authentication.TokenAuthentication'  # or JWT
```

---

## Advanced Configuration

### PostgreSQL Connection

In `.env`:
```
DB_ENGINE=postgresql
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=inneredge
POSTGRES_USER=inneredge
POSTGRES_PASSWORD=<secure_password>
```

### Custom Broker Adapter

Extend `market.services.brokers.BrokerAdapter`:

```python
class CustomAdapter(BrokerAdapter):
    def fetch_candles(self, symbol, timeframe, limit):
        # Your broker API logic
        return [NormalizedCandle(...), ...]
```

Register in settings:

```python
BROKER_MAPPING = {"custom": CustomAdapter}
```

---

## Testing

```bash
python manage.py test
```

---

## Performance & Monitoring

- Use Redis for session/cache layer
- Celery tasks run async for heavy SMC calculations
- PostgreSQL indexes on (asset, timeframe, open_time) for fast candle queries
- Monitor Celery with Flower: `celery -A config events`

---

## License

Proprietary SaaS. Built for CFD traders following Atif Hussain's Smart Money Concepts philosophy.

---

## Contact & Support

For setup issues or feature requests, refer to the repo's wiki or contact the development team.
