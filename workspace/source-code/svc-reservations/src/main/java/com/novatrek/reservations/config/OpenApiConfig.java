package com.novatrek.reservations.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "NovaTrek Reservations API",
                version = "1.0.0",
                description = "Core booking and reservation service for NovaTrek Adventures. "
                        + "Manages trip reservations for hiking, kayaking, climbing, and camping experiences.",
                contact = @Contact(
                        name = "NovaTrek Platform Team",
                        email = "platform@novatrek.com"
                )
        )
)
public class OpenApiConfig {
}
