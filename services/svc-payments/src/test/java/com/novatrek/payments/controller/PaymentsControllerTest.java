package com.novatrek.payments.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.payments.entity.Dispute;
import com.novatrek.payments.entity.Payment;
import com.novatrek.payments.repository.DisputeRepository;
import com.novatrek.payments.repository.PaymentRepository;
import com.novatrek.payments.repository.RefundRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest
class PaymentsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private PaymentRepository paymentRepository;

    @MockBean
    private DisputeRepository disputeRepository;

    @MockBean
    private RefundRepository refundRepository;

    // --- PaymentsController ---

    @Test
    void processPayment_returns201() throws Exception {
        Payment p = new Payment();
        p.setReservationId(UUID.randomUUID());
        p.setGuestId(UUID.randomUUID());
        p.setAmount(new BigDecimal("149.99"));
        p.setCurrency("USD");
        p.setMethod(Payment.PaymentMethod.CREDIT_CARD);
        p.setStatus(Payment.PaymentStatus.PENDING);

        when(paymentRepository.save(any(Payment.class))).thenReturn(p);

        mockMvc.perform(post("/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(p)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.method", is("CREDIT_CARD")));
    }

    @Test
    void getPayment_returns200() throws Exception {
        UUID id = UUID.randomUUID();
        Payment p = new Payment();
        p.setId(id);
        p.setAmount(new BigDecimal("99.00"));
        p.setStatus(Payment.PaymentStatus.CAPTURED);

        when(paymentRepository.findById(id)).thenReturn(Optional.of(p));

        mockMvc.perform(get("/payments/{paymentId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("CAPTURED")));
    }

    @Test
    void getPayment_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(paymentRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/payments/{paymentId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void getDailySummary_returnsList() throws Exception {
        when(paymentRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/payments/daily-summary"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    // --- DisputesController ---

    @Test
    void listDisputes_returnsEmptyList() throws Exception {
        when(disputeRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/disputes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void createDispute_returns201() throws Exception {
        Dispute d = new Dispute();
        d.setPaymentId(UUID.randomUUID());
        d.setGuestId(UUID.randomUUID());
        d.setType(Dispute.DisputeType.CANCELLATION);
        d.setStatus(Dispute.DisputeStatus.OPENED);
        d.setTier(Dispute.DisputeTier.AUTO);
        d.setAmountRequested(new BigDecimal("50.00"));

        when(disputeRepository.save(any(Dispute.class))).thenReturn(d);

        mockMvc.perform(post("/disputes")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(d)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.type", is("CANCELLATION")));
    }

    @Test
    void getDispute_returns200() throws Exception {
        UUID id = UUID.randomUUID();
        Dispute d = new Dispute();
        d.setId(id);
        d.setStatus(Dispute.DisputeStatus.UNDER_REVIEW);

        when(disputeRepository.findById(id)).thenReturn(Optional.of(d));

        mockMvc.perform(get("/disputes/{disputeId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("UNDER_REVIEW")));
    }

    @Test
    void getDispute_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(disputeRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/disputes/{disputeId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateDispute_patchFields() throws Exception {
        UUID id = UUID.randomUUID();
        Dispute existing = new Dispute();
        existing.setId(id);
        existing.setStatus(Dispute.DisputeStatus.OPENED);
        existing.setTier(Dispute.DisputeTier.AUTO);

        Dispute updated = new Dispute();
        updated.setId(id);
        updated.setStatus(Dispute.DisputeStatus.ESCALATED);
        updated.setTier(Dispute.DisputeTier.MANAGER);

        when(disputeRepository.findById(id)).thenReturn(Optional.of(existing));
        when(disputeRepository.save(any(Dispute.class))).thenReturn(updated);

        Dispute patch = new Dispute();
        patch.setStatus(Dispute.DisputeStatus.ESCALATED);
        patch.setTier(Dispute.DisputeTier.MANAGER);

        mockMvc.perform(patch("/disputes/{disputeId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(patch)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("ESCALATED")));
    }

    // --- ChargebacksController ---

    @Test
    void ingestChargeback_returns201() throws Exception {
        Dispute d = new Dispute();
        d.setType(Dispute.DisputeType.CHARGEBACK);
        d.setStatus(Dispute.DisputeStatus.OPENED);

        when(disputeRepository.save(any(Dispute.class))).thenReturn(d);

        mockMvc.perform(post("/chargebacks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(d)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.type", is("CHARGEBACK")));
    }

    // --- GuestsController ---

    @Test
    void getGuestPaymentHistory_returns200() throws Exception {
        UUID guestId = UUID.randomUUID();
        Dispute d = new Dispute();
        d.setId(guestId);
        d.setGuestId(guestId);

        when(disputeRepository.findById(guestId)).thenReturn(Optional.of(d));

        mockMvc.perform(get("/guests/{guestId}/payment-history", guestId))
                .andExpect(status().isOk());
    }

    @Test
    void getGuestPaymentHistory_returns404() throws Exception {
        UUID guestId = UUID.randomUUID();
        when(disputeRepository.findById(guestId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/guests/{guestId}/payment-history", guestId))
                .andExpect(status().isNotFound());
    }
}
