package com.novatrek.partnerintegrations.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.partnerintegrations.entity.Partner;
import com.novatrek.partnerintegrations.entity.PartnerBooking;
import com.novatrek.partnerintegrations.repository.PartnerBookingRepository;
import com.novatrek.partnerintegrations.repository.PartnerRepository;
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

@WebMvcTest({PartnersController.class, PartnerBookingsController.class})
class PartnerIntegrationsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private PartnerRepository partnerRepository;

    @MockBean
    private PartnerBookingRepository partnerBookingRepository;

    @Test
    void listPartners_returnsList() throws Exception {
        Partner p = new Partner();
        p.setName("Alpine Tours GmbH");
        p.setType(Partner.PartnerType.TOUR_OPERATOR);
        p.setCommissionRate(new BigDecimal("12.50"));
        p.setStatus(Partner.PartnerStatus.ACTIVE);

        when(partnerRepository.findAll()).thenReturn(List.of(p));

        mockMvc.perform(get("/partners"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name", is("Alpine Tours GmbH")));
    }

    @Test
    void registerPartner_returns201() throws Exception {
        Partner p = new Partner();
        p.setName("Expedition Corp");
        p.setType(Partner.PartnerType.CORPORATE_ACCOUNT);
        p.setCommissionRate(new BigDecimal("8.00"));
        p.setStatus(Partner.PartnerStatus.PENDING_APPROVAL);

        when(partnerRepository.save(any(Partner.class))).thenReturn(p);

        mockMvc.perform(post("/partners")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(p)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name", is("Expedition Corp")));
    }

    @Test
    void getCommissionReport_found() throws Exception {
        UUID id = UUID.randomUUID();
        Partner p = new Partner();
        p.setId(id);
        p.setName("Trek Agency");
        p.setCommissionRate(new BigDecimal("10.00"));

        when(partnerRepository.findById(id)).thenReturn(Optional.of(p));

        mockMvc.perform(get("/partners/{id}/commission-report", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name", is("Trek Agency")));
    }

    @Test
    void getCommissionReport_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(partnerRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/partners/{id}/commission-report", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void createPartnerBooking_returns201() throws Exception {
        PartnerBooking b = new PartnerBooking();
        b.setPartnerId(UUID.randomUUID());
        b.setExternalReference("EXT-001");
        b.setCommissionRate(new BigDecimal("10.00"));
        b.setStatus(PartnerBooking.BookingStatus.PENDING);

        when(partnerBookingRepository.save(any(PartnerBooking.class))).thenReturn(b);

        mockMvc.perform(post("/partner-bookings")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(b)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.externalReference", is("EXT-001")));
    }

    @Test
    void getPartnerBooking_found() throws Exception {
        UUID id = UUID.randomUUID();
        PartnerBooking b = new PartnerBooking();
        b.setId(id);
        b.setPartnerId(UUID.randomUUID());
        b.setExternalReference("EXT-002");
        b.setCommissionRate(new BigDecimal("12.00"));
        b.setStatus(PartnerBooking.BookingStatus.CONFIRMED);

        when(partnerBookingRepository.findById(id)).thenReturn(Optional.of(b));

        mockMvc.perform(get("/partner-bookings/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("CONFIRMED")));
    }

    @Test
    void getPartnerBooking_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(partnerBookingRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/partner-bookings/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updatePartnerBooking_patchFields() throws Exception {
        UUID id = UUID.randomUUID();
        PartnerBooking existing = new PartnerBooking();
        existing.setId(id);
        existing.setPartnerId(UUID.randomUUID());
        existing.setExternalReference("EXT-003");
        existing.setCommissionRate(new BigDecimal("10.00"));
        existing.setStatus(PartnerBooking.BookingStatus.PENDING);

        PartnerBooking updated = new PartnerBooking();
        updated.setId(id);
        updated.setPartnerId(existing.getPartnerId());
        updated.setExternalReference("EXT-003");
        updated.setCommissionRate(new BigDecimal("10.00"));
        updated.setStatus(PartnerBooking.BookingStatus.CONFIRMED);

        when(partnerBookingRepository.findById(id)).thenReturn(Optional.of(existing));
        when(partnerBookingRepository.save(any(PartnerBooking.class))).thenReturn(updated);

        mockMvc.perform(patch("/partner-bookings/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updated)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("CONFIRMED")));
    }

    @Test
    void confirmPartnerBooking_found() throws Exception {
        UUID id = UUID.randomUUID();
        PartnerBooking b = new PartnerBooking();
        b.setId(id);
        b.setPartnerId(UUID.randomUUID());
        b.setExternalReference("EXT-004");
        b.setCommissionRate(new BigDecimal("10.00"));
        b.setStatus(PartnerBooking.BookingStatus.CONFIRMED);

        when(partnerBookingRepository.findById(id)).thenReturn(Optional.of(b));
        when(partnerBookingRepository.save(any(PartnerBooking.class))).thenReturn(b);

        mockMvc.perform(post("/partner-bookings/{id}/confirm", id))
                .andExpect(status().isOk());
    }

    // --- PartnerBookingsController PATCH coverage ---

    @Test
    void updatePartnerBooking_allFields() throws Exception {
        UUID id = UUID.randomUUID();
        PartnerBooking existing = new PartnerBooking();
        existing.setId(id);
        when(partnerBookingRepository.findById(id)).thenReturn(Optional.of(existing));
        when(partnerBookingRepository.save(any(PartnerBooking.class))).thenReturn(existing);

        mockMvc.perform(patch("/partner-bookings/{bookingId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"partnerId\":\"00000000-0000-0000-0000-000000000001\",\"externalReference\":\"EXT-ALL\",\"reservationId\":\"00000000-0000-0000-0000-000000000002\",\"status\":\"PENDING\",\"commissionRate\":15.00,\"commissionAmount\":150.00,\"bookingTotal\":1000.00,\"activityId\":\"00000000-0000-0000-0000-000000000003\",\"tripDate\":\"2026-06-15\",\"participantCount\":4}"))
                .andExpect(status().isOk());
    }

    @Test
    void updatePartnerBooking_emptyBody() throws Exception {
        UUID id = UUID.randomUUID();
        PartnerBooking existing = new PartnerBooking();
        existing.setId(id);
        when(partnerBookingRepository.findById(id)).thenReturn(Optional.of(existing));
        when(partnerBookingRepository.save(any(PartnerBooking.class))).thenReturn(existing);

        mockMvc.perform(patch("/partner-bookings/{bookingId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isOk());
    }

    @Test
    void updatePartnerBooking_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(partnerBookingRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/partner-bookings/{bookingId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }
}
