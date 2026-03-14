plugins {
    java
    id("org.springframework.boot") version "3.3.5"
    id("io.spring.dependency-management") version "1.1.6"
    id("jacoco")
    id("info.solidsoft.pitest") version "1.15.0"
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
        mavenBom("com.azure.spring:spring-cloud-azure-dependencies:5.18.0")
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-validation")

    implementation("org.flywaydb:flyway-core")
    implementation("org.flywaydb:flyway-database-postgresql")
    runtimeOnly("org.postgresql:postgresql")

    implementation("com.azure.spring:spring-cloud-azure-starter-keyvault-secrets")

    implementation("io.micrometer:micrometer-tracing-bridge-otel")
    implementation("io.opentelemetry:opentelemetry-exporter-otlp")
    runtimeOnly("io.micrometer:micrometer-registry-otlp")
    implementation("net.logstash.logback:logstash-logback-encoder:8.0")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:postgresql:1.20.3")
    testImplementation("org.testcontainers:junit-jupiter:1.20.3")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    // --- Contract Testing (Spring Cloud Contract) ---
    testImplementation("org.springframework.cloud:spring-cloud-starter-contract-verifier")

    // --- BDD Acceptance Testing (Cucumber-JVM) ---
    testImplementation("io.cucumber:cucumber-java:7.18.0")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:7.18.0")
    testImplementation("io.cucumber:cucumber-spring:7.18.0")
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

// ---------------------------------------------------------------------------
// JaCoCo Coverage Enforcement (ADR-012 — thresholds from config/test-standards.yaml)
// Line:   80% minimum (blocking)
// Branch: 70% minimum (blocking)
// ---------------------------------------------------------------------------
tasks.jacocoTestCoverageVerification {
    dependsOn(tasks.jacocoTestReport)
    violationRules {
        rule {
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = "0.80".toBigDecimal()
            }
        }
        rule {
            limit {
                counter = "BRANCH"
                value = "COVEREDRATIO"
                minimum = "0.70".toBigDecimal()
            }
        }
    }
}

tasks.named("check") {
    dependsOn(tasks.jacocoTestCoverageVerification)
}

// ---------------------------------------------------------------------------
// PITest Mutation Testing (ADR-012 — advisory in Phase A, blocking in Phase D)
// ---------------------------------------------------------------------------
pitest {
    junit5PluginVersion.set("1.2.1")
    targetClasses.set(listOf("com.novatrek.*"))
    excludedClasses.set(listOf(
        "com.novatrek.*.config.*",
        "com.novatrek.*.dto.*",
        "com.novatrek.*.entity.*"
    ))
    mutators.set(listOf("DEFAULTS"))
    outputFormats.set(listOf("HTML"))
    mutationThreshold.set(0)         // Phase A: advisory only — set to 60 in Phase D
    withHistory.set(true)
    timestampedReports.set(false)
}
