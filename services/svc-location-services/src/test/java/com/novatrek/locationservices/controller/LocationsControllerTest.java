package com.novatrek.locationservices.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.locationservices.entity.Location;
import com.novatrek.locationservices.repository.LocationRepository;
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

@WebMvcTest(LocationsController.class)
class LocationsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private LocationRepository locationRepository;

    @Test
    void listLocations_returnsEmptyList() throws Exception {
        when(locationRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/locations"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void listLocations_returnsLocations() throws Exception {
        Location loc = new Location();
        loc.setName("Glacier Base Camp");
        loc.setType(Location.LocationType.BASE_CAMP);
        loc.setRegionId(UUID.randomUUID());
        loc.setCapacity(200);
        loc.setStatus(Location.LocationStatus.ACTIVE);

        when(locationRepository.findAll()).thenReturn(List.of(loc));

        mockMvc.perform(get("/locations"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name", is("Glacier Base Camp")));
    }

    @Test
    void createLocation_returns201() throws Exception {
        Location loc = new Location();
        loc.setName("Summit Outpost");
        loc.setType(Location.LocationType.OUTPOST);
        loc.setRegionId(UUID.randomUUID());
        loc.setCapacity(50);
        loc.setStatus(Location.LocationStatus.ACTIVE);

        when(locationRepository.save(any(Location.class))).thenReturn(loc);

        mockMvc.perform(post("/locations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(loc)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name", is("Summit Outpost")));
    }

    @Test
    void getLocation_found() throws Exception {
        UUID id = UUID.randomUUID();
        Location loc = new Location();
        loc.setId(id);
        loc.setName("Ranger Station Alpha");
        loc.setType(Location.LocationType.RANGER_STATION);
        loc.setRegionId(UUID.randomUUID());
        loc.setStatus(Location.LocationStatus.ACTIVE);

        when(locationRepository.findById(id)).thenReturn(Optional.of(loc));

        mockMvc.perform(get("/locations/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name", is("Ranger Station Alpha")));
    }

    @Test
    void getLocation_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(locationRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/locations/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateLocation_patchFields() throws Exception {
        UUID id = UUID.randomUUID();
        Location existing = new Location();
        existing.setId(id);
        existing.setName("Gear Rental Shop");
        existing.setType(Location.LocationType.RENTAL_SHOP);
        existing.setRegionId(UUID.randomUUID());
        existing.setCapacity(30);
        existing.setStatus(Location.LocationStatus.ACTIVE);

        Location updated = new Location();
        updated.setId(id);
        updated.setName("Gear Rental Shop");
        updated.setType(Location.LocationType.RENTAL_SHOP);
        updated.setRegionId(existing.getRegionId());
        updated.setCapacity(30);
        updated.setStatus(Location.LocationStatus.MAINTENANCE);

        when(locationRepository.findById(id)).thenReturn(Optional.of(existing));
        when(locationRepository.save(any(Location.class))).thenReturn(updated);

        mockMvc.perform(patch("/locations/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updated)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("MAINTENANCE")));
    }

    @Test
    void updateLocation_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(locationRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/locations/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }

    @Test
    void getLocationCapacity_found() throws Exception {
        UUID id = UUID.randomUUID();
        Location loc = new Location();
        loc.setId(id);
        loc.setName("HQ");
        loc.setType(Location.LocationType.HEADQUARTERS);
        loc.setRegionId(UUID.randomUUID());
        loc.setCapacity(500);
        loc.setStatus(Location.LocationStatus.ACTIVE);

        when(locationRepository.findById(id)).thenReturn(Optional.of(loc));

        mockMvc.perform(get("/locations/{id}/capacity", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.capacity", is(500)));
    }

    @Test
    void getLocationCapacity_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(locationRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/locations/{id}/capacity", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void getOperatingHours_found() throws Exception {
        UUID id = UUID.randomUUID();
        Location loc = new Location();
        loc.setId(id);
        loc.setName("River Launch Point");
        loc.setType(Location.LocationType.OUTPOST);
        loc.setRegionId(UUID.randomUUID());
        loc.setStatus(Location.LocationStatus.SEASONAL_CLOSURE);

        when(locationRepository.findById(id)).thenReturn(Optional.of(loc));

        mockMvc.perform(get("/locations/{id}/operating-hours", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("SEASONAL_CLOSURE")));
    }

    @Test
    void getOperatingHours_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(locationRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/locations/{id}/operating-hours", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateLocation_emptyBody() throws Exception {
        UUID id = UUID.randomUUID();
        Location existing = new Location();
        existing.setId(id);
        existing.setName("Base Camp");
        existing.setType(Location.LocationType.BASE_CAMP);
        existing.setRegionId(UUID.randomUUID());
        existing.setCapacity(50);
        existing.setStatus(Location.LocationStatus.ACTIVE);

        when(locationRepository.findById(id)).thenReturn(Optional.of(existing));
        when(locationRepository.save(any(Location.class))).thenReturn(existing);

        mockMvc.perform(patch("/locations/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isOk());
    }
}
