package com.novatrek.checkin.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.checkin.entity.CheckIn;
import com.novatrek.checkin.repository.CheckInRepository;
import com.novatrek.checkin.repository.GearItemRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(CheckInsController.class)
class CheckInsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private CheckInRepository checkInRepository;

    @MockBean
    private GearItemRepository gearItemRepository;

    private CheckIn sampleCheckIn() {
        CheckIn c = new CheckIn();
        c.setReservationId(UUID.randomUUID());
        c.setParticipantGuestId(UUID.randomUUID());
        c.setStatus(CheckIn.CheckInStatus.INITIATED);
        c.setCheckedInAt(OffsetDateTime.now());
        c.setCheckedInBy(UUID.randomUUID());
        return c;
    }

    @Test
    void listCheckIns_returnsEmptyList() throws Exception {
        when(checkInRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/check-ins"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void listCheckIns_returnsCheckIns() throws Exception {
        CheckIn c = sampleCheckIn();
        when(checkInRepository.findAll()).thenReturn(List.of(c));

        mockMvc.perform(get("/check-ins"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].status", is("INITIATED")));
    }

    @Test
    void createCheckIn_returns201() throws Exception {
        CheckIn c = sampleCheckIn();
        when(checkInRepository.save(any(CheckIn.class))).thenReturn(c);

        mockMvc.perform(post("/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(c)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status", is("INITIATED")));
    }

    @Test
    void getCheckIn_returnsCheckIn() throws Exception {
        CheckIn c = sampleCheckIn();
        UUID id = UUID.randomUUID();
        c.setId(id);
        when(checkInRepository.findById(id)).thenReturn(Optional.of(c));

        mockMvc.perform(get("/check-ins/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("INITIATED")));
    }

    @Test
    void getCheckIn_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(checkInRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/check-ins/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void verifyGear_returnsCheckIn() throws Exception {
        CheckIn c = sampleCheckIn();
        UUID id = UUID.randomUUID();
        c.setId(id);
        when(checkInRepository.findById(id)).thenReturn(Optional.of(c));
        when(checkInRepository.save(any(CheckIn.class))).thenReturn(c);

        mockMvc.perform(post("/check-ins/{id}/gear-verification", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(c)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("INITIATED")));
    }

    @Test
    void assignWristband_returnsCheckIn() throws Exception {
        CheckIn c = sampleCheckIn();
        UUID id = UUID.randomUUID();
        c.setId(id);
        when(checkInRepository.findById(id)).thenReturn(Optional.of(c));
        when(checkInRepository.save(any(CheckIn.class))).thenReturn(c);

        mockMvc.perform(post("/check-ins/{id}/wristband-assignment", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(c)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("INITIATED")));
    }

    @Test
    void verifyGear_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(checkInRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(post("/check-ins/{id}/gear-verification", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }

    @Test
    void assignWristband_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(checkInRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(post("/check-ins/{id}/wristband-assignment", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }
}
