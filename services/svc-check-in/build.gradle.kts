plugins {
    java
    id("org.springframework.boot") version "3.3.5"
    id("io.spring.dependency-management") version "1.1.6"
    id("org.owasp.dependencycheck") version "10.0.3"
    id("jacoco")
    id("info.solidsoft.pitest") version "1.15.0"
    id("org.springframework.cloud.contract") version "4.1.4"
    id("org.sonarqube") version "5.1.0.4882"
}

group = "com.novatrek"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencyManagement {
    imports {
        // Spring Cloud Azure BOM — aligns all Azure SDK versions
        mavenBom("com.azure.spring:spring-cloud-azure-dependencies:5.18.0")
        // Spring Cloud BOM — aligns Spring Cloud Contract and related modules
        mavenBom("org.springframework.cloud:spring-cloud-dependencies:2023.0.4")
    }
}

dependencies {
    // --- Spring Boot Core ---
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-validation")

    // --- Database ---
    implementation("org.flywaydb:flyway-core")
    implementation("org.flywaydb:flyway-database-postgresql")
    runtimeOnly("org.postgresql:postgresql")

    // --- Azure Integration ---
    implementation("com.azure.spring:spring-cloud-azure-starter-keyvault-secrets")
    implementation("com.azure.spring:spring-cloud-azure-starter-servicebus")

    // --- Observability ---
    implementation("io.micrometer:micrometer-tracing-bridge-otel")
    implementation("io.opentelemetry:opentelemetry-exporter-otlp")
    runtimeOnly("io.micrometer:micrometer-registry-otlp")

    // --- Structured Logging ---
    implementation("net.logstash.logback:logstash-logback-encoder:8.0")

    // --- Resilience ---
    implementation("io.github.resilience4j:resilience4j-spring-boot3:2.2.0")

    // --- Testing ---
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testRuntimeOnly("com.h2database:h2")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    // --- BDD (Cucumber) ---
    testImplementation("io.cucumber:cucumber-java:7.20.1")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:7.20.1")
    testImplementation("io.cucumber:cucumber-spring:7.20.1")

    // --- Contract Testing (Spring Cloud Contract) ---
    testImplementation("org.springframework.cloud:spring-cloud-starter-contract-verifier")
    testImplementation("org.springframework.cloud:spring-cloud-starter-contract-stub-runner")
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required = true
        html.required = true
    }
}

tasks.jacocoTestCoverageVerification {
    dependsOn(tasks.jacocoTestReport)
    violationRules {
        rule {
            limit {
                counter = "LINE"
                minimum = "0.80".toBigDecimal()
            }
            limit {
                counter = "BRANCH"
                minimum = "0.70".toBigDecimal()
            }
        }
    }
}

tasks.check {
    dependsOn(tasks.jacocoTestCoverageVerification)
}

// PITest mutation testing — advisory in Phase A, promoted to gate in Phase D
pitest {
    junit5PluginVersion = "1.2.1"
    targetClasses = listOf("com.novatrek.*")
    mutationThreshold = 0  // advisory — set to 60 when promoted to gate
    outputFormats = listOf("HTML", "XML")
    timestampedReports = false
}

// Spring Cloud Contract — provider-side contract verification (ADR-013)
contracts {
    testFramework = org.springframework.cloud.contract.verifier.config.TestFramework.JUNIT5
    baseClassForTests = "com.novatrek.contract.BaseContractTest"
    contractsDslDir = file("src/test/resources/contracts")
    failOnNoContracts = false
}

// OWASP Dependency Check — fail on CRITICAL/HIGH CVEs
dependencyCheck {
    failBuildOnCVSS = 7.0f
    formats = listOf("HTML", "JSON")
}

