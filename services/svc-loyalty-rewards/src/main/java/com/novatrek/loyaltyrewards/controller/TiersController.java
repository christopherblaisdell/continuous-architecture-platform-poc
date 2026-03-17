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
@RequestMapping("/tiers")
public class TiersController {

    private final LoyaltyMemberRepository loyaltyMemberRepository;

    public TiersController(LoyaltyMemberRepository loyaltyMemberRepository) {
        this.loyaltyMemberRepository = loyaltyMemberRepository;
    }

    @GetMapping
    public List<LoyaltyMember> listTiers() {
        return loyaltyMemberRepository.findAll();
    }

}
