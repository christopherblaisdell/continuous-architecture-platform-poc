package com.novatrek.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Common step definitions for NovaTrek BDD scenarios.
 *
 * These steps provide reusable Given/When/Then implementations for
 * patterns that appear across multiple feature files — guest identity,
 * reservation lookup, API calls, and response assertions.
 *
 * Service-specific steps should be added in separate step definition
 * classes within the same package (e.g., CheckInSteps, ReservationSteps).
 *
 * See: ADR-012, config/test-standards.yaml
 */
public class CommonSteps {

    private String guestId;
    private String guestName;
    private String reservationId;
    private String tripId;
    private int responseStatus;
    private String responseBody;

    // --- Guest identity steps ---

    @Given("a guest {string} with guest ID {string}")
    public void aGuestWithId(String name, String id) {
        this.guestName = name;
        this.guestId = id;
    }

    // --- Reservation steps ---

    @Given("a confirmed reservation {string} for trip {string}")
    public void aConfirmedReservation(String reservationId, String tripId) {
        this.reservationId = reservationId;
        this.tripId = tripId;
    }

    @Given("the reservation {string} has status {string}")
    public void theReservationHasStatus(String reservationId, String status) {
        // Configure mock/stub to return reservation with given status
        this.reservationId = reservationId;
    }

    // --- Response assertion steps ---

    @Then("the error message contains {string}")
    public void theErrorMessageContains(String expectedMessage) {
        assertThat(responseBody).contains(expectedMessage);
    }

    // --- HTTP response steps ---

    @Then("the response status is {int}")
    public void theResponseStatusIs(int expectedStatus) {
        assertThat(responseStatus).isEqualTo(expectedStatus);
    }
}
