package com.novatrek.guestprofiles.repository;

import com.novatrek.guestprofiles.entity.Guest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class GuestRepositoryTest {

    @Autowired
    private GuestRepository guestRepository;

    private Guest createGuest(String email) {
        Guest guest = new Guest();
        guest.setFirstName("Test");
        guest.setLastName("User");
        guest.setEmail(email);
        guest.setDateOfBirth(LocalDate.of(1985, 3, 20));
        return guest;
    }

    @Test
    void saveAndFindById() {
        Guest saved = guestRepository.save(createGuest("test1@novatrek.example.com"));

        assertThat(saved.getGuestId()).isNotNull();
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        Optional<Guest> found = guestRepository.findById(saved.getGuestId());
        assertThat(found).isPresent();
        assertThat(found.get().getEmail()).isEqualTo("test1@novatrek.example.com");
    }

    @Test
    void findByEmail() {
        guestRepository.save(createGuest("find@novatrek.example.com"));

        Optional<Guest> found = guestRepository.findByEmail("find@novatrek.example.com");
        assertThat(found).isPresent();
        assertThat(found.get().getFirstName()).isEqualTo("Test");
    }

    @Test
    void findByEmail_notFound() {
        Optional<Guest> found = guestRepository.findByEmail("nonexistent@novatrek.example.com");
        assertThat(found).isEmpty();
    }

    @Test
    void findAll_returnsMultiple() {
        guestRepository.save(createGuest("a@novatrek.example.com"));
        guestRepository.save(createGuest("b@novatrek.example.com"));

        assertThat(guestRepository.findAll()).hasSizeGreaterThanOrEqualTo(2);
    }

    @Test
    void updateGuest_incrementsVersion() {
        Guest saved = guestRepository.save(createGuest("version@novatrek.example.com"));
        assertThat(saved.getVersion()).isEqualTo(0);

        saved.setLoyaltyTier(Guest.LoyaltyTier.SUMMIT);
        Guest updated = guestRepository.saveAndFlush(saved);
        assertThat(updated.getVersion()).isEqualTo(1);
    }

    @Test
    void defaultValues_appliedCorrectly() {
        Guest saved = guestRepository.save(createGuest("defaults@novatrek.example.com"));

        assertThat(saved.getStatus()).isEqualTo(Guest.GuestStatus.ACTIVE);
        assertThat(saved.getLoyaltyTier()).isEqualTo(Guest.LoyaltyTier.EXPLORER);
        assertThat(saved.getTotalAdventures()).isEqualTo(0);
    }
}
