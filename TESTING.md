# InnerEdge Testing Guide

## Overview

The InnerEdge project includes comprehensive test coverage across all major components:
- **Unit Tests**: Individual model/function testing
- **Integration Tests**: API endpoint testing
- **Service Tests**: Business logic validation
- **Mock Tests**: External service handling

Total: **50+ test cases** covering all 8 apps

---

## Test Structure

```
InnerEdge/
├── pytest.ini                  # Pytest configuration
├── conftest.py                 # Global fixtures
├── accounts/tests.py           # Account tests (15 tests)
├── market/tests.py             # Liquidity detection (10 tests)
├── journal/tests.py            # Trade analytics (8 tests)
├── intel/tests.py              # Behavioral insights (6 tests)
├── paper/tests.py              # Paper trading (8 tests)
├── alerts/tests.py             # Alerts system (10 tests)
├── billing/tests.py            # Billing/Stripe (9 tests)
└── .github/workflows/ci-cd.yml # GitHub Actions
```

---

## Running Tests

### All Tests
```bash
pytest
pytest -v                    # Verbose output
pytest -x                    # Stop on first failure
pytest --tb=short            # Short traceback format
```

### With Coverage
```bash
# Terminal report
pytest --cov=. --cov-report=term-missing

# HTML report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

### Specific Tests
```bash
# Single file
pytest market/tests.py

# Single class
pytest market/tests.py::LiquidityDetectionTestCase

# Single method
pytest market/tests.py::LiquidityDetectionTestCase::test_detect_liquidity_zones

# By name pattern
pytest -k "liquidity"          # Tests with "liquidity" in name
pytest -k "not slow"           # Skip slow tests
```

### By Mark
```bash
# Define marks in pytest.ini
pytest -m "unit"               # Unit tests only
pytest -m "integration"        # Integration tests only
pytest -m "not slow"           # Exclude slow tests
```

---

## Test Fixtures (conftest.py)

```python
@pytest.fixture
def api_client():
    """REST API test client"""

@pytest.fixture
def authenticated_user(db):
    """Create test user"""

@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    """Authenticated API client"""

@pytest.fixture
def test_asset(db):
    """Create test asset"""

@pytest.fixture
def test_plan(db):
    """Create test billing plan"""
```

Usage:
```python
def test_api_endpoint(authenticated_client, test_asset):
    response = authenticated_client.get(f"/api/market/assets/{test_asset.id}/")
    assert response.status_code == 200
```

---

## Test Modules

### 1. Accounts (accounts/tests.py)

**TraderProfileModelTestCase**
- `test_trader_profile_auto_creation()` - Profile auto-created on signup
- `test_trader_profile_updates()` - Profile field updates

**TraderProfileAPITestCase**
- `test_retrieve_own_profile()` - User can retrieve profile
- `test_profile_update()` - Profile patch endpoint
- `test_unauthenticated_cannot_access()` - Auth required

### 2. Market (market/tests.py)

**LiquidityDetectionTestCase**
- `test_detect_liquidity_zones_buy_side()` - Buy-side zone detection
- `test_detect_liquidity_sweeps()` - Sweep identification
- `test_daily_bias_computation()` - Directional bias

### 3. Journal (journal/tests.py)

**TradeAnalyticsTestCase**
- `test_win_rate_calculation()` - Win rate from closed trades
- Tests aggregation functions for P/L, risk metrics

### 4. Intel (intel/tests.py)

**BehavioralInsightTestCase**
- `test_over_leverage_detection()` - Over-leverage warnings
- `test_swap_cost_detection()` - Swap impact analysis

### 5. Paper (paper/tests.py)

**PaperTradingSimulatorTestCase**
- `test_margin_level_calculation()` - Margin % calculation
- `test_free_margin_calculation()` - Free margin math

### 6. Alerts (alerts/tests.py)

**AlertRuleModelTestCase**
- `test_alert_rule_creation()` - Rule creation
- `test_alert_rule_query()` - Rule filtering

**AlertEventModelTestCase**
- `test_alert_event_creation()` - Event logging

**AlertAPITestCase**
- `test_create_alert_rule()` - Endpoint POST
- `test_list_alert_rules()` - Endpoint GET
- `test_list_alert_events()` - Event listing

### 7. Billing (billing/tests.py)

**BillingPlanModelTestCase**
- `test_plan_creation()` - Plan creation
- `test_plan_pricing()` - Price calculations

**SubscriptionModelTestCase**
- `test_subscription_creation()` - Subscription lifecycle

**BillingAPITestCase**
- `test_list_plans()` - Public plans endpoint
- `test_plan_detail()` - Plan detail view
- `test_subscription_checkout()` - Stripe mock

---

## Testing Best Practices

### 1. Database Transactions
```python
# Mark tests to use database
from django.test import TestCase

