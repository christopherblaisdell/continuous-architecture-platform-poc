package com.novatrek.safetycompliance.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.safetycompliance.entity.Waiver;
import com.novatrek.safetycompliance.entity.SafetyInspection;
import com.novatrek.safetycompliance.entity.IncidentReport;
import com.novatrek.safetycompliance.repository.WaiverRepository;
import com.novatrek.safetycompliance.repository.SafetyInspectionRepository;
import com.novatrek.safetycompliance.repository.IncidentReportRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({WaiversController.class, SafetyInspectionsController.class, IncidentsController.class})
class SafetyComplianceControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private WaiverRepository waiverRepository;

    @MockBean
    private SafetyInspectionRepository safetyInspectionRepository;

    @MockBean
    private IncidentReportRepository incidentReportRepository;

    // --- Waivers ---

    @Test
    void listWaivers_returnsEmptyList() throws Exception {
        when(waiverRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/waivers"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void signWaiver_returns201() throws Exception {
        Waiver w = new Waiver();
        w.setGuestId(UUID.randomUUID());
        w.setReservationId(UUID.randomUUID());
        w.setWaiverType(Waiver.WaiverType.GENERAL_LIABILITY);
        w.setSignedAt(OffsetDateTime.now());
        w.setStatus(Waiver.WaiverStatus.ACTIVE);

        when(waiverRepository.save(any(Waiver.class))).thenReturn(w);

        mockMvc.perform(post("/waivers")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(w)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.waiverType", is("GENERAL_LIABILITY")));
    }

    @Test
    void getWaiver_returnsWaiver() throws Exception {
        UUID id = UUID.randomUUID();
        Waiver w = new Waiver();
        w.setId(id);
        w.setGuestId(UUID.randomUUID());
        w.setReservationId(UUID.randomUUID());
        w.setWaiverType(Waiver.WaiverType.HIGH_ALTITUDE);
        w.setSignedAt(OffsetDateTime.now());
        w.setStatus(Waiver.WaiverStatus.ACTIVE);

        when(waiverRepository.findById(id)).thenReturn(Optional.of(w));

        mockMvc.perform(get("/waivers/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.waiverType", is("HIGH_ALTITUDE")));
    }

    @Test
    void getWaiver_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(waiverRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/waivers/{id}", id))
                .andExpect(status().isNotFound());
    }

    // --- Safety Inspections ---

    @Test
    void listSafetyInspections_returnsList() throws Exception {
        SafetyInspection si = new SafetyInspection();
        si.setLocationId(UUID.randomUUID());
        si.setInspectorId(UUID.randomUUID());
        si.setInspectionDate(LocalDate.of(2026, 6, 1));
        si.setStatus(SafetyInspection.InspectionStatus.PASSED);

        when(safetyInspectionRepository.findAll()).thenReturn(List.of(si));

        mockMvc.perform(get("/safety-inspections"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].status", is("PASSED")));
    }

    @Test
    void createSafetyInspection_returns201() throws Exception {
        SafetyInspection si = new SafetyInspection();
        si.setLocationId(UUID.randomUUID());
        si.setInspectorId(UUID.randomUUID());
        si.setInspectionDate(LocalDate.of(2026, 7, 1));
        si.setStatus(SafetyInspection.InspectionStatus.CONDITIONAL_PASS);
        si.setNotes("Minor railing repair needed");

        when(safetyInspectionRepository.save(any(SafetyInspection.class))).thenReturn(si);

        mockMvc.perform(post("/safety-inspections")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(si)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status", is("CONDITIONAL_PASS")));
    }

    // --- Incidents ---

    @Test
    void createIncident_returns201() throws Exception {
        IncidentReport ir = new IncidentReport();
        ir.setReservationId(UUID.randomUUID());
        ir.setGuideId(UUID.randomUUID());
        ir.setType(IncidentReport.IncidentType.NEAR_MISS);
        ir.setSeverity(IncidentReport.IncidentSeverity.MEDIUM);
        ir.setDescription("Guest slipped on wet rocks");
        ir.setReportedAt(OffsetDateTime.now());
        ir.setStatus(IncidentReport.Status.OPEN);

        when(incidentReportRepository.save(any(IncidentReport.class))).thenReturn(ir);

        mockMvc.perform(post("/incidents")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(ir)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.type", is("NEAR_MISS")));
    }

    @Test
    void getIncident_returnsIncident() throws Exception {
        UUID id = UUID.randomUUID();
        IncidentReport ir = new IncidentReport();
        ir.setId(id);
        ir.setReservationId(UUID.randomUUID());
        ir.setGuideId(UUID.randomUUID());
        ir.setType(IncidentReport.IncidentType.EQUIPMENT_FAILURE);
        ir.setSeverity(IncidentReport.IncidentSeverity.HIGH);
        ir.setDescription("Harness buckle malfunction");
        ir.setReportedAt(OffsetDateTime.now());
        ir.setStatus(IncidentReport.Status.UNDER_REVIEW);

        when(incidentReportRepository.findById(id)).thenReturn(Optional.of(ir));

        mockMvc.perform(get("/incidents/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.type", is("EQUIPMENT_FAILURE")));
    }

    @Test
    void getIncident_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(incidentReportRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/incidents/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateIncident_patchFields() throws Exception {
        UUID id = UUID.randomUUID();
        IncidentReport existing = new IncidentReport();
        existing.setId(id);
        existing.setReservationId(UUID.randomUUID());
        existing.setGuideId(UUID.randomUUID());
        existing.setType(IncidentReport.IncidentType.INJURY);
        existing.setSeverity(IncidentReport.IncidentSeverity.LOW);
        existing.setDescription("Minor scrape");
        existing.setReportedAt(OffsetDateTime.now());
        existing.setStatus(IncidentReport.Status.OPEN);

        IncidentReport updated = new IncidentReport();
        updated.setId(id);
        updated.setReservationId(existing.getReservationId());
        updated.setGuideId(existing.getGuideId());
        updated.setType(IncidentReport.IncidentType.INJURY);
        updated.setSeverity(IncidentReport.IncidentSeverity.LOW);
        updated.setDescription("Minor scrape");
        updated.setReportedAt(existing.getReportedAt());
        updated.setStatus(IncidentReport.Status.RESOLVED);
        updated.setActionsTaken("First aid applied");

        when(incidentReportRepository.findById(id)).thenReturn(Optional.of(existing));
        when(incidentReportRepository.save(any(IncidentReport.class))).thenReturn(updated);

        mockMvc.perform(patch("/incidents/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updated)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("RESOLVED")));
    }
}
