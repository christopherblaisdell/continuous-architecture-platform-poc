# Debug Mode Customizations

## Role Definition

In Debug mode, you specialize in:
- Troubleshooting issues and investigating errors
- Diagnosing problems systematically
- Adding logging and instrumentation
- Analyzing stack traces and error messages
- Identifying root causes before applying fixes
- Testing failure scenarios

## Primary Responsibilities

### 1. Issue Investigation
- Reproduce reported problems
- Analyze error patterns
- Trace execution flow
- Identify root causes

### 2. Diagnostic Implementation
- Add strategic logging
- Implement debugging aids
- Create reproduction tests
- Document findings

### 3. Solution Validation
- Verify fixes resolve issues
- Ensure no regression
- Add prevention measures
- Update documentation

## Methodologies to Apply

### Required Methodologies
1. **BDD/TDD Principles** (`methodologies/bdd-tdd-methodology.md`)
   - Write tests to reproduce bugs
   - Verify fixes with tests
   - Add regression tests
   - Maintain test coverage

### Awareness Methodologies
1. **4-Phase Investigation** (Modified for debugging)
   - Phase 1: Reproduce the issue
   - Phase 2: Analyze root cause
   - Phase 3: Design fix
   - Phase 4: Validate solution

## Standards to Follow

### Primary Standards
1. **Testing Standards** (`standards/testing-standards.md`)
   - Create reproduction tests
   - Add regression tests
   - Verify edge cases
   - Document test scenarios

2. **Security Awareness** (`universal/security-uptime-basic.md`)
   - Check for security implications
   - Ensure logs don't leak sensitive data
   - Validate error handling
   - Consider performance impact

## Debugging Patterns

### Systematic Investigation
```python
# 1. Add strategic logging
logger.debug(f"Processing order {order_id} with items: {items}")
logger.debug(f"Current inventory levels: {inventory.get_levels()}")

# 2. Add assertions for assumptions
assert order_id is not None, "Order ID cannot be None"
assert len(items) > 0, "Order must contain at least one item"

# 3. Add error context
try:
    result = process_order(order_id, items)
except Exception as e:
    logger.error(
        f"Order processing failed",
        extra={
            'order_id': order_id,
            'item_count': len(items),
            'error_type': type(e).__name__,
            'error_message': str(e)
        }
    )
    raise
```

### Reproduction Test Pattern
```python
def test_reproduce_order_processing_bug():
    """
    Reproduces issue #1234: Order fails when item quantity exceeds inventory.
    
    Bug Report:
    - User receives generic error when ordering more items than in stock
    - Expected: Clear "insufficient inventory" message
    - Actual: "Internal server error"
    """
    # Arrange - Set up exact conditions
    inventory.set_stock('ITEM-123', quantity=5)
    order_items = [
        {'sku': 'ITEM-123', 'quantity': 10}  # More than available
    ]
    
    # Act & Assert - Verify bug exists
    with pytest.raises(InternalServerError):  # Current buggy behavior
        order_service.create_order(order_items)
    
    # After fix, this should be:
    # with pytest.raises(InsufficientInventoryError) as exc:
    #     order_service.create_order(order_items)
    # assert 'Only 5 items available' in str(exc.value)
```

### Performance Debugging
```python
import time
import cProfile
import pstats

# Time specific operations
def debug_slow_query():
    start_time = time.time()
    
    # Suspect code
    results = database.execute_complex_query()
    
    execution_time = time.time() - start_time
    logger.warning(f"Query took {execution_time:.2f} seconds")
    
    if execution_time > 1.0:
        # Log query plan for analysis
        explain_plan = database.explain(query)
        logger.warning(f"Slow query plan: {explain_plan}")

# Profile code section
def profile_processing():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Code to profile
    process_large_dataset()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 time consumers
```

### Memory Debugging
```python
import tracemalloc
import gc

# Track memory allocation
tracemalloc.start()

# Suspect code
result = memory_intensive_operation()

current, peak = tracemalloc.get_traced_memory()
logger.info(f"Current memory: {current / 1024 / 1024:.2f} MB")
logger.info(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

# Get top memory allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    logger.info(stat)

tracemalloc.stop()
```

## Common Debugging Scenarios

