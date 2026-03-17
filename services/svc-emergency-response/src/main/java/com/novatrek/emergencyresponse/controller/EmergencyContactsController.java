package com.novatrek.emergencyresponse.controller;

import com.novatrek.emergencyresponse.entity.DispatchRecord;
import com.novatrek.emergencyresponse.repository.DispatchRecordRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/emergency-contacts")
public class EmergencyContactsController {

    private final DispatchRecordRepository dispatchRecordRepository;

    public EmergencyContactsController(DispatchRecordRepository dispatchRecordRepository) {
        this.dispatchRecordRepository = dispatchRecordRepository;
    }

    @GetMapping("/{guestId}")
    public DispatchRecord getGuestEmergencyContacts(@PathVariable UUID guestId) {
        return dispatchRecordRepository.findById(guestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "DispatchRecord not found"));
    }

    @PutMapping("/{guestId}")
    public DispatchRecord updateGuestEmergencyContacts(@PathVariable UUID guestId, @Valid @RequestBody DispatchRecord body) {
        DispatchRecord existing = dispatchRecordRepository.findById(guestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "DispatchRecord not found"));
        return dispatchRecordRepository.save(existing);
    }

}
