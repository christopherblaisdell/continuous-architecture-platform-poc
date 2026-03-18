package com.novatrek.loyaltyrewards.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.loyaltyrewards.entity.LoyaltyMember;
import com.novatrek.loyaltyrewards.repository.LoyaltyMemberRepository;
import com.novatrek.loyaltyrewards.repository.TransactionRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({MembersController.class, TiersController.class})
class LoyaltyRewardsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private LoyaltyMemberRepository loyaltyMemberRepository;

    @MockBean
    private TransactionRepository transactionRepository;

    @Test
    void getMemberBalance_found() throws Exception {
        UUID guestId = UUID.randomUUID();
        LoyaltyMember m = new LoyaltyMember();
        m.setGuestId(guestId);
        m.setTier(LoyaltyMember.TierName.PATHFINDER);
        m.setPointsBalance(5000);
        m.setLifetimePoints(12000);

        when(loyaltyMemberRepository.findById(guestId)).thenReturn(Optional.of(m));

        mockMvc.perform(get("/members/{guestId}/balance", guestId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.pointsBalance", is(5000)))
                .andExpect(jsonPath("$.tier", is("PATHFINDER")));
    }

    @Test
    void getMemberBalance_notFound() throws Exception {
        UUID guestId = UUID.randomUUID();
        when(loyaltyMemberRepository.findById(guestId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/members/{guestId}/balance", guestId))
                .andExpect(status().isNotFound());
    }

    @Test
    void earnPoints_returns201() throws Exception {
        UUID guestId = UUID.randomUUID();
        LoyaltyMember m = new LoyaltyMember();
        m.setGuestId(guestId);
        m.setTier(LoyaltyMember.TierName.EXPLORER);
        m.setPointsBalance(1500);
        m.setLifetimePoints(1500);

        when(loyaltyMemberRepository.findById(guestId)).thenReturn(Optional.of(m));
        when(loyaltyMemberRepository.save(any(LoyaltyMember.class))).thenReturn(m);

        mockMvc.perform(post("/members/{guestId}/earn", guestId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(m)))
                .andExpect(status().isCreated());
    }

    @Test
    void redeemPoints_returns201() throws Exception {
        UUID guestId = UUID.randomUUID();
        LoyaltyMember m = new LoyaltyMember();
        m.setGuestId(guestId);
        m.setTier(LoyaltyMember.TierName.SUMMIT);
        m.setPointsBalance(8000);
        m.setLifetimePoints(25000);

        when(loyaltyMemberRepository.findById(guestId)).thenReturn(Optional.of(m));
        when(loyaltyMemberRepository.save(any(LoyaltyMember.class))).thenReturn(m);

        mockMvc.perform(post("/members/{guestId}/redeem", guestId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(m)))
                .andExpect(status().isCreated());
    }

    @Test
    void getMemberTransactions_found() throws Exception {
        UUID guestId = UUID.randomUUID();
        LoyaltyMember m = new LoyaltyMember();
        m.setGuestId(guestId);
        m.setTier(LoyaltyMember.TierName.LEGEND);
        m.setPointsBalance(50000);
        m.setLifetimePoints(100000);

        when(loyaltyMemberRepository.findById(guestId)).thenReturn(Optional.of(m));

        mockMvc.perform(get("/members/{guestId}/transactions", guestId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tier", is("LEGEND")));
    }

    @Test
    void getMemberTransactions_notFound() throws Exception {
        UUID guestId = UUID.randomUUID();
        when(loyaltyMemberRepository.findById(guestId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/members/{guestId}/transactions", guestId))
                .andExpect(status().isNotFound());
    }

    @Test
    void listTiers_returnsList() throws Exception {
        when(loyaltyMemberRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/tiers"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }
}
