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
@RequestMapping("/refund-policy")
public class RefundPolicyController {

    private final DisputeRepository disputeRepository;

    public RefundPolicyController(DisputeRepository disputeRepository) {
        this.disputeRepository = disputeRepository;
    }

    @PostMapping("/evaluate")
    public Dispute evaluateRefundPolicy() {
        throw new UnsupportedOperationException("Not yet implemented");
    }

}
