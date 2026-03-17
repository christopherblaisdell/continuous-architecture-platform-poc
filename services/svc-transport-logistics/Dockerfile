# ===========================================================================
# NovaTrek Microservice — Multi-stage Dockerfile
# ===========================================================================
# Stage 1: Build with JDK 21
# Stage 2: Run with distroless JRE (minimal attack surface)
# ===========================================================================

# --- Build Stage ---
FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /app
COPY build.gradle.kts settings.gradle.kts gradlew ./
COPY gradle/ gradle/
RUN ./gradlew dependencies --no-daemon || true
COPY src/ src/
RUN ./gradlew bootJar --no-daemon -x test

# --- Runtime Stage ---
FROM gcr.io/distroless/java21-debian12:nonroot
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", \
  "-XX:+UseG1GC", \
  "-XX:MaxRAMPercentage=75.0", \
  "-Djava.security.egd=file:/dev/./urandom", \
  "-jar", "app.jar"]
