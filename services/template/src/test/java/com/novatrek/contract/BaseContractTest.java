package com.novatrek.contract;

import io.restassured.module.mockmvc.RestAssuredMockMvc;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.web.context.WebApplicationContext;

/**
 * Base class for Spring Cloud Contract auto-generated verifier tests.
 *
 * Each service that acts as a provider should extend this class (or create
 * a service-specific base class) and configure the application context
 * needed to verify its contracts.
 *
 * Contracts live in src/test/resources/contracts/ as Groovy DSL or YAML files.
 * The Spring Cloud Contract Gradle plugin generates JUnit 5 tests from these
 * contracts at build time, using this class as the base.
 *
 * See ADR-013 for the contract testing tool selection rationale.
 * See config/test-standards.yaml for the contract testing standards.
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
public abstract class BaseContractTest {

    @Autowired
    private WebApplicationContext context;

    @BeforeEach
    void setup() {
        RestAssuredMockMvc.webAppContextSetup(context);
    }
}
