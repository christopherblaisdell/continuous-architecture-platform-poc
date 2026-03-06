#!/usr/bin/env python3
"""Quick test for load_metadata module."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from load_metadata import *

print(f"Domains: {len(DOMAINS)}")
print(f"Services: {len(ALL_SERVICES)}")
print(f"Data stores: {len(DATA_STORES)}")
print(f"Cross-service call keys: {len(CROSS_SERVICE_CALLS)}")
print(f"Events: {len(EVENT_CATALOG)}")
print(f"Consumers: {len(APP_CONSUMERS)}")
print(f"Actors: {len(ACTORS)}")
print(f"Applications: {len(APPLICATIONS)}")
print(f"PCI services: {PCI_SERVICES}")
print(f"PCI flows: {len(PCI_DATA_FLOWS)}")

# Verify tuple format
test_key = ("svc-check-in", "POST", "/check-ins")
test_calls = CROSS_SERVICE_CALLS[test_key]
print(f"Test cross-service call: {test_calls[0]}")
test_ds = DATA_STORES["svc-check-in"]["table_details"]["check_ins"]["columns"][0]
print(f"Test data store column: {test_ds}")
test_evt = EVENT_CATALOG["reservation.created"]["trigger"]
print(f"Test event trigger: {test_evt}")
test_app = APPLICATIONS["web-guest-portal"]["screens"]["Trip Browser"]["steps"][0]
print(f"Test app step: {test_app}")
print("ALL CHECKS PASSED")
