package com.novatrek.contract;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.contract.stubrunner.spring.AutoConfigureStubRunner;
import org.springframework.cloud.contract.stubrunner.spring.StubRunnerProperties;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.ResponseEntity;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Example consumer-side contract test using Spring Cloud Contract Stub Runner.
 *
 * This test demonstrates how a consumer service (e.g., svc-check-in) verifies
 * its integration with a provider (e.g., svc-guest-profiles) using auto-generated
 * WireMock stubs from the provider's contract definitions.
 *
 * In a real service, the stub-runner configuration would reference the provider's
 * published stub JAR artifact. For the template, this uses LOCAL stubs mode.
 *
 * See: ADR-013, config/test-standards.yaml
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureStubRunner(
    ids = "com.novatrek:svc-guest-profiles:+:stubs",
    stubsMode = StubRunnerProperties.StubsMode.LOCAL
)
class ConsumerContractExampleTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldRetrieveGuestProfileFromProvider() {
        // The stub runner starts a WireMock server with the provider's contract stubs.
        // This test verifies that the consumer's HTTP client correctly handles
        // the provider's response format.
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/guests/guest-001", String.class
        );

        assertThat(response.getStatusCode().value()).isEqualTo(200);
        assertThat(response.getBody()).contains("guest-001");
        assertThat(response.getBody()).contains("Alex");
    }

    @Test
    void shouldHandleMissingGuestGracefully() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/guests/guest-nonexistent", String.class
        );

        assertThat(response.getStatusCode().value()).isEqualTo(404);
    }
}
