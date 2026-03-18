package com.novatrek.checkin.repository;

import com.novatrek.checkin.entity.CheckIn;
import com.novatrek.checkin.entity.GearItem;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class CheckInRepositoryTest {

    @Autowired
    private CheckInRepository checkInRepository;

    @Autowired
    private GearItemRepository gearItemRepository;

    @Test
    void saveAndFindCheckIn() {
        CheckIn c = new CheckIn();
        c.setReservationId(UUID.randomUUID());
        c.setParticipantGuestId(UUID.randomUUID());
        c.setStatus(CheckIn.CheckInStatus.INITIATED);
        c.setCheckedInAt(OffsetDateTime.now());
        c.setCheckedInBy(UUID.randomUUID());

        CheckIn saved = checkInRepository.save(c);
        assertThat(saved.getId()).isNotNull();

        Optional<CheckIn> found = checkInRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getStatus()).isEqualTo(CheckIn.CheckInStatus.INITIATED);
    }

    @Test
    void saveAndFindGearItem() {
        GearItem g = new GearItem();
        g.setGearType("Helmet");
        g.setSize("M");
        g.setConditionOnIssue(GearItem.ConditionOnIssue.NEW);

        GearItem saved = gearItemRepository.save(g);
        assertThat(saved.getGearInventoryId()).isNotNull();

        Optional<GearItem> found = gearItemRepository.findById(saved.getGearInventoryId());
        assertThat(found).isPresent();
        assertThat(found.get().getGearType()).isEqualTo("Helmet");
    }

    @Test
    void checkInStatusTransition() {
        CheckIn c = new CheckIn();
        c.setReservationId(UUID.randomUUID());
        c.setParticipantGuestId(UUID.randomUUID());
        c.setStatus(CheckIn.CheckInStatus.INITIATED);
        c.setCheckedInAt(OffsetDateTime.now());
        c.setCheckedInBy(UUID.randomUUID());

        CheckIn saved = checkInRepository.save(c);
        saved.setStatus(CheckIn.CheckInStatus.GEAR_VERIFIED);
        saved.setGearVerified(true);
        CheckIn updated = checkInRepository.save(saved);

        assertThat(updated.getStatus()).isEqualTo(CheckIn.CheckInStatus.GEAR_VERIFIED);
        assertThat(updated.getGearVerified()).isTrue();
    }
}
