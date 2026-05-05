# Component Resource Hierarchy Standards

**Applicable Modes**: Solution Architect, Code

## Overview

The Component Resource Hierarchy defines how system components are organized, how they interact, and the principles governing their relationships. This ensures maintainable, scalable architectures with clear boundaries and responsibilities.

## Core Principle: One Impact Per Resource

Every component should have a single, well-defined responsibility and receive only one primary impact from any change. This principle:
- Ensures clear ownership
- Simplifies testing
- Reduces coupling
- Improves maintainability

## Component hierarchy Levels

### Level 1: System
**Definition**: Top-level bounded context or major subsystem
**Examples**:
- Order Management System
- User Management System
- Payment System
- Inventory System

**Characteristics**:
- Independent deployment capability
- own data store
- Clear API boundaries
- Dedicated team ownership

### Level 2: Service
**Definition**: Functional unit within a system
**Examples**:
- OrderService within Order Management
- AuthenticationService within User Management
- PaymentProcessor within Payment System

**Characteristics**:
- Single responsibility
- Stateless operations
- Well-defined interface
- Can be scaled independently

### Level 3: Component
**Definition**: Building block within a service
**Examples**:
- OrderValidator component
- PriceCalculator component
- NotificationSender component

**Characteristics**:
- Focused functionality
- Reusable logic
- Clear input/output contract
- Testable in isolation

### Level 4: Module/Utility
**definition**: Shared functionality
**Examples**:
- DateFormatter utility
- CurrencyConverter module
- ValidationHelper utility

**Characteristics**:
- No business logic
- Purely functional
- Highly reusable
- No external dependencies

## Hierarchy Rules

### 1. Dependency Direction
Dependencies must flow downward in the hierarchy:
```
System → Service → Component → Module
```

**Allowed**:
- OrderService → OrderValidator (service uses component)
- OrderValidator → DateFormatter (component uses utility)

**Not Allowed**:
- DateFormatter → OrderService (utility depends on service)
- OrderValidator → PaymentService (cross-service direct dependency)

### 2. Communication Patterns

#### Within Same Level
- Components at same level communicate through parent
- Never direct peer-to-peer communication
- Use events or parent orchestration

```
❌ incorrect:
OrderValidator → InventoryChecker (direct communication)

✅ Correct:
OrderValidator → OrderService → InventoryChecker
```

#### Cross-System Communication
- Always through defined interfaces
- Use API contracts
- Never direct database access
- Prefer async where possible

```plantuml
@startuml
component "Order System" {
  component "OrderService" as OS
  component "OrderValidator" as OV
}

component "Inventory System" {
  component "InventoryService" as IS
  component "StockChecker" as SC
}

OS -> IS : API Call
note: Systems communicate via APIs
@enduml
```

## Component Design Standards

### 1. Single Responsibility
Each component must have ONE primary responsibility:

```yaml
OrderService:
  responsibility: Manage order lifecycle
  NOT responsible for:
    - Payment processing
    - User authentication
    - Inventory management
    
OrderValidator:
  responsibility: Validate order data
  NOT responsible for:
    - Saving orders
    - Calculating prices
    - Sending notifications
```

### 2. Interface Contracts
Every component must define:
- Input contract (what it accepts)
- Output contract (what it returns)
- Error contract (possible failures)
- SLA (performance expectations)

```typescript
interface OrderValidator {
  // Input contract
  input: {
    orderId: string;
    items: OrderItem[];
    customer: Customer;
  }
  
  // Output contract
  output: {
    isValid: boolean;
    errors?: ValidationError[];
  }
  
  // Error contract
  errors: {
    INVALID_ITEMS: "Items list cannot be empty";
    INVALID_CUSTOMER: "Customer data incomplete";
  }
  
  // SLA
  performance: {
    maxLatency: 100ms;
    availability: 99.9%;
  }
}
```

### 3. State Management

#### Stateless Components (Preferred)
- No internal state maintained
- Idempotent operations
- Easily scalable
- Simple testing

```python
class PriceCalculator:
    def calculate_total(self, items: List[Item]) -> Decimal:
        """Stateless calculation - no internal state"""
        return sum(item.price * item.quantity for item in items)
```

#### Stateful Components (When Necessary)
- Clearly documented state
- State persistence strategy
- Concurrency handling
- Recovery mechanisms

