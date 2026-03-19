package com.novatrek.schedulingorchestrator.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.schedulingorchestrator.entity.ConflictResolutionResult;
import com.novatrek.schedulingorchestrator.repository.ConflictResolutionResultRepository;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import jakarta.servlet.ServletException;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ScheduleRequestsController.class)
class ScheduleRequestsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ConflictResolutionResultRepository conflictResolutionResultRepository;

    @Test
    void getScheduleRequest_returnsResult() throws Exception {
        ConflictResolutionResult r = new ConflictResolutionResult();
        UUID id = UUID.randomUUID();
        r.setConflictId(id);
        r.setResolutionStatus(ConflictResolutionResult.ResolutionStatus.RESOLVED);
        r.setAppliedStrategy("REASSIGN_GUIDE");

        when(conflictResolutionResultRepository.findById(id)).thenReturn(Optional.of(r));

        mockMvc.perform(get("/schedule-requests/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.resolutionStatus", is("RESOLVED")));
    }

    @Test
    void getScheduleRequest_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(conflictResolutionResultRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/schedule-requests/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void createScheduleRequest_throwsUnsupported() {
        assertThrows(ServletException.class, () ->
                mockMvc.perform(post("/schedule-requests")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
        );
    }
}
