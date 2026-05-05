# Behavior-Driven Development (BDD) and Test-Driven Development (TDD) Methodology

**Applicable Modes**: Code, Debug, VS Code Plugin

## Overview

BDD and TDD are complementary methodologies that ensure high-quality, well-tested code through a test-first approach. BDD focuses on behavior from a user perspective, while TDD focuses on technical implementation.

## Behavior-Driven Development (BDD)

### Core Principles
1. **Behavior First** - Define what the system should do before how
2. **Shared Understanding** - Use language all stakeholders understand
3. **Living Documentation** - Tests serve as executable specifications
4. **Outside-In** - Start from user perspective, work toward implementation

### Given-When-Then Format

```gherkin
Feature: User Authentication
  As a user
  I want to log in to the system
  So that I can access my personal dashboard

  Scenario: Successful login with valid credentials
    Given I am on the login page
    And I have a valid username "user@example.com"
    And I have a valid password "SecurePass123"
    When I enter my credentials
    And I click the login button
    Then I should be redirected to my dashboard
    And I should see a welcome message "Welcome back, User!"

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    And I have an invalid username "wrong@example.com"
    When I enter my credentials
    And I click the login button
    Then I should remain on the login page
    And I should see an error message "Invalid credentials"
```

### BDD Process Flow

1. **Discovery** - Collaborate to understand the feature
2. **Formulation** - Write scenarios in Given-When-Then format
3. **Automation** - Implement step definitions
4. **Implementation** - Write code to make tests pass
5. **Validation** - Ensure all scenarios pass

### BDD Best Practices

#### Scenario Writing
- Keep scenarios focused on single behaviors
- Use business language, not technical jargon
- Make scenarios independent
- Avoid implementation details
- Include both happy and unhappy paths

#### Example: Good vs Bad Scenarios

❌ **Bad - Too Technical**:
```gherkin
Scenario: Database update
  Given the user table has a record with id=123
  When I execute UPDATE user SET status='active'
  Then the database should return 1 row affected
```

✅ **Good - Business Focused**:
```gherkin
Scenario: Activate user account
  Given a deactivated user account exists
  When an administrator activates the account
  Then the user should be able to log in
```

## Test-Driven Development (TDD)

### The TDD Cycle (Red-Green-Refactor)

1. **Red** - Write a failing test
2. **Green** - Write minimum code to pass
3. **Refactor** - Improve code while keeping tests green

### TDD Process Example

#### Step 1: Write Failing Test (Red)
```python
def test_calculate_discount():
    # Test for 10% discount on orders over $100
    assert calculate_discount(150) == 15
    assert calculate_discount(50) == 0
    assert calculate_discount(100) == 0
    assert calculate_discount(101) == 10.1
```

#### Step 2: Write Minimum Code (Green)
```python
def calculate_discount(order_total):
    if order_total > 100:
        return order_total * 0.1
    return 0
```

#### Step 3: Refactor
```python
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.1

def calculate_discount(order_total):
    """Calculate discount for orders over threshold."""
    if order_total > DISCOUNT_THRESHOLD:
        return order_total * DISCOUNT_RATE
    return 0
```

### TDD Best Practices

1. **One Test at a Time** - Focus on single behavior
2. **Keep Tests Small** - Test one thing per test
3. **Fast Tests** - Tests should run quickly
4. **Independent Tests** - No test should depend on another
5. **Descriptive Names** - Test names should explain what they test

## Integrating BDD and TDD

### Workflow Integration

1. **Start with BDD** - Define feature behavior
2. **Break into Units** - Identify components needed
3. **Apply TDD** - Build components test-first
4. **Connect Layers** - Integrate unit tests with BDD scenarios

### Example: Feature to Implementation

#### BDD Scenario
```gherkin
Scenario: Calculate order total with tax
  Given I have items worth $100 in my cart
  And my location has 8% sales tax
  When I proceed to checkout
  Then my total should be $108
```

