package com.novatrek.trips.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.UUID;

@Entity
@Table(name = "trips")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Trip {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotBlank
    private String name;

    @Column(columnDefinition = "TEXT")
    private String description;

    @NotBlank
    private String adventureCategory;

    @NotNull
    @Enumerated(EnumType.STRING)
    private Difficulty difficulty;

    @Positive
    private int durationMinutes;

    @Positive
    private int maxParticipants;

    @NotNull
    @Positive
    private BigDecimal basePrice;

    @Builder.Default
    private String currency = "USD";

    private UUID locationId;

    private UUID trailId;

    private boolean guideRequired;

    private int minimumAge;

    private boolean equipmentProvided;

    private String seasonAvailability;

    @Builder.Default
    private boolean active = true;

    public enum Difficulty {
        BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    }
}
