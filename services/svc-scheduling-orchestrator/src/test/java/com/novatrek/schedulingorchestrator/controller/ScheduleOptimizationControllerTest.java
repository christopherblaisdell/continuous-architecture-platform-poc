package com.novatrek.schedulingorchestrator.controller;

import com.novatrek.schedulingorchestrator.entity.ConflictResolutionResult;
import com.novatrek.schedulingorchestrator.repository.ConflictResolutionResultRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.hamcrest.Matchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ScheduleOptimizationController.class)
class ScheduleOptimizationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ConflictResolutionResultRepository conflictResolutionResultRepository;

    @Test
    void getScheduleOptimization_returnsResults() throws Exception {
        ConflictResolutionResult r = new ConflictResolutionResult();
        r.setResolutionStatus(ConflictResolutionResult.ResolutionStatus.PARTIALLY_RESOLVED);
        r.setAppliedStrategy("ADJUST_CAPACITY");

        when(conflictResolutionResultRepository.findAll()).thenReturn(List.of(r));

        mockMvc.perform(get("/schedule-optimization"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].appliedStrategy", is("ADJUST_CAPACITY")));
    }
}
