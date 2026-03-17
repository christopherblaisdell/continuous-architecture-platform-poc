# Example BDD feature file — Guest Check-In
# This demonstrates the Gherkin format used for acceptance testing
# in NovaTrek services. Each feature file maps to one or more
# user story acceptance criteria from solution designs.
#
# See: ADR-012 (TDD/BDD hybrid), config/test-standards.yaml

Feature: Guest Check-In
  As a guest arriving for an adventure
  I want to check in with my reservation
  So that the operations team can prepare for my arrival

  Background:
    Given a guest "Alex Rivera" with guest ID "guest-001"
    And a confirmed reservation "res-5001" for trip "trip-100"

  Scenario: Successful check-in with valid reservation
    Given the reservation "res-5001" has status "confirmed"
    And the guest has an active waiver for the adventure category
    When the guest checks in with reservation "res-5001"
    Then the check-in is created successfully
    And the check-in status is "checked_in"
    And a check-in confirmation notification is sent

  Scenario: Check-in rejected for cancelled reservation
    Given the reservation "res-5001" has status "cancelled"
    When the guest checks in with reservation "res-5001"
    Then the check-in is rejected
    And the error message contains "reservation is not confirmed"

  Scenario: Check-in requires waiver for high-risk adventure
    Given the trip "trip-100" has adventure category "rock_climbing"
    And the guest does not have an active waiver
    When the guest checks in with reservation "res-5001"
    Then the check-in is rejected
    And the error message contains "active waiver required"

  Scenario: Unknown adventure category defaults to Pattern 3
    Given the trip "trip-100" has adventure category "unknown_activity"
    When the system determines the check-in pattern
    Then the check-in pattern is "Pattern 3 (Full Service)"
