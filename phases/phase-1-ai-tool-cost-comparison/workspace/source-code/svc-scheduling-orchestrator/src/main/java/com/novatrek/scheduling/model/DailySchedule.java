package com.novatrek.scheduling.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.UUID;

@Entity
@Table(name = "daily_schedules")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DailySchedule {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotNull
    private LocalDate scheduleDate;

    @NotNull
    private UUID locationId;

    private UUID guideId;

    private UUID tripId;

    @NotNull
    private LocalTime startTime;

    @NotNull
    private LocalTime endTime;

    // GETS OVERWRITTEN by NTK-10004 bug - guide-management enriches this field
    @Column(columnDefinition = "TEXT")
    private String guideNotes;

    // GETS OVERWRITTEN by NTK-10004 bug - guide-management enriches this field
    @Column(columnDefinition = "TEXT")
    private String guidePreferences;

    private int participantCount;

    private int maxCapacity;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Builder.Default
    private ScheduleStatus status = ScheduleStatus.DRAFT;

    private LocalDateTime generatedAt;

    private LocalDateTime lastModifiedAt;

    private String lastModifiedBy;

    public enum ScheduleStatus {
        DRAFT, PUBLISHED, IN_PROGRESS, COMPLETED, CANCELLED
    }

    @PrePersist
    protected void onCreate() {
        generatedAt = LocalDateTime.now();
        lastModifiedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        lastModifiedAt = LocalDateTime.now();
    }
}
