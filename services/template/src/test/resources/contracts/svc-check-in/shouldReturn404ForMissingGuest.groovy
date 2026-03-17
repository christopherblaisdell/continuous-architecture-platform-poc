// Example Spring Cloud Contract — Provider: svc-guest-profiles
// Contract for 404 response when guest does not exist.

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "Should return 404 when guest does not exist"
    request {
        method GET()
        urlPath("/guests/guest-nonexistent")
        headers {
            accept(applicationJson())
        }
    }
    response {
        status NOT_FOUND()
        headers {
            contentType(applicationJson())
        }
        body([
            error  : "NOT_FOUND",
            message: "Guest not found: guest-nonexistent"
        ])
    }
}
