package com.novatrek.reservations.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.reservations.entity.Reservation;
import com.novatrek.reservations.repository.ReservationRepository;
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

@WebMvcTest(ReservationsController.class)
class ReservationsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ReservationRepository reservationRepository;

    @Test
    void searchReservations_returnsEmptyList() throws Exception {
        when(reservationRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/reservations"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void searchReservations_returnsReservations() throws Exception {
        Reservation r = new Reservation();
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setStatus(Reservation.ReservationStatus.PENDING);
        r.setRev("1");

        when(reservationRepository.findAll()).thenReturn(List.of(r));

        mockMvc.perform(get("/reservations"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].status", is("PENDING")));
    }

    @Test
    void createReservation_returns201() throws Exception {
        Reservation r = new Reservation();
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setStatus(Reservation.ReservationStatus.PENDING);
        r.setBookingSource(Reservation.BookingSource.WEB_DIRECT);
        r.setTotalAmount(new BigDecimal("199.99"));
        r.setCurrency("USD");
        r.setRev("1");

        when(reservationRepository.save(any(Reservation.class))).thenReturn(r);

        mockMvc.perform(post("/reservations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(r)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status", is("PENDING")))
                .andExpect(jsonPath("$.bookingSource", is("WEB_DIRECT")));
    }

    @Test
    void getReservation_returnsList() throws Exception {
        when(reservationRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/reservations/{reservation_id}", UUID.randomUUID()))
                .andExpect(status().isOk());
    }

    @Test
    void addParticipant_returns201() throws Exception {
        Reservation r = new Reservation();
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setRev("1");

        when(reservationRepository.save(any(Reservation.class))).thenReturn(r);

        mockMvc.perform(post("/reservations/{reservation_id}/participants", UUID.randomUUID())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(r)))
                .andExpect(status().isCreated());
    }
}
