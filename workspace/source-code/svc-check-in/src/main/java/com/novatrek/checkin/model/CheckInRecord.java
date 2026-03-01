package com.novatrek.checkin.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "check_in_records")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CheckInRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private UUID reservationId;

    @Column(nullable = false)
    private UUID guestId;

    @Column(nullable = false)
    private Instant checkInTime;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private CheckInMethod checkInMethod;

    private String wristbandId;

    @Column(nullable = false)
    private String locationId;

    private String adventureCategory;

    @Enumerated(EnumType.STRING)
    private UiPattern uiPattern;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private CheckInStatus status;

    public enum CheckInMethod {
        KIOSK, STAFF, MOBILE, PARTNER_TABLET
    }

    public enum UiPattern {
        PATTERN_1, PATTERN_2, PATTERN_3
    }

    public enum CheckInStatus {
        PROCESSING, COMPLETED, FAILED
    }
}
