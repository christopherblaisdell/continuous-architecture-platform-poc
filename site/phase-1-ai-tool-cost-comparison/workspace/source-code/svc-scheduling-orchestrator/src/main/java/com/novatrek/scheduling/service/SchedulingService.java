package com.novatrek.scheduling.service;

import com.novatrek.scheduling.model.DailySchedule;
import com.novatrek.scheduling.repository.ScheduleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class SchedulingService {

    private final ScheduleRepository scheduleRepository;

    public List<DailySchedule> getSchedules(LocalDate date, UUID locationId) {
        if (date != null && locationId != null) {
            return scheduleRepository.findByScheduleDateAndLocationId(date, locationId);
        }
        return scheduleRepository.findAll();
    }

    public DailySchedule getSchedule(UUID id) {
        return scheduleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Schedule not found: " + id));
    }

    @Transactional
    public List<DailySchedule> generateDailySchedule(LocalDate date, UUID locationId) {
        log.info("Generating daily schedule for date={} locationId={}", date, locationId);
        // In production, this would query trip-catalog and guide-management
        // to auto-generate schedule slots based on available guides and trips
        DailySchedule schedule = DailySchedule.builder()
                .scheduleDate(date)
                .locationId(locationId)
                .status(DailySchedule.ScheduleStatus.DRAFT)
                .build();
        return List.of(scheduleRepository.save(schedule));
    }

    // BUG: NTK-10004 - This PUT replaces the entire entity, overwriting guide enrichments
    // (guideNotes, guidePreferences) that were set by svc-guide-management.
    // Should use PATCH semantics or selective field updates instead.
    // Root cause: No data ownership boundary - orchestrator owns scheduling fields,
    // but guide-management owns enrichment fields on the same entity.
    @Transactional
    public DailySchedule updateSchedule(UUID id, DailySchedule incoming) {
        if (!scheduleRepository.existsById(id)) {
            throw new RuntimeException("Schedule not found: " + id);
        }
        // Full entity replacement - this is the bug!
        // The incoming entity from API clients does NOT include guideNotes/guidePreferences
        // that were enriched by svc-guide-management, so they get set to null.
        incoming.setId(id);
        incoming.setLastModifiedAt(LocalDateTime.now());
        incoming.setLastModifiedBy("scheduling-orchestrator");
        return scheduleRepository.save(incoming);
    }
}
