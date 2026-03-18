package com.novatrek.guestprofiles.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.guestprofiles.entity.Guest;
import com.novatrek.guestprofiles.repository.GuestRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(GuestController.class)
class GuestControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private GuestRepository guestRepository;

    private Guest createTestGuest() {
        Guest guest = new Guest();
        guest.setGuestId(UUID.randomUUID());
        guest.setFirstName("Jane");
        guest.setLastName("Explorer");
        guest.setEmail("jane@novatrek.example.com");
        guest.setPhone("+1-555-0100");
        guest.setDateOfBirth(LocalDate.of(1990, 6, 15));
        guest.setLoyaltyTier(Guest.LoyaltyTier.PATHFINDER);
        return guest;
    }

    @Test
    void listGuests_returnsAllGuests() throws Exception {
        Guest guest = createTestGuest();
        when(guestRepository.findAll()).thenReturn(List.of(guest));

        mockMvc.perform(get("/guests"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].firstName").value("Jane"))
                .andExpect(jsonPath("$[0].lastName").value("Explorer"));
    }

    @Test
    void listGuests_returnsEmptyList() throws Exception {
        when(guestRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/guests"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void createGuest_returns201() throws Exception {
        Guest guest = createTestGuest();
        when(guestRepository.save(any(Guest.class))).thenReturn(guest);

        Guest input = new Guest();
        input.setFirstName("Jane");
        input.setLastName("Explorer");
        input.setEmail("jane@novatrek.example.com");

        mockMvc.perform(post("/guests")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(input)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.firstName").value("Jane"))
                .andExpect(jsonPath("$.email").value("jane@novatrek.example.com"));
    }

    @Test
    void getGuest_returnsGuest() throws Exception {
        Guest guest = createTestGuest();
        UUID id = guest.getGuestId();
        when(guestRepository.findById(id)).thenReturn(Optional.of(guest));

        mockMvc.perform(get("/guests/{guestId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Jane"))
                .andExpect(jsonPath("$.loyaltyTier").value("PATHFINDER"));
    }

    @Test
    void getGuest_returns404WhenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(guestRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/guests/{guestId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateGuest_patchesFields() throws Exception {
        Guest existing = createTestGuest();
        UUID id = existing.getGuestId();
        when(guestRepository.findById(id)).thenReturn(Optional.of(existing));
        when(guestRepository.save(any(Guest.class))).thenAnswer(inv -> inv.getArgument(0));

        String patchJson = """
                {"firstName": "Janet", "loyaltyTier": "SUMMIT"}
                """;

        mockMvc.perform(patch("/guests/{guestId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patchJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Janet"))
                .andExpect(jsonPath("$.loyaltyTier").value("SUMMIT"))
                .andExpect(jsonPath("$.lastName").value("Explorer"));
    }

    @Test
    void updateGuest_returns404WhenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(guestRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/guests/{guestId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"firstName\": \"Janet\"}"))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateGuest_patchesOptionalFields() throws Exception {
        Guest existing = createTestGuest();
        UUID id = existing.getGuestId();
        when(guestRepository.findById(id)).thenReturn(Optional.of(existing));
        when(guestRepository.save(any(Guest.class))).thenAnswer(inv -> inv.getArgument(0));

        String patchJson = """
                {"phone": "+1-555-0999", "profileImageUrl": "https://cdn.novatrek.example.com/img.jpg", "preferredLanguage": "es"}
                """;

        mockMvc.perform(patch("/guests/{guestId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patchJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.phone").value("+1-555-0999"))
                .andExpect(jsonPath("$.profileImageUrl").value("https://cdn.novatrek.example.com/img.jpg"))
                .andExpect(jsonPath("$.preferredLanguage").value("es"));
    }
}