#### TDD Implementation
```python
# Test tax calculation
def test_calculate_tax():
    assert calculate_tax(100, 0.08) == 8
    assert calculate_tax(50, 0.10) == 5

# Test order total
def test_calculate_order_total():
    items = [{"price": 50}, {"price": 50}]
    assert calculate_order_total(items, 0.08) == 108

# Implementation
def calculate_tax(subtotal, tax_rate):
    return subtotal * tax_rate

def calculate_order_total(items, tax_rate):
    subtotal = sum(item["price"] for item in items)
    tax = calculate_tax(subtotal, tax_rate)
    return subtotal + tax
```

## Testing Patterns and Anti-Patterns

### Patterns (Good Practices)

#### Arrange-Act-Assert (AAA)
```python
def test_user_registration():
    # Arrange
    user_data = {"email": "test@example.com", "password": "secure123"}
    
    # Act
    result = register_user(user_data)
    
    # Assert
    assert result.success is True
    assert result.user.email == "test@example.com"
```

#### Test Data Builders
```python
class UserBuilder:
    def __init__(self):
        self.email = "default@example.com"
        self.password = "password123"
    
    def with_email(self, email):
        self.email = email
        return self
    
    def build(self):
        return User(email=self.email, password=self.password)

# Usage
user = UserBuilder().with_email("custom@example.com").build()
```

### Anti-Patterns (Avoid These)

#### Testing Implementation Details
❌ **Bad**:
```python
def test_internal_method_called():
    mock_internal = Mock()
    obj._internal_method = mock_internal
    obj.public_method()
    mock_internal.assert_called_once()
```

✅ **Good**:
```python
def test_public_behavior():
    result = obj.public_method()
    assert result == expected_value
```

#### Overly Complex Tests
❌ **Bad**:
```python
def test_everything():
    # 100 lines of setup
    # Multiple assertions
    # Testing multiple behaviors
```

✅ **Good**:
```python
def test_specific_behavior():
    # Minimal setup
    # Single logical assertion
    # One behavior tested
```

## Test Organization

### Directory Structure
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_database_operations.py
├── bdd/
│   ├── features/
│   │   ├── authentication.feature
│   │   └── order_processing.feature
│   └── steps/
│       ├── authentication_steps.py
│       └── order_steps.py
└── fixtures/
    └── test_data.py
```

## Coverage Standards

### Minimum Coverage Requirements
- Unit Tests: 80% code coverage
- Integration Tests: Critical paths covered
- BDD Scenarios: All user-facing features

### What to Test
1. **Business Logic** - Always test
2. **Edge Cases** - Boundary conditions
3. **Error Handling** - Exception paths
4. **Integration Points** - External dependencies
5. **Security Controls** - Authentication/authorization

### What Not to Test
1. **Framework Code** - Trust the framework
2. **Simple Getters/Setters** - Unless they have logic
3. **Configuration** - Test behavior, not config
4. **External Libraries** - Mock them instead

## Mode-Specific Applications

### Code Mode
- Write tests before implementation
- Follow TDD cycle strictly
- Ensure comprehensive test coverage
- Include both unit and integration tests

### Debug Mode
- Use tests to identify issues
- Write tests to reproduce bugs
- Verify fixes with tests
- Add regression tests

### VS Code Plugin Mode
- Test extension activation
- Test command execution
- Test UI interactions
- Include end-to-end tests

## Testing Checklist

Before considering code complete:
- [ ] BDD scenarios defined for user-facing features
- [ ] Unit tests written for all business logic
- [ ] Integration tests for external dependencies
- [ ] Edge cases and error paths tested
- [ ] Tests are independent and repeatable
- [ ] Tests run quickly (< 10 minutes for full suite)
- [ ] Test names clearly describe what they test
- [ ] No test relies on external services without mocks
- [ ] Coverage meets minimum standards
- [ ] All tests pass in CI/CD pipeline

---

Remember: In BDD/TDD, tests are not an afterthought—they drive the design and implementation. Always write tests first, then make them pass with the simplest code possible.