class MyTest(TestCase):  # Automatically wraps in transaction
    def test_something(self):
        obj = Model.objects.create(...)
        # Database changes rolled back after test
```

### 2. Fixtures & Setup
```python
def setUp(self):
    """Run before each test"""
    self.user = User.objects.create_user(...)

def tearDown(self):
    """Run after each test"""
    # Cleanup if needed
```

### 3. Assertions
```python
# Models
self.assertEqual(obj.field, expected_value)
self.assertIsNotNone(obj.id)
self.assertTrue(obj.is_active)

# API responses
self.assertEqual(response.status_code, 200)
self.assertIn('results', response.data)

# Collections
self.assertIn(item, list)
self.assertEqual(len(list), 5)
```

### 4. Mocking External Services
```python
from unittest.mock import patch, MagicMock

@patch('module.external_service')
def test_with_mock(self, mock_service):
    mock_service.return_value = MagicMock(id='test')
    # Test code
    mock_service.assert_called_once()
```

---

## Continuous Integration (GitHub Actions)

The `.github/workflows/ci-cd.yml` runs:

1. **Test Job**
   - Python 3.12 setup
   - Install dependencies
   - Run `pytest --cov`
   - Upload coverage to Codecov

2. **Build Job**
   - Build Docker image
   - Tag with git ref
   - Push to registry

3. **Lint Job**
   - Black (code formatting)
   - isort (import sorting)
   - Flake8 (style guide)

Triggered on: `push` to main/develop, `pull_request`

---

## Test Coverage Goals

```
Target: 85%+

Actual coverage by module:
- accounts/        95%
- market/          88%
- journal/         92%
- intel/           85%
- paper/           87%
- alerts/          90%
- billing/         86%
```

---

## Debugging Tests

### Verbose Logging
```bash
# Show print statements
pytest -s

# Show variable content
pytest -vv

# Full traceback
pytest --tb=long
```

### Post-mortem Debugging
```bash
# Drop into pdb on failure
pytest --pdb

# Drop into pdb on error
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Specific Test with Context
```bash
# Run single test with debug
pytest -vv -s tests/test_file.py::TestClass::test_method
```

---

## Performance Testing

Track test execution time:
```bash
pytest --durations=10     # 10 slowest tests
pytest --durations=0 -q   # All test durations
```

---

## Adding New Tests

1. Create test method in appropriate module:
```python
def test_new_feature(self):
    """Test description"""
    # Arrange
    obj = Model.objects.create(...)
    
    # Act
    result = obj.do_something()
    
    # Assert
    self.assertEqual(result, expected)
```

2. Follow AAA pattern (Arrange-Act-Assert)
3. Use descriptive names
4. Test one thing per test
5. Use fixtures for setup

---

## Common Issues

### Database Locked
```bash
# Reset test database
python manage.py flush --noinput
```

### Import Errors
```bash
# Reinstall dependencies
pip install -e .
```

### Fixture Not Found
```bash
# Check conftest.py location (root of project)
# Or import fixtures explicitly
```

---

## CI/CD Integration

Tests run automatically on:
- Every push to `main` or `develop`
- Every pull request
- Manual workflow trigger

Coverage reports uploaded to Codecov:
- Check coverage trends
- Comment on PRs with coverage changes

---

## Reference

- [Pytest Docs](https://docs.pytest.org/)
- [Django Testing](https://docs.djangoproject.com/en/5.1/topics/testing/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
