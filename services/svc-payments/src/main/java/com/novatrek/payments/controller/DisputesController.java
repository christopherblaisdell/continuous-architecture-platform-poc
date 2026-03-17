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
@RequestMapping("/disputes")
public class DisputesController {

    private final DisputeRepository disputeRepository;

    public DisputesController(DisputeRepository disputeRepository) {
        this.disputeRepository = disputeRepository;
    }

    @GetMapping
    public List<Dispute> listDisputes() {
        return disputeRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Dispute> createDispute(@Valid @RequestBody Dispute body) {
        Dispute saved = disputeRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{disputeId}")
    public Dispute getDispute(@PathVariable UUID disputeId) {
        return disputeRepository.findById(disputeId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Dispute not found"));
    }

    @PatchMapping("/{disputeId}")
    public Dispute updateDispute(@PathVariable UUID disputeId, @Valid @RequestBody Dispute body) {
        Dispute existing = disputeRepository.findById(disputeId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Dispute not found"));

        if (body.getPaymentId() != null) existing.setPaymentId(body.getPaymentId());
        if (body.getReservationId() != null) existing.setReservationId(body.getReservationId());
        if (body.getGuestId() != null) existing.setGuestId(body.getGuestId());
        if (body.getType() != null) existing.setType(body.getType());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());
        if (body.getTier() != null) existing.setTier(body.getTier());
        if (body.getAmountRequested() != null) existing.setAmountRequested(body.getAmountRequested());
        if (body.getAmountApproved() != null) existing.setAmountApproved(body.getAmountApproved());
        if (body.getResolution() != null) existing.setResolution(body.getResolution());
        if (body.getJustification() != null) existing.setJustification(body.getJustification());
        if (body.getAssignedTo() != null) existing.setAssignedTo(body.getAssignedTo());
        if (body.getRev() != null) existing.setRev(body.getRev());

        return disputeRepository.save(existing);
    }

    @PostMapping("/{disputeId}/resolve")
    public Dispute resolveDispute(@PathVariable UUID disputeId, @Valid @RequestBody Dispute body) {
        Dispute existing = disputeRepository.findById(disputeId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Dispute not found"));
        return disputeRepository.save(existing);
    }

}
