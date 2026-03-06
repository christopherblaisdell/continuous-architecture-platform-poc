package com.novatrek.checkin.controller;

import com.novatrek.checkin.model.CheckInRecord;
import com.novatrek.checkin.service.CheckInService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/check-ins")
@RequiredArgsConstructor
public class CheckInController {

    private final CheckInService checkInService;

    @PostMapping
    public ResponseEntity<CheckInRecord> processCheckIn(@Valid @RequestBody CheckInRecord request) {
        CheckInRecord result = checkInService.processCheckIn(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(result);
    }

    @GetMapping("/{id}")
    public ResponseEntity<CheckInRecord> getCheckIn(@PathVariable UUID id) {
        return checkInService.getCheckIn(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/lookup-reservation")
    public ResponseEntity<CheckInRecord> lookupReservation(
            @RequestBody Map<String, String> lookupRequest) {
        String confirmationCode = lookupRequest.get("confirmationCode");
        String lastName = lookupRequest.get("lastName");
        return checkInService.lookupReservation(confirmationCode, lastName)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/today")
    public ResponseEntity<List<CheckInRecord>> getTodayCheckIns(
            @RequestParam String locationId) {
        List<CheckInRecord> records = checkInService.getTodayCheckIns(locationId);
        return ResponseEntity.ok(records);
    }
}
