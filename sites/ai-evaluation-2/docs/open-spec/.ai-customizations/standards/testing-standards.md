# Testing Standards

**Applicable Modes**: Code, Debug, VS Code Plugin

## Overview

Testing is mandatory for all code deliverables. This document defines the testing standards, patterns, and requirements that ensure high-quality, maintainable software across the enterprise.

## Testing Hierarchy

### 1. Unit Tests
**Purpose**: Test individual components in isolation
**Coverage Target**: 80% minimum
**Execution Time**: < 100ms per test

```python
# Example Python Unit Test
def test_calculate_discount():
    # Arrange
    order_total = 150.00
    discount_rate = 0.10
    
    # Act
    discount = calculate_discount(order_total, discount_rate)
    
    # Assert
    assert discount == 15.00
```

```javascript
// Example JavaScript Unit Test
describe('OrderService', () => {
  describe('calculateTotal', () => {
    it('should calculate total with tax', () => {
      // Arrange
      const items = [{ price: 10 }, { price: 20 }];
      const taxRate = 0.08;
      
      // Act
      const total = calculateTotal(items, taxRate);
      
      // Assert
      expect(total).toBe(32.40);
    });
  });
});
```

### 2. Integration Tests
**Purpose**: Test component interactions
**Coverage Target**: Critical paths covered
**Execution Time**: < 5 seconds per test

```python
# Example Integration Test
def test_order_processing_flow():
    # Arrange
    order_service = OrderService()
    payment_service = PaymentService()
    inventory_service = InventoryService()
    
    order_data = {
        "items": [{"sku": "ABC123", "quantity": 2}],
        "payment": {"method": "credit_card"}
    }
    
    # Act
    order = order_service.create_order(order_data)
    payment_result = payment_service.process_payment(order)
    inventory_result = inventory_service.update_inventory(order)
    
    # Assert
    assert order.status == "completed"
    assert payment_result.success is True
    assert inventory_result.updated is True
```

### 3. End-to-End Tests
**Purpose**: Test complete user workflows
**Coverage Target**: Critical user journeys
**Execution Time**: < 30 seconds per test

```javascript
// Example E2E Test with Playwright
test('user can complete purchase', async ({ page }) => {
  // Navigate to site
  await page.goto('https://shop.example.com');
  
  // Add item to cart
  await page.click('[data-testid="add-to-cart-ABC123"]');
  
  // Go to checkout
  await page.click('[data-testid="checkout-button"]');
  
  // Fill payment info
  await page.fill('[data-testid="card-number"]', '4111111111111111');
  
  // Complete purchase
  await page.click('[data-testid="complete-purchase"]');
  
  // Verify success
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
});
```

## Test Organization Standards

### Directory Structure
```
tests/
├── unit/
│   ├── services/
│   │   ├── test_order_service.py
│   │   ├── test_payment_service.py
│   │   └── test_inventory_service.py
│   ├── utils/
│   │   ├── test_validators.py
│   │   └── test_formatters.py
│   └── models/
│       ├── test_order_model.py
│       └── test_user_model.py
├── integration/
│   ├── test_order_workflow.py
│   ├── test_payment_processing.py
│   └── test_api_endpoints.py
├── e2e/
│   ├── test_purchase_flow.py
│   ├── test_user_registration.py
│   └── test_admin_functions.py
└── fixtures/
    ├── test_data.py
    ├── mock_services.py
    └── factories.py
```

### Naming Conventions
- Test files: `test_[module_name].py` or `[module_name].test.js`
- Test classes: `Test[ClassName]`
- Test methods: `test_[specific_behavior]`
- BDD scenarios: `should_[expected_behavior]_when_[condition]`

## Testing Patterns

### Arrange-Act-Assert (AAA)
Every test should follow this pattern:

```python
def test_user_registration():
    # Arrange - Set up test data and conditions
    user_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    user_service = UserService()
    
    # Act - Execute the behavior being tested
    result = user_service.register(user_data)
    
    # Assert - Verify the outcome
    assert result.success is True
    assert result.user.email == user_data["email"]
    assert result.user.is_active is False  # Requires email verification
```

### Test Data Builders
Use builders for complex test data:

```python
class OrderBuilder:
    def __init__(self):
        self.order = {
            "id": str(uuid.uuid4()),
            "items": [],
            "customer": None,
            "status": "pending"
        }
    
    def with_items(self, items):
        self.order["items"] = items
        return self
    
    def with_customer(self, customer):
        self.order["customer"] = customer
        return self
    
    def with_status(self, status):
        self.order["status"] = status
        return self
    
    def build(self):
        return Order(**self.order)

# Usage in tests
order = (OrderBuilder()
    .with_items([{"sku": "ABC", "quantity": 2}])
    .with_customer({"id": "123", "email": "test@example.com"})
    .with_status("processing")
    .build())
```

### Mock and Stub Patterns

