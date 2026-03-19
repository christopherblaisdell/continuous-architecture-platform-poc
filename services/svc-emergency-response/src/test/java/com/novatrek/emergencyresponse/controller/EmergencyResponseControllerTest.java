package com.novatrek.emergencyresponse.controller;

import com.novatrek.emergencyresponse.entity.Emergency;
import com.novatrek.emergencyresponse.entity.DispatchRecord;
import com.novatrek.emergencyresponse.repository.EmergencyRepository;
import com.novatrek.emergencyresponse.repository.DispatchRecordRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({EmergenciesController.class, RescueTeamsController.class, EmergencyContactsController.class})
@ActiveProfiles("test")
class EmergencyResponseControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private EmergencyRepository emergencyRepository;

    @MockBean
    private DispatchRecordRepository dispatchRecordRepository;

    // --- EmergenciesController ---

    @Test
    void listEmergencies_returnsList() throws Exception {
        when(emergencyRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/emergencies"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    @Test
    void triggerEmergency_returns201() throws Exception {
        Emergency e = new Emergency();
        e.setEmergencyId(UUID.randomUUID());
        e.setType("medical");
        e.setSeverity("high");
        e.setStatus("active");
        e.setDescription("Guest fell on trail");
        when(emergencyRepository.save(any(Emergency.class))).thenReturn(e);

        mockMvc.perform(post("/emergencies")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"type\":\"medical\",\"severity\":\"high\",\"status\":\"active\",\"description\":\"Guest fell on trail\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.type").value("medical"));
    }

    @Test
    void getEmergency_found() throws Exception {
        UUID id = UUID.randomUUID();
        Emergency e = new Emergency();
        e.setEmergencyId(id);
        e.setType("weather");
        e.setStatus("active");
        when(emergencyRepository.findById(id)).thenReturn(Optional.of(e));

        mockMvc.perform(get("/emergencies/{emergencyId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.type").value("weather"));
    }

    @Test
    void getEmergency_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(emergencyRepository.findById(id)).thenReturn(Optional.empty());
        mockMvc.perform(get("/emergencies/{emergencyId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateEmergencyStatus_found() throws Exception {
        UUID id = UUID.randomUUID();
        Emergency existing = new Emergency();
        existing.setEmergencyId(id);
        existing.setStatus("active");
        when(emergencyRepository.findById(id)).thenReturn(Optional.of(existing));
        when(emergencyRepository.save(any(Emergency.class))).thenReturn(existing);

        mockMvc.perform(patch("/emergencies/{emergencyId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\":\"resolved\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void getEmergencyTimeline_found() throws Exception {
        UUID id = UUID.randomUUID();
        Emergency e = new Emergency();
        e.setEmergencyId(id);
        when(emergencyRepository.findById(id)).thenReturn(Optional.of(e));

        mockMvc.perform(get("/emergencies/{emergencyId}/timeline", id))
                .andExpect(status().isOk());
    }

    @Test
    void dispatchRescueTeam_returns201() throws Exception {
        UUID id = UUID.randomUUID();
        Emergency e = new Emergency();
        e.setEmergencyId(id);
        when(emergencyRepository.save(any(Emergency.class))).thenReturn(e);

        mockMvc.perform(post("/emergencies/{emergencyId}/dispatch", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\":\"dispatching\"}"))
                .andExpect(status().isCreated());
    }

    // --- RescueTeamsController ---

    @Test
    void listRescueTeams_returnsList() throws Exception {
        when(dispatchRecordRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/rescue-teams"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    // --- EmergencyContactsController ---

    @Test
    void getGuestEmergencyContacts_found() throws Exception {
        UUID guestId = UUID.randomUUID();
        DispatchRecord dr = new DispatchRecord();
        dr.setDispatchId(guestId);
        dr.setPriority("high");
        when(dispatchRecordRepository.findById(guestId)).thenReturn(Optional.of(dr));

        mockMvc.perform(get("/emergency-contacts/{guestId}", guestId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.priority").value("high"));
    }

    @Test
    void getGuestEmergencyContacts_notFound() throws Exception {
        UUID guestId = UUID.randomUUID();
        when(dispatchRecordRepository.findById(guestId)).thenReturn(Optional.empty());
        mockMvc.perform(get("/emergency-contacts/{guestId}", guestId))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateGuestEmergencyContacts_found() throws Exception {
        UUID guestId = UUID.randomUUID();
        DispatchRecord dr = new DispatchRecord();
        dr.setDispatchId(guestId);
        when(dispatchRecordRepository.findById(guestId)).thenReturn(Optional.of(dr));
        when(dispatchRecordRepository.save(any(DispatchRecord.class))).thenReturn(dr);

        mockMvc.perform(put("/emergency-contacts/{guestId}", guestId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"priority\":\"critical\"}"))
                .andExpect(status().isOk());
    }

    // --- EmergenciesController PATCH coverage ---

    @Test
    void updateEmergency_allFields() throws Exception {
        UUID id = UUID.randomUUID();
        Emergency existing = new Emergency();
        existing.setEmergencyId(id);
        when(emergencyRepository.findById(id)).thenReturn(Optional.of(existing));
        when(emergencyRepository.save(any(Emergency.class))).thenReturn(existing);

        mockMvc.perform(patch("/emergencies/{emergencyId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"guestId\":\"00000000-0000-0000-0000-000000000001\",\"reservationId\":\"00000000-0000-0000-0000-000000000002\",\"type\":\"MEDICAL\",\"severity\":\"HIGH\",\"status\":\"IN_PROGRESS\",\"description\":\"Test\",\"reportedBy\":\"Guide\",\"dispatchId\":\"00000000-0000-0000-0000-000000000003\",\"resolutionNotes\":\"Resolved\",\"rev\":\"2\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void updateEmergency_emptyBody() throws Exception {
        UUID id = UUID.randomUUID();
        Emergency existing = new Emergency();
        existing.setEmergencyId(id);
        when(emergencyRepository.findById(id)).thenReturn(Optional.of(existing));
        when(emergencyRepository.save(any(Emergency.class))).thenReturn(existing);

        mockMvc.perform(patch("/emergencies/{emergencyId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isOk());
    }

    @Test
    void updateEmergency_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(emergencyRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/emergencies/{emergencyId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }
}
