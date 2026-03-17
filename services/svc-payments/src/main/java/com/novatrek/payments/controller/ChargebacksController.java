package com.novatrek.payments.controller;

import com.novatrek.payments.entity.Dispute;
import com.novatrek.payments.repository.DisputeRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/chargebacks")
public class ChargebacksController {

    private final DisputeRepository disputeRepository;

    public ChargebacksController(DisputeRepository disputeRepository) {
        this.disputeRepository = disputeRepository;
    }

    @PostMapping
    public ResponseEntity<Dispute> ingestChargeback(@Valid @RequestBody Dispute body) {
        Dispute saved = disputeRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}
