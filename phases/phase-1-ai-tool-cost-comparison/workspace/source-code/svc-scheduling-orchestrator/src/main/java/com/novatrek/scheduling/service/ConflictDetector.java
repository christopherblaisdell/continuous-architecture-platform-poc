package com.novatrek.scheduling.service;

import com.novatrek.scheduling.model.DailySchedule;
import com.novatrek.scheduling.repository.ScheduleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Component
@RequiredArgsConstructor
public class ConflictDetector {

    private final ScheduleRepository scheduleRepository;

    public List<String> detectConflicts(DailySchedule schedule) {
        List<String> conflicts = new ArrayList<>();

        // Detect guide double-bookings on same date/time
        if (schedule.getGuideId() != null) {
            List<DailySchedule> guideSchedules = scheduleRepository
                    .findByGuideIdAndScheduleDate(schedule.getGuideId(), schedule.getScheduleDate());

            for (DailySchedule existing : guideSchedules) {
                if (!existing.getId().equals(schedule.getId()) &&
                        hasTimeOverlap(schedule.getStartTime(), schedule.getEndTime(),
                                existing.getStartTime(), existing.getEndTime())) {
                    conflicts.add(String.format(
                            "Guide %s is double-booked: %s-%s overlaps with %s-%s (schedule %s)",
                            schedule.getGuideId(),
                            schedule.getStartTime(), schedule.getEndTime(),
                            existing.getStartTime(), existing.getEndTime(),
                            existing.getId()));
                }
            }
        }

        // Detect capacity exceeded
        if (schedule.getParticipantCount() > schedule.getMaxCapacity() &&
                schedule.getMaxCapacity() > 0) {
            conflicts.add(String.format(
                    "Capacity exceeded: %d participants exceeds max capacity of %d",
                    schedule.getParticipantCount(), schedule.getMaxCapacity()));
        }

        // Detect overlapping time slots at same location
        List<DailySchedule> conflicting = scheduleRepository
                .findConflictingSchedules(schedule.getScheduleDate(),
                        schedule.getLocationId(),
                        schedule.getStartTime(), schedule.getEndTime());
        for (DailySchedule existing : conflicting) {
            if (!existing.getId().equals(schedule.getId())) {
                conflicts.add(String.format(
                        "Overlapping slot at location %s: %s-%s conflicts with schedule %s",
                        schedule.getLocationId(),
                        existing.getStartTime(), existing.getEndTime(),
                        existing.getId()));
            }
        }

        return conflicts;
    }

    private boolean hasTimeOverlap(LocalTime start1, LocalTime end1,
                                    LocalTime start2, LocalTime end2) {
        return start1.isBefore(end2) && start2.isBefore(end1);
    }
}
