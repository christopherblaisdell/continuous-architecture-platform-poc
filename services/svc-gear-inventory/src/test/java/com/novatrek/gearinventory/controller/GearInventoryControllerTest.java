package com.novatrek.gearinventory.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.gearinventory.entity.GearItem;
import com.novatrek.gearinventory.entity.GearPackage;
import com.novatrek.gearinventory.entity.GearAssignment;
import com.novatrek.gearinventory.repository.GearItemRepository;
import com.novatrek.gearinventory.repository.GearPackageRepository;
import com.novatrek.gearinventory.repository.GearAssignmentRepository;
import com.novatrek.gearinventory.repository.MaintenanceRecordRepository;
import com.novatrek.gearinventory.repository.InventoryLevelRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({GearItemsController.class, GearPackagesController.class, GearAssignmentsController.class, InventoryLevelsController.class})
class GearInventoryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private GearItemRepository gearItemRepository;

    @MockBean
    private GearPackageRepository gearPackageRepository;

    @MockBean
    private GearAssignmentRepository gearAssignmentRepository;

    @MockBean
    private MaintenanceRecordRepository maintenanceRecordRepository;

    @MockBean
    private InventoryLevelRepository inventoryLevelRepository;

    @Test
    void searchGearItems_returnsEmptyList() throws Exception {
        when(gearItemRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/gear-items"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void searchGearItems_returnsItems() throws Exception {
        GearItem item = new GearItem();
        item.setName("Climbing Helmet");
        item.setCategory(GearItem.GearCategory.HELMET);
        item.setSize(GearItem.GearSize.M);
        item.setCondition(GearItem.GearCondition.NEW);
        item.setLocationId(UUID.randomUUID());
        item.setSerialNumber("HLM-001");
        item.setPurchaseDate(LocalDate.of(2026, 1, 15));
        item.setStatus(GearItem.Status.AVAILABLE);

        when(gearItemRepository.findAll()).thenReturn(List.of(item));

        mockMvc.perform(get("/gear-items"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name", is("Climbing Helmet")));
    }

    @Test
    void addGearItem_returns201() throws Exception {
        GearItem item = new GearItem();
        item.setName("Kayak Paddle");
        item.setCategory(GearItem.GearCategory.PADDLE);
        item.setSize(GearItem.GearSize.ONE_SIZE);
        item.setCondition(GearItem.GearCondition.NEW);
        item.setLocationId(UUID.randomUUID());
        item.setSerialNumber("PDL-042");
        item.setPurchaseDate(LocalDate.of(2026, 3, 1));
        item.setStatus(GearItem.Status.AVAILABLE);

        when(gearItemRepository.save(any(GearItem.class))).thenReturn(item);

        mockMvc.perform(post("/gear-items")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(item)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name", is("Kayak Paddle")));
    }

    @Test
    void listGearPackages_returnsPackages() throws Exception {
        GearPackage pkg = new GearPackage();
        pkg.setName("Rock Climbing Starter");
        pkg.setDescription("Basic rock climbing gear set");
        pkg.setActivityType(GearPackage.ActivityType.ROCK_CLIMBING);
        pkg.setRentalPricePerDay(new BigDecimal("49.99"));

        when(gearPackageRepository.findAll()).thenReturn(List.of(pkg));

        mockMvc.perform(get("/gear-packages"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name", is("Rock Climbing Starter")));
    }

    @Test
    void createGearAssignment_returns201() throws Exception {
        GearAssignment a = new GearAssignment();
        a.setReservationId(UUID.randomUUID());
        a.setParticipantGuestId(UUID.randomUUID());
        a.setAssignedAt(OffsetDateTime.now());

        when(gearAssignmentRepository.save(any(GearAssignment.class))).thenReturn(a);

        mockMvc.perform(post("/gear-assignments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(a)))
                .andExpect(status().isCreated());
    }

    @Test
    void getInventoryLevels_returnsList() throws Exception {
        when(gearAssignmentRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/inventory-levels"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void updateGearItem_unimplemented_returns500() throws Exception {
        mockMvc.perform(patch("/gear-items/{item_id}", UUID.randomUUID())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isInternalServerError());
    }
}
