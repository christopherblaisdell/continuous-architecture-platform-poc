# Swagger/YAML Locations for UDX Microservices

## Primary Location for UDX Microservices

### Official Corporate Repository
**Location**: `external-repos/architecture/udx-architecture-artifacts/services/`

This directory contains all the Swagger/OpenAPI YAML specifications for UDX microservices:
- All `ms-*` microservice API definitions
- Service contracts and schemas
- Request/response models
- API versioning information

### Directory Structure
```
external-repos/
└── architecture/
    └── udx-architecture-artifacts/
        └── services/
            ├── ms-acp/
            │   └── [service YAML files]
            ├── ms-biometrics/
            │   └── [service YAML files]
            ├── ms-checkout/
            │   └── [service YAML files]
            ├── ms-guest/
            │   └── [service YAML files]
            ├── ms-guest-entitlements/
            │   └── [service YAML files]
            ├── ms-hotel-stays/
            │   └── [service YAML files]
            ├── ms-hotels/
            │   └── [service YAML files]
            ├── ms-ohip-reservations/
            │   └── [service YAML files]
            ├── ms-orders/
            │   └── [service YAML files]
            ├── ms-presence/
            │   └── [service YAML files]
            └── [other microservices]/
                └── [service YAML files]
```

## Important Notes

1. **Always check this location first** when looking for existing service definitions
2. **Do not create duplicate Swagger files** - use the ones in this repository
3. **Maintain consistency** with existing patterns found in these files
4. **Version updates** should be done in this location

## Legacy/Alternative Locations

While the primary location is as above, these locations may still be referenced in older documentation:
- `/1-upr-services/swagger/[service-name]/[service-name].yaml`
- `/1-upr-services/services/[service-name]/`

However, the authoritative source is now `external-repos/architecture/udx-architecture-artifacts/services/`.

## Usage in Solution Architecture

When designing new services or modifying existing ones:
1. First check `external-repos/architecture/udx-architecture-artifacts/services/[service-name]/` for existing definitions
2. Reuse schemas and models where possible
3. Follow the patterns established in existing services
4. Update version numbers appropriately when making changes
5. Document all changes in release notes

## Accessing the Files

To access these files:
1. Ensure the `udx-architecture-artifacts` repository is cloned locally
2. Navigate to `external-repos/architecture/udx-architecture-artifacts/services/`
3. Look for the specific microservice directory
4. Review the YAML files for API specifications

## Integration with Roo

This location is now formalized in the Solution Architect mode customizations, ensuring that:
- Roo will always know where to look for microservice API specifications
- Consistency is maintained across all architectural work
- No duplicate or conflicting Swagger definitions are created
- All architects reference the same authoritative source