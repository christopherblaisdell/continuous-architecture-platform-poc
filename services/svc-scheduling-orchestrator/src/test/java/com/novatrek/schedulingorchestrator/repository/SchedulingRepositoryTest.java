package com.novatrek.schedulingorchestrator.repository;

import com.novatrek.schedulingorchestrator.entity.ConflictResolutionResult;
import com.novatrek.schedulingorchestrator.entity.GuideAssignment;
import com.novatrek.schedulingorchestrator.entity.ScheduleConflict;
import com.novatrek.schedulingorchestrator.entity.ResolutionOption;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class SchedulingRepositoryTest {

    @Autowired
    private ConflictResolutionResultRepository conflictResolutionResultRepository;

    @Autowired
    private GuideAssignmentRepository guideAssignmentRepository;

    @Autowired
    private ScheduleConflictRepository scheduleConflictRepository;

    @Autowired
    private ResolutionOptionRepository resolutionOptionRepository;

    @Test
    void saveAndFindConflictResolutionResult() {
        ConflictResolutionResult r = new ConflictResolutionResult();
        r.setResolutionStatus(ConflictResolutionResult.ResolutionStatus.RESOLVED);
        r.setAppliedStrategy("REASSIGN_GUIDE");

        ConflictResolutionResult saved = conflictResolutionResultRepository.save(r);
        assertThat(saved.getConflictId()).isNotNull();

        Optional<ConflictResolutionResult> found = conflictResolutionResultRepository.findById(saved.getConflictId());
        assertThat(found).isPresent();
        assertThat(found.get().getResolutionStatus()).isEqualTo(ConflictResolutionResult.ResolutionStatus.RESOLVED);
    }

    @Test
    void saveAndFindGuideAssignment() {
        GuideAssignment g = new GuideAssignment();
        g.setGuideName("Alex Rivers");
        g.setDate(LocalDate.of(2026, 7, 15));
        g.setAssignmentStatus(GuideAssignment.AssignmentStatus.CONFIRMED);

        GuideAssignment saved = guideAssignmentRepository.save(g);
        assertThat(saved.getGuideId()).isNotNull();

        Optional<GuideAssignment> found = guideAssignmentRepository.findById(saved.getGuideId());
        assertThat(found).isPresent();
        assertThat(found.get().getGuideName()).isEqualTo("Alex Rivers");
    }

    @Test
    void saveAndFindScheduleConflict() {
        ScheduleConflict sc = new ScheduleConflict();
        sc.setType(ScheduleConflict.ConflictType.GUIDE_DOUBLE_BOOKED);
        sc.setSeverity(ScheduleConflict.ConflictSeverity.HIGH);
        sc.setDescription("Guide assigned to two trips on same date");
        sc.setConflictDate(LocalDate.of(2026, 8, 1));
        sc.setResolved(false);
        sc.setDetectedAt(OffsetDateTime.now());

        ScheduleConflict saved = scheduleConflictRepository.save(sc);
        assertThat(saved.getId()).isNotNull();

        Optional<ScheduleConflict> found = scheduleConflictRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getType()).isEqualTo(ScheduleConflict.ConflictType.GUIDE_DOUBLE_BOOKED);
    }

    @Test
    void saveAndFindResolutionOption() {
        ResolutionOption ro = new ResolutionOption();
        ro.setStrategy(ResolutionOption.Strategy.REASSIGN_GUIDE);
        ro.setDescription("Assign a different guide to the afternoon trip");
        ro.setImpactAssessment("Low impact");
        ro.setEstimatedAffectedGuests(8);
        ro.setRequiresGuestNotification(false);

        ResolutionOption saved = resolutionOptionRepository.save(ro);
        assertThat(saved.getId()).isNotNull();

        Optional<ResolutionOption> found = resolutionOptionRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getStrategy()).isEqualTo(ResolutionOption.Strategy.REASSIGN_GUIDE);
    }
}
