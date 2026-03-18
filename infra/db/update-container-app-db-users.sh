#!/usr/bin/env bash
# =============================================================================
# Update Container Apps — Switch to Per-Service Database Users
# =============================================================================
# Updates each container app's SPRING_DATASOURCE_USERNAME and PASSWORD
# to use the schema-isolated service user instead of novatrekadmin.
#
# Usage: bash infra/db/update-container-app-db-users.sh
# =============================================================================
set -euo pipefail

RG="rg-novatrek-dev"

declare -A SERVICE_SCHEMAS=(
    [ca-svc-analytics]="svc_analytics"
    [ca-svc-check-in]="svc_check_in"
    [ca-svc-emergency-response]="svc_emergency_response"
    [ca-svc-gear-inventory]="svc_gear_inventory"
    [ca-svc-guest-profiles]="svc_guest_profiles"
    [ca-svc-guide-management]="svc_guide_management"
    [ca-svc-inventory-procurement]="svc_inventory_procurement"
    [ca-svc-location-services]="svc_location_services"
    [ca-svc-loyalty-rewards]="svc_loyalty_rewards"
    [ca-svc-media-gallery]="svc_media_gallery"
    [ca-svc-notifications]="svc_notifications"
    [ca-svc-partner-integrations]="svc_partner_integrations"
    [ca-svc-payments]="svc_payments"
    [ca-svc-reservations]="svc_reservations"
    [ca-svc-reviews]="svc_reviews"
    [ca-svc-safety-compliance]="svc_safety_compliance"
    [ca-svc-scheduling-orchestrator]="svc_scheduling_orchestrator"
    [ca-svc-trail-management]="svc_trail_management"
    [ca-svc-transport-logistics]="svc_transport_logistics"
    [ca-svc-trip-catalog]="svc_trip_catalog"
    [ca-svc-weather]="svc_weather"
    [ca-svc-wildlife-tracking]="svc_wildlife_tracking"
)

echo "Updating container app database credentials..."
echo "================================================"

for APP in "${!SERVICE_SCHEMAS[@]}"; do
    USER="${SERVICE_SCHEMAS[$APP]}"
    PASS="${USER}_2026x"
    echo ""
    echo "→ ${APP}: user=${USER}"
    az containerapp update \
        --name "$APP" \
        --resource-group "$RG" \
        --set-env-vars \
            "SPRING_DATASOURCE_USERNAME=${USER}" \
            "SPRING_DATASOURCE_PASSWORD=${PASS}" \
        --query '{name:name,provisioningState:properties.provisioningState}' \
        -o json \
    || echo "  ✗ Failed to update ${APP}"
done

echo ""
echo "================================================"
echo "All container apps updated with per-service DB users."
echo ""
echo "NOTE: Flyway migrations still run as novatrekadmin."
echo "Services use schema-isolated users for runtime queries only."
