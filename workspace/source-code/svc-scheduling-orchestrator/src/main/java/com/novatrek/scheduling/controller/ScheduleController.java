package com.novatrek.scheduling.controller;

import com.novatrek.scheduling.model.DailySchedule;
import com.novatrek.scheduling.service.ConflictDetector;
import com.novatrek.scheduling.service.SchedulingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/schedules")
@RequiredArgsConstructor
public class ScheduleController {

    private final SchedulingService schedulingService;
    private final ConflictDetector conflictDetector;

    @GetMapping
    public List<DailySchedule> listSchedules(
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
            @RequestParam(required = false) UUID locationId) {
        return schedulingService.getSchedules(date, locationId);
    }

    @PostMapping("/generate")
    public ResponseEntity<List<DailySchedule>> generateDailySchedule(
            @RequestBody Map<String, Object> request) {
        LocalDate date = LocalDate.parse((String) request.get("date"));
        UUID locationId = UUID.fromString((String) request.get("locationId"));
        List<DailySchedule> generated = schedulingService.generateDailySchedule(date, locationId);
        return ResponseEntity.status(HttpStatus.CREATED).body(generated);
    }

    @PutMapping("/{id}")
    public DailySchedule updateSchedule(@PathVariable UUID id,
                                        @Valid @RequestBody DailySchedule schedule) {
        // THE PROBLEMATIC ENDPOINT - full entity replacement overwrites guide enrichments
        return schedulingService.updateSchedule(id, schedule);
    }

    @GetMapping("/{id}/conflicts")
    public List<String> getConflicts(@PathVariable UUID id) {
        DailySchedule schedule = schedulingService.getSchedule(id);
        return conflictDetector.detectConflicts(schedule);
    }
}
