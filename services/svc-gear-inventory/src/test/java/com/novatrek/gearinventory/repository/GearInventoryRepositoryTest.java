package com.novatrek.gearinventory.repository;

import com.novatrek.gearinventory.entity.GearItem;
import com.novatrek.gearinventory.entity.GearPackage;
import com.novatrek.gearinventory.entity.GearAssignment;
import com.novatrek.gearinventory.entity.MaintenanceRecord;
import com.novatrek.gearinventory.entity.InventoryLevel;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class GearInventoryRepositoryTest {

    @Autowired
    private GearItemRepository gearItemRepository;

    @Autowired
    private GearPackageRepository gearPackageRepository;

    @Autowired
    private GearAssignmentRepository gearAssignmentRepository;

    @Autowired
    private MaintenanceRecordRepository maintenanceRecordRepository;

    @Autowired
    private InventoryLevelRepository inventoryLevelRepository;

    @Test
    void saveAndFindGearItem() {
        GearItem item = new GearItem();
        item.setName("Alpine Harness");
        item.setCategory(GearItem.GearCategory.HARNESS);
        item.setSize(GearItem.GearSize.L);
        item.setCondition(GearItem.GearCondition.GOOD);
        item.setLocationId(UUID.randomUUID());
        item.setSerialNumber("HRN-201");
        item.setPurchaseDate(LocalDate.of(2025, 6, 1));
        item.setStatus(GearItem.Status.AVAILABLE);

        GearItem saved = gearItemRepository.save(item);
        assertThat(saved.getId()).isNotNull();

        Optional<GearItem> found = gearItemRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alpine Harness");
        assertThat(found.get().getCategory()).isEqualTo(GearItem.GearCategory.HARNESS);
    }

    @Test
    void saveAndFindGearPackage() {
        GearPackage pkg = new GearPackage();
        pkg.setName("Kayaking Adventure Pack");
        pkg.setDescription("Complete kayaking gear set");
        pkg.setActivityType(GearPackage.ActivityType.KAYAKING);
        pkg.setRentalPricePerDay(new BigDecimal("75.00"));

        GearPackage saved = gearPackageRepository.save(pkg);
        assertThat(saved.getId()).isNotNull();

        Optional<GearPackage> found = gearPackageRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getActivityType()).isEqualTo(GearPackage.ActivityType.KAYAKING);
    }

    @Test
    void saveAndFindGearAssignment() {
        GearAssignment a = new GearAssignment();
        a.setReservationId(UUID.randomUUID());
        a.setParticipantGuestId(UUID.randomUUID());
        a.setAssignedAt(OffsetDateTime.now());

        GearAssignment saved = gearAssignmentRepository.save(a);
        assertThat(saved.getId()).isNotNull();

        Optional<GearAssignment> found = gearAssignmentRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getReservationId()).isEqualTo(a.getReservationId());
    }

    @Test
    void saveAndFindMaintenanceRecord() {
        MaintenanceRecord mr = new MaintenanceRecord();
        mr.setGearItemId(UUID.randomUUID());
        mr.setType(MaintenanceRecord.Type.INSPECTION);
        mr.setDate(OffsetDateTime.now());
        mr.setTechnician("Jake Thompson");
        mr.setNotes("Regular quarterly inspection");
        mr.setCost(new BigDecimal("25.00"));

        MaintenanceRecord saved = maintenanceRecordRepository.save(mr);
        assertThat(saved.getId()).isNotNull();

        Optional<MaintenanceRecord> found = maintenanceRecordRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getTechnician()).isEqualTo("Jake Thompson");
    }

    @Test
    void saveAndFindInventoryLevel() {
        InventoryLevel il = new InventoryLevel();
        il.setLocationName("Base Camp Alpha");
        il.setCategory(InventoryLevel.GearCategory.HELMET);
        il.setTotal(50);
        il.setAvailable(35);
        il.setAssigned(10);
        il.setInMaintenance(5);

        InventoryLevel saved = inventoryLevelRepository.save(il);
        assertThat(saved.getLocationId()).isNotNull();

        Optional<InventoryLevel> found = inventoryLevelRepository.findById(saved.getLocationId());
        assertThat(found).isPresent();
        assertThat(found.get().getAvailable()).isEqualTo(35);
    }
}
