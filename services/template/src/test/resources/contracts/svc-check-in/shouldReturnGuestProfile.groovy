// Example Spring Cloud Contract — Provider: svc-guest-profiles
// This contract defines the expected behavior of GET /guests/{guest_id}
// when called by consumer services (svc-check-in, svc-reservations, etc.).
//
// Place contracts in src/test/resources/contracts/{consumer-name}/
// to organize by consumer. The SCC Gradle plugin auto-generates
// JUnit 5 tests from these contracts at build time.
//
// See: ADR-013, config/test-standards.yaml, cross-service-calls.yaml

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "Should return guest profile when guest exists"
    request {
        method GET()
        urlPath("/guests/guest-001")
        headers {
            accept(applicationJson())
        }
    }
    response {
        status OK()
        headers {
            contentType(applicationJson())
        }
        body([
            guest_id   : "guest-001",
            first_name : "Alex",
            last_name  : "Rivera",
            email      : "alex.rivera@novatrek.example.com",
            phone      : "+1-555-0142",
            emergency_contact: [
                name : "Jordan Rivera",
                phone: "+1-555-0143"
            ]
        ])
    }
}
