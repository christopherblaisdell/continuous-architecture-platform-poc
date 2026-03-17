package com.novatrek.loyaltyrewards.controller;

import com.novatrek.loyaltyrewards.entity.LoyaltyMember;
import com.novatrek.loyaltyrewards.repository.LoyaltyMemberRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/members")
public class MembersController {

    private final LoyaltyMemberRepository loyaltyMemberRepository;

    public MembersController(LoyaltyMemberRepository loyaltyMemberRepository) {
        this.loyaltyMemberRepository = loyaltyMemberRepository;
    }

    @GetMapping("/{guestId}/balance")
    public LoyaltyMember getMemberBalance(@PathVariable UUID guestId) {
        return loyaltyMemberRepository.findById(guestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "LoyaltyMember not found"));
    }

    @PostMapping("/{guestId}/earn")
    public ResponseEntity<LoyaltyMember> earnPoints(@PathVariable UUID guestId, @Valid @RequestBody LoyaltyMember body) {
        LoyaltyMember saved = loyaltyMemberRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PostMapping("/{guestId}/redeem")
    public ResponseEntity<LoyaltyMember> redeemPoints(@PathVariable UUID guestId, @Valid @RequestBody LoyaltyMember body) {
        LoyaltyMember saved = loyaltyMemberRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{guestId}/transactions")
    public LoyaltyMember getMemberTransactions(@PathVariable UUID guestId) {
        return loyaltyMemberRepository.findById(guestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "LoyaltyMember not found"));
    }

}
