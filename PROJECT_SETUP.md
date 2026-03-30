# InnerEdge Backend Setup

## 1) Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Copy environment file:

```bash
cp .env.example .env
```

1. Run migrations and start server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 2) Background Worker

Run Celery in a separate terminal:

```bash
celery -A config worker -l info
```

## 3) Docker Deployment

```bash
docker compose up --build
```

## 4) API Modules

- Accounts: `/api/accounts/`
- Market: `/api/market/`
- Journal: `/api/journal/`
- Intelligence: `/api/intel/`
- Paper Trading: `/api/paper/`
- Alerts: `/api/alerts/`
- Billing: `/api/billing/`

## 5) Trading Philosophy Encoded

- Bias and sweep logic prioritize liquidity flow before secondary indicators.
- FVG and Order Blocks are available as confluence-only outputs.
- AI module generates behavioral insights, not market predictions.

## 6) Verification Commands

- Run complete checks on Windows:

```bat
scripts\verify.bat
```

- Run complete checks on Bash:

```bash
bash scripts/verify.sh
```

## 7) Optional Pre-Commit Setup

Install and enable pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

Run hooks manually:

```bash
pre-commit run --all-files
```