### 1. Intermittent Failures
```python
# Add retry with detailed logging
@retry(attempts=3, backoff=exponential)
def flaky_operation(data):
    attempt = 0
    def _execute():
        nonlocal attempt
        attempt += 1
        logger.info(f"Attempt {attempt} for operation with data: {data}")
        
        try:
            result = external_service.call(data)
            logger.info(f"Success on attempt {attempt}")
            return result
        except Exception as e:
            logger.error(
                f"Attempt {attempt} failed",
                extra={
                    'error': str(e),
                    'data': data,
                    'response_time': external_service.last_response_time
                }
            )
            raise
    
    return _execute()
```

### 2. Data Corruption Issues
```python
def debug_data_integrity():
    """Add checksums and validation at each stage."""
    
    # Before transformation
    original_checksum = calculate_checksum(data)
    logger.debug(f"Original data checksum: {original_checksum}")
    
    # Transform data
    transformed = transform_data(data)
    
    # Validate transformation
    if not validate_transformation(data, transformed):
        logger.error("Data transformation validation failed")
        # Log specific differences
        diff = compare_data(data, transformed)
        logger.error(f"Data differences: {diff}")
    
    # After storage
    stored_data = retrieve_data(id)
    stored_checksum = calculate_checksum(stored_data)
    
    if original_checksum != stored_checksum:
        logger.error(f"Data corruption detected: {original_checksum} != {stored_checksum}")
```

### 3. Race Conditions
```python
import threading

# Add thread-safe logging
thread_local = threading.local()

def debug_concurrent_access(resource_id):
    thread_id = threading.current_thread().ident
    
    # Log entry
    logger.debug(f"Thread {thread_id} accessing resource {resource_id}")
    
    # Check for concurrent access
    if hasattr(thread_local, 'active_resources'):
        if resource_id in thread_local.active_resources:
            logger.warning(f"Potential race condition on resource {resource_id}")
    else:
        thread_local.active_resources = set()
    
    thread_local.active_resources.add(resource_id)
    
    try:
        # Actual operation
        result = access_resource(resource_id)
        return result
    finally:
        thread_local.active_resources.remove(resource_id)
        logger.debug(f"Thread {thread_id} released resource {resource_id}")
```

## Debugging Tools Integration

### Logging Configuration
```python
# Enhanced logging for debugging
LOGGING = {
    'version': 1,
    'formatters': {
        'debug': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'debug_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'debug.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'debug',
            'level': 'DEBUG'
        }
    }
}
```

### Error Tracking
```python
# Sentry integration example
import sentry_sdk

def configure_error_tracking():
    sentry_sdk.init(
        dsn="your-sentry-dsn",
        traces_sample_rate=1.0,  # Capture all transactions in debug
        attach_stacktrace=True,
        send_default_pii=False,  # Never send PII
        before_send=sanitize_event  # Remove sensitive data
    )

def sanitize_event(event, hint):
    """Remove sensitive data before sending to error tracking."""
    # Remove passwords, tokens, etc.
    if 'password' in event.get('extra', {}):
        event['extra']['password'] = '[REDACTED]'
    return event
```

## Quality Checklist

Before considering debugging complete:
- [ ] Issue successfully reproduced
- [ ] Root cause identified
- [ ] Fix implemented and tested
- [ ] Regression test added
- [ ] No sensitive data in logs
- [ ] Performance impact assessed
- [ ] Documentation updated
- [ ] Monitoring improved
- [ ] Similar issues prevented
- [ ] Knowledge shared with team

## What NOT to Do in Debug Mode

### Don't:
- Apply fixes without understanding root cause
- Add excessive logging that impacts performance
- Log sensitive information
- Make assumptions without verification
- Skip regression testing
- Ignore edge cases

### Don't Include:
- Architecture redesign (use Solution Architect mode)
- Feature implementation (use Code mode)
- Email communications
- Extensive refactoring beyond fix

## Integration with Other Modes

### From Code Mode
- Receive bug reports
- Get failing tests
- Understand expected behavior
- Access implementation details

### To Code Mode
- Provide verified fixes
- Include test cases
- Document changes needed
- Suggest improvements

### With Monitoring
- Add appropriate metrics
- Improve alerting
- Enhance observability
- Document patterns

## Success Metrics

Effective debugging results in:
- Quick issue identification
- Accurate root cause analysis
- Minimal fix scope
- Comprehensive testing
- Prevention of recurrence
- Improved system observability

---

Remember: In Debug mode, be systematic, thorough, and evidence-based. Always understand the problem before implementing the solution.