```python
class OrderProcessor:
    """Stateful component managing order workflow"""
    
    def __init__(self):
        self.state_store = StateStore()
        
    def process_order(self, order_id: str):
        current_state = self.state_store.get(order_id)
        # State-aware processing
```

## Resource Allocation Patterns

### Pattern 1: Vertical Slice
Each feature owns full stack of components:
```
Feature: Order Processing
├── OrderController (API layer)
├── OrderService (Business Logic)
├── OrderRepository (Data Access)
└── OrderValidator (Validation)
```

### Pattern 2: Layered Components
Components organized by technical layers:
```
API Layer
├── OrderController
├── PaymentController
└── UserController

Service Layer
├── orderService
├── PaymentService
└── UserService

Data Layer
├── OrderRepository
├── PaymentRepository
└── UserRepository
```

### Pattern 3: Domain-Driven Components
Components organized by business domain:
```
Orders Domain
├── OrderAggregate
├── OrderService
├── OrderRepository
└── OrderEventHandler

Payments Domain
├── PaymentAggregate
├── PaymentService
├── PaymentRepository
└── PaymentEventHandler
```

## Component interaction Standards

### Synchronous Communication
Use when:
- immediate response required
- Simple request/response
- Within same service boundary
- Low latency critical

```python
# Direct method call
class OrderService:
    def __init__(self, validator: OrderValidator):
        self.validator = validator
    
    def create_order(self, order_data: dict):
        # Sync call to component
        validation_result = self.validator.validate(order_data)
        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)
```

### Asynchronous Communication
Use when:
- No immediate response needed
- Cross-system communication
- Long-running operations
- Resilience important

```python
# Event-driven communication
class OrderService:
    def create_order(self, order_data: dict):
        # Async event publishing
        self.event_bus.publish({
            'event_type': 'OrderCreated',
            'data': order_data
        })
```

## Component Testing Strategy

### Unit Testing
Test components in isolation:
```python
def test_order_validator():
    # Test component in isolation
    validator = OrderValidator()
    
    # Mock dependencies if any
    result = validator.validate({
        'items': [],
        'customer_id': '123'
    })
    
    assert result.is_valid is False
    assert 'items_required' in result.errors
```

### Integration Testing
Test component interactions:
```python
def test_order_service_integration():
    # Test service with real components
    validator = OrderValidator()
    repository = MockOrderRepository()
    service = OrderService(validator, repository)
    
    order = service.create_order({'items': [...]})
    assert order.status == 'created'
```

## Anti-Patterns to Avoid

### 1. God Components
Components doing too much:
```python
# ❌ BAD - Multiple responsibilities
class OrderManager:
    def validate_order(self, order): ...
    def calculate_price(self, order): ...
    def send_notification(self, order): ...
    def update_inventory(self, order): ...
```

### 2. Circular Dependencies
Components depending on each other:
```
❌ OrderService → PaymentService → InventoryService → OrderService
```

### 3. Leaky Abstractions
Components exposing internal details:
```python
# ❌ BAD - Exposing internal structure
class OrderService:
    def get_order_with_internal_flags(self, id):
        return self._internal_repository._get_with_flags(id)
```

## Component Documentation

### Required Documentation
```python
class PriceCalculator:
    """
    CalculatES pricing for orders with discounts and taxes.
    
    Responsibilities:
    - Apply discount rules
    - Calculate taxes
    - Handle currency conversion
    
    NOT Responsible For:
    - Persisting prices
    - Validating payment methods
    - Processing payments
    
    Dependencies:
    - TaxService (for tax rates)
    - CurrencyService (for conversion)
    
    Performance:
    - Max latency: 50ms
    - Throughput: 1000 req/sec
    """
```

## Metrics and Monitoring

### Component Health Metrics
- Response time per operation
- Error rate by type
- Throughput metrics
- Dependency health
- Resource utilization

### Hierarchy Metrics
- Cross-component calls
- Dependency violations
- Component complexity
- Coupling metrics

## Best Practices

### Do's ✅
1. Define clear boundaries
2. Document responsibilities
3. Version interfaces
4. Monitor interactions
5. Regular refactoring

### Don'ts ❌
1. Skip interface definitions
2. Allow circular dependencies
3. Mix concerns in components
4. Ignore performance SLAs
5. Create deep hierarchies (>5 levels)

---

The Component Resource Hierarchy ensures system maintainability by enforcing clear boundaries, single responsibilities, and predictable interactions between components at every level of the architecture.