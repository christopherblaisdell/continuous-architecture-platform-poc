package com.novatrek.checkin.controller;

import com.novatrek.checkin.entity.CheckIn;
import com.novatrek.checkin.repository.CheckInRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/check-ins")
public class CheckInsController {

    private final CheckInRepository checkInRepository;

    public CheckInsController(CheckInRepository checkInRepository) {
        this.checkInRepository = checkInRepository;
    }

    @GetMapping
    public List<CheckIn> listCheckIns() {
        return checkInRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<CheckIn> createCheckIn(@Valid @RequestBody CheckIn body) {
        CheckIn saved = checkInRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{checkInId}")
    public CheckIn getCheckIn(@PathVariable UUID checkInId) {
        return checkInRepository.findById(checkInId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "CheckIn not found"));
    }

    @PostMapping("/{checkInId}/gear-verification")
    public CheckIn verifyGear(@PathVariable UUID checkInId, @Valid @RequestBody CheckIn body) {
        CheckIn existing = checkInRepository.findById(checkInId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "CheckIn not found"));
        return checkInRepository.save(existing);
    }

    @PostMapping("/{checkInId}/wristband-assignment")
    public CheckIn assignWristband(@PathVariable UUID checkInId, @Valid @RequestBody CheckIn body) {
        CheckIn existing = checkInRepository.findById(checkInId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "CheckIn not found"));
        return checkInRepository.save(existing);
    }

}