#### Mocking External Services
```python
from unittest.mock import Mock, patch

def test_order_with_payment_service():
    # Create mock payment service
    mock_payment = Mock()
    mock_payment.process.return_value = {"status": "approved", "id": "PAY123"}
    
    # Inject mock
    order_service = OrderService(payment_service=mock_payment)
    
    # Test behavior
    result = order_service.complete_order(order_id="ORD123")
    
    # Verify interactions
    mock_payment.process.assert_called_once_with(amount=100.00, order_id="ORD123")
    assert result.payment_id == "PAY123"
```

#### Stubbing Database Calls
```javascript
// Using sinon for stubbing
const sinon = require('sinon');
const UserRepository = require('./UserRepository');

describe('UserService', () => {
  let userRepoStub;
  
  beforeEach(() => {
    userRepoStub = sinon.stub(UserRepository.prototype, 'findById');
  });
  
  afterEach(() => {
    userRepoStub.restore();
  });
  
  it('should get user by id', async () => {
    // Arrange
    userRepoStub.returns({ id: '123', name: 'Test User' });
    
    // Act
    const user = await userService.getUser('123');
    
    // Assert
    expect(user.name).toBe('Test User');
  });
});
```

## Test Quality Standards

### 1. Test Independence
- Each test must be able to run in isolation
- No dependencies between tests
- Clean up test data after execution

### 2. Test Clarity
```python
# ❌ Bad - Unclear test name and assertions
def test_1():
    u = User("test@example.com")
    assert u.e == "test@example.com"

# ✅ Good - Clear test name and assertions
def test_user_email_is_stored_correctly():
    # Given a user with a specific email
    email = "test@example.com"
    user = User(email=email)
    
    # Then the email should be stored correctly
    assert user.email == email
```

### 3. Test Performance
- Unit tests: < 100ms
- Integration tests: < 5s
- E2E tests: < 30s
- Full test suite: < 10 minutes

### 4. Test Coverage
```yaml
# Coverage requirements by component type
coverage:
  business_logic: 90%  # Critical business rules
  api_endpoints: 85%   # Public APIs
  utilities: 80%       # Helper functions
  ui_components: 70%   # Frontend components
  infrastructure: 60%  # Config and setup
```

## Specialized Testing

### API Testing
```python
def test_api_create_order():
    # Arrange
    client = TestClient(app)
    order_data = {
        "items": [{"sku": "ABC123", "quantity": 2}],
        "shipping_address": "123 Main St"
    }
    
    # Act
    response = client.post("/api/orders", json=order_data)
    
    # Assert
    assert response.status_code == 201
    assert "order_id" in response.json()
    assert response.json()["status"] == "pending"
```

### Performance Testing
```python
def test_bulk_processing_performance():
    # Arrange
    items = [create_test_item() for _ in range(1000)]
    processor = BulkProcessor()
    
    # Act
    start_time = time.time()
    results = processor.process_items(items)
    end_time = time.time()
    
    # Assert
    processing_time = end_time - start_time
    assert processing_time < 5.0  # Should process 1000 items in under 5 seconds
    assert len(results) == 1000
```

### Security Testing
```python
def test_sql_injection_prevention():
    # Arrange
    malicious_input = "'; DROP TABLE users; --"
    user_service = UserService()
    
    # Act & Assert
    with pytest.raises(ValidationError):
        user_service.find_by_name(malicious_input)
```

## Test Documentation

### Test Case Documentation
```python
def test_discount_calculation_for_vip_customers():
    """
    Test that VIP customers receive correct discount tiers.
    
    Given: A VIP customer with various order amounts
    When: Calculating discounts
    Then: Correct discount percentages are applied
    
    Business Rule: 
    - Orders > $1000: 20% discount
    - Orders $500-$1000: 15% discount
    - Orders < $500: 10% discount
    """
    # Test implementation...
```

### Test Data Documentation
```python
# fixtures/test_customers.py
"""
Test customer data for various scenarios.

VIP_CUSTOMER: Has VIP status, high purchase history
REGULAR_CUSTOMER: Standard customer, normal purchase history
NEW_CUSTOMER: Recently registered, no purchase history
BLOCKED_CUSTOMER: Account blocked for policy violations
"""
```

## Continuous Integration Standards

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: unit-tests
        name: Run unit tests
        entry: pytest tests/unit/
        language: system
        pass_filenames: false
```

### CI Pipeline
```yaml
# Example GitHub Actions
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Run Unit Tests
      run: pytest tests/unit/ --cov=src --cov-report=xml
    - name: Run Integration Tests
      run: pytest tests/integration/
    - name: Check Coverage
      run: |
        coverage report --fail-under=80
```

## Testing Checklist

Before code review:
- [ ] All new code has corresponding tests
- [ ] Tests follow AAA pattern
- [ ] Test names clearly describe behavior
- [ ] No hard-coded test data
- [ ] Tests run independently
- [ ] Coverage meets minimum requirements
- [ ] Performance benchmarks met
- [ ] No flaky tests
- [ ] Test documentation updated
- [ ] CI pipeline passes

---

Remember: Tests are not just about coverage—they're about confidence. Write tests that give you confidence your code works correctly and will continue to work as the system evolves.