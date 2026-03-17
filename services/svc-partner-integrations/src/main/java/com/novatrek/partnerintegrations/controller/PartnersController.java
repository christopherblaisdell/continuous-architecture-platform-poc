package com.novatrek.partnerintegrations.controller;

import com.novatrek.partnerintegrations.entity.Partner;
import com.novatrek.partnerintegrations.repository.PartnerRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/partners")
public class PartnersController {

    private final PartnerRepository partnerRepository;

    public PartnersController(PartnerRepository partnerRepository) {
        this.partnerRepository = partnerRepository;
    }

    @GetMapping
    public List<Partner> listPartners() {
        return partnerRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Partner> registerPartner(@Valid @RequestBody Partner body) {
        Partner saved = partnerRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{partnerId}/commission-report")
    public Partner getCommissionReport(@PathVariable UUID partnerId) {
        return partnerRepository.findById(partnerId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Partner not found"));
    }

}
