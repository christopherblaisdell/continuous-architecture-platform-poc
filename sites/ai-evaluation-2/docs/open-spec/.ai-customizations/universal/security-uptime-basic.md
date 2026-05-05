# Security and Uptime Basic Awareness - Universal Application

All modes MUST maintain basic security and uptime awareness. These are non-negotiable requirements for all UDX systems and solutions.

## Core Security Principles

### Security-First Mindset
- **Assume Breach**: Design assuming attackers will get in
- **Defense in Depth**: Multiple layers of security
- **Least Privilege**: Minimum access necessary
- **Zero Trust**: Verify everything, trust nothing

### Universal Security Considerations

#### Data Classification
Always consider:
- **Public**: Generally available information
- **Internal**: UDX internal use only
- **Confidential**: Restricted access required
- **Secret**: Highest protection needed

#### Basic Security Questions
For EVERY solution/recommendation:
1. What data is being accessed?
2. Who can access this data?
3. How is access controlled?
4. What happens if compromised?
5. How do we detect issues?

## Uptime Requirements

### Standard Uptime Tiers
- **99.9%** (Three nines): ~8.76 hours downtime/year
- **99.95%** (Three and a half nines): ~4.38 hours downtime/year
- **99.99%** (Four nines): ~52.56 minutes downtime/year
- **99.999%** (Five nines): ~5.26 minutes downtime/year

### Uptime Considerations
Every solution must consider:
- Single points of failure
- Redundancy requirements
- Failover mechanisms
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)

## Security in Different Contexts

### Architecture & Design (SA, Orchestrator)
- Design with security boundaries
- Document trust zones
- Identify attack surfaces
- Plan for incident response

### Development (Code, Debug, VS Code Plugin)
- Never hard-code credentials
- Validate all inputs
- Use secure coding practices
- Consider OWASP Top 10

### Documentation (Compliance, Ask)
- Never include real credentials
- Sanitize sensitive examples
- Mark security classifications
- Protect internal details

## Common Security Anti-Patterns

### Never Do This
❌ **Credentials in Code**
```python
# NEVER DO THIS
api_key = "sk-1234567890abcdef"
password = "MySecretPassword123!"
```

❌ **Unvalidated Input**
```javascript
// NEVER DO THIS
const userInput = request.body.data;
database.query(`SELECT * FROM users WHERE id = ${userInput}`);
```

❌ **Overly Permissive Access**
```yaml
# NEVER DO THIS
permissions:
  - "*:*"  # Grants everything to everyone
```

### Always Do This
✅ **Environment Variables**
```python
# CORRECT
api_key = os.environ.get('API_KEY')
password = aws_secrets.get_secret('db_password')
```

✅ **Input Validation**
```javascript
// CORRECT
const userId = parseInt(request.body.userId);
if (!isValidUserId(userId)) {
    throw new ValidationError('Invalid user ID');
}
```

✅ **Least Privilege**
```yaml
# CORRECT
permissions:
  - "s3:GetObject"  # Only what's needed
  - "s3:PutObject"  # For specific bucket
```

## Uptime Best Practices

### Design Patterns
1. **Redundancy**: No single points of failure
2. **Graceful Degradation**: Partial service better than none
3. **Circuit Breakers**: Prevent cascade failures
4. **Health Checks**: Continuous monitoring
5. **Autoscaling**: Handle load variations

### Common Uptime Threats
- Resource exhaustion
- Dependency failures
- Network partitions
- Configuration errors
- Deployment issues

## Security Incident Awareness

### If Security Concerns Arise
1. **Stop**: Don't proceed with insecure design
2. **Document**: Note the security concern
3. **Escalate**: Recommend security review
4. **Alternative**: Suggest secure approach

### Red Flags
- Storing passwords in plain text
- Direct database access from frontend
- No authentication on APIs
- Shared credentials
- No encryption for sensitive data

## Mode-Specific Applications

### All Modes Must
- Consider security implications
- Document security decisions
- Highlight security risks
- Recommend secure alternatives
- Never compromise security for convenience

### Enhanced Requirements by Mode
- **Solution Architect**: Full threat modeling
- **Code**: Secure coding practices
- **Debug**: Security-aware troubleshooting
- **Compliance**: Security documentation
- **Orchestrator**: Security coordination

## Quick Security Checklist

For every recommendation:
- [ ] Data classification considered
- [ ] Access controls defined
- [ ] No hardcoded secrets
- [ ] Input validation mentioned
- [ ] Encryption requirements noted
- [ ] Uptime impact assessed
- [ ] Failure modes identified
- [ ] Security review recommended if needed

## Uptime Impact Assessment

For every change:
- [ ] Single points of failure identified
- [ ] Redundancy plan documented
- [ ] Rollback strategy defined
- [ ] Monitoring approach specified
- [ ] Impact on SLAs calculated

## Communication Templates

### Highlighting Security Concerns
```
"This approach requires security review due to:
- Direct database access from client
- Unencrypted data transmission
- Shared credential usage

Recommended: Implement API gateway with proper authentication"
```

### Noting Uptime Impacts
```
"Uptime Considerations:
- Current design has single point of failure at [component]
- Estimated impact: 99.9% availability (8.76 hours/year downtime)
- Recommendation: Add redundancy to achieve 99.99% target"
```

## Escalation

### When to Escalate
- Unclear security requirements
- Potential data breach scenarios
- Uptime requirements not achievable
- Compliance concerns
- Novel security challenges

### How to Escalate
1. Document the concern clearly
2. Provide impact assessment
3. Suggest alternatives
4. Recommend expert review
5. Track resolution

---

**Remember**: Security and uptime are not optional features - they are fundamental requirements for every UDX solution. When in doubt, choose the more secure option and document the decision.