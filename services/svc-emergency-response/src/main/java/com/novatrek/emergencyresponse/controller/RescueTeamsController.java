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
@RequestMapping("/rescue-teams")
public class RescueTeamsController {

    private final DispatchRecordRepository dispatchRecordRepository;

    public RescueTeamsController(DispatchRecordRepository dispatchRecordRepository) {
        this.dispatchRecordRepository = dispatchRecordRepository;
    }

    @GetMapping
    public List<DispatchRecord> listRescueTeams() {
        return dispatchRecordRepository.findAll();
    }

}
