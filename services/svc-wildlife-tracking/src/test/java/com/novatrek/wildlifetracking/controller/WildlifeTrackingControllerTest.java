package com.novatrek.wildlifetracking.controller;

import com.novatrek.wildlifetracking.entity.Sighting;
import com.novatrek.wildlifetracking.entity.Species;
import com.novatrek.wildlifetracking.entity.HabitatZone;
import com.novatrek.wildlifetracking.entity.WildlifeAlert;
import com.novatrek.wildlifetracking.repository.SightingRepository;
import com.novatrek.wildlifetracking.repository.SpeciesRepository;
import com.novatrek.wildlifetracking.repository.HabitatZoneRepository;
import com.novatrek.wildlifetracking.repository.WildlifeAlertRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({SightingsController.class, SpeciesController.class,
        HabitatZonesController.class, AlertsController.class})
@ActiveProfiles("test")
class WildlifeTrackingControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SightingRepository sightingRepository;

    @MockBean
    private SpeciesRepository speciesRepository;

    @MockBean
    private HabitatZoneRepository habitatZoneRepository;

    @MockBean
    private WildlifeAlertRepository wildlifeAlertRepository;

    // --- SightingsController ---

    @Test
    void listSightings_returnsList() throws Exception {
        when(sightingRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/sightings"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    @Test
    void reportSighting_returns201() throws Exception {
        Sighting s = new Sighting();
        s.setSightingId(UUID.randomUUID());
        s.setSpeciesName("Black Bear");
        s.setAnimalCount(2);
        s.setReportedBy("Guide-Chen");
        when(sightingRepository.save(any(Sighting.class))).thenReturn(s);

        mockMvc.perform(post("/sightings")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"speciesName\":\"Black Bear\",\"animalCount\":2,\"reportedBy\":\"Guide-Chen\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.speciesName").value("Black Bear"));
    }

    @Test
    void getSighting_found() throws Exception {
        UUID id = UUID.randomUUID();
        Sighting s = new Sighting();
        s.setSightingId(id);
        s.setSpeciesName("Mountain Lion");
        when(sightingRepository.findById(id)).thenReturn(Optional.of(s));

        mockMvc.perform(get("/sightings/{sightingId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.speciesName").value("Mountain Lion"));
    }

    @Test
    void getSighting_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(sightingRepository.findById(id)).thenReturn(Optional.empty());
        mockMvc.perform(get("/sightings/{sightingId}", id))
                .andExpect(status().isNotFound());
    }

    // --- SpeciesController ---

    @Test
    void listSpecies_returnsList() throws Exception {
        Species sp = new Species();
        sp.setCommonName("Bald Eagle");
        sp.setThreatLevel(Species.ThreatLevel.low);
        sp.setCategory(Species.Category.bird);
        when(speciesRepository.findAll()).thenReturn(List.of(sp));

        mockMvc.perform(get("/species"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].commonName").value("Bald Eagle"));
    }

    @Test
    void getSpecies_found() throws Exception {
        UUID id = UUID.randomUUID();
        Species sp = new Species();
        sp.setSpeciesId(id);
        sp.setCommonName("Grizzly Bear");
        sp.setThreatLevel(Species.ThreatLevel.high);
        when(speciesRepository.findById(id)).thenReturn(Optional.of(sp));

        mockMvc.perform(get("/species/{speciesId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.commonName").value("Grizzly Bear"));
    }

    @Test
    void getSpecies_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(speciesRepository.findById(id)).thenReturn(Optional.empty());
        mockMvc.perform(get("/species/{speciesId}", id))
                .andExpect(status().isNotFound());
    }

    // --- HabitatZonesController ---

    @Test
    void listHabitatZones_returnsList() throws Exception {
        HabitatZone hz = new HabitatZone();
        hz.setName("Alpine Meadow");
        hz.setActivityLevel(HabitatZone.ActivityLevel.high);
        hz.setSeason("summer");
        when(habitatZoneRepository.findAll()).thenReturn(List.of(hz));

        mockMvc.perform(get("/habitat-zones"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Alpine Meadow"));
    }

    // --- AlertsController ---

    @Test
    void listWildlifeAlerts_returnsList() throws Exception {
        when(wildlifeAlertRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/alerts"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    @Test
    void issueWildlifeAlert_returns201() throws Exception {
        WildlifeAlert alert = new WildlifeAlert();
        alert.setAlertId(UUID.randomUUID());
        alert.setSpeciesName("Mountain Lion");
        alert.setThreatLevel("high");
        alert.setRadiusMeters(new BigDecimal("500.00"));
        when(wildlifeAlertRepository.save(any(WildlifeAlert.class))).thenReturn(alert);

        mockMvc.perform(post("/alerts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"speciesName\":\"Mountain Lion\",\"threatLevel\":\"high\",\"radiusMeters\":500.00}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.speciesName").value("Mountain Lion"));
    }

    @Test
    void getWildlifeAlert_found() throws Exception {
        UUID id = UUID.randomUUID();
        WildlifeAlert alert = new WildlifeAlert();
        alert.setAlertId(id);
        alert.setSpeciesName("Wolf Pack");
        when(wildlifeAlertRepository.findById(id)).thenReturn(Optional.of(alert));

        mockMvc.perform(get("/alerts/{alertId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.speciesName").value("Wolf Pack"));
    }

    @Test
    void getWildlifeAlert_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(wildlifeAlertRepository.findById(id)).thenReturn(Optional.empty());
        mockMvc.perform(get("/alerts/{alertId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateWildlifeAlert_found() throws Exception {
        UUID id = UUID.randomUUID();
        WildlifeAlert existing = new WildlifeAlert();
        existing.setAlertId(id);
        existing.setSpeciesName("Wolf Pack");
        existing.setStatus("active");
        when(wildlifeAlertRepository.findById(id)).thenReturn(Optional.of(existing));
        when(wildlifeAlertRepository.save(any(WildlifeAlert.class))).thenReturn(existing);

        mockMvc.perform(patch("/alerts/{alertId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\":\"cancelled\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void updateWildlifeAlert_allFields() throws Exception {
        UUID id = UUID.randomUUID();
        WildlifeAlert existing = new WildlifeAlert();
        existing.setAlertId(id);
        when(wildlifeAlertRepository.findById(id)).thenReturn(Optional.of(existing));
        when(wildlifeAlertRepository.save(any(WildlifeAlert.class))).thenReturn(existing);

        mockMvc.perform(patch("/alerts/{alertId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"speciesId\":\"00000000-0000-0000-0000-000000000001\",\"speciesName\":\"Mountain Lion\",\"sightingId\":\"00000000-0000-0000-0000-000000000002\",\"threatLevel\":\"HIGH\",\"status\":\"active\",\"radiusMeters\":500,\"recommendedAction\":\"Avoid area\",\"notes\":\"Near trail 7\",\"rev\":\"2\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void updateWildlifeAlert_emptyBody() throws Exception {
        UUID id = UUID.randomUUID();
        WildlifeAlert existing = new WildlifeAlert();
        existing.setAlertId(id);
        when(wildlifeAlertRepository.findById(id)).thenReturn(Optional.of(existing));
        when(wildlifeAlertRepository.save(any(WildlifeAlert.class))).thenReturn(existing);

        mockMvc.perform(patch("/alerts/{alertId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isOk());
    }

    @Test
    void updateWildlifeAlert_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(wildlifeAlertRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/alerts/{alertId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }
}
