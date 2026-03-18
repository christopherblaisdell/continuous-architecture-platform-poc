package com.novatrek.emergencyresponse.repository;

import com.novatrek.emergencyresponse.entity.Emergency;
import com.novatrek.emergencyresponse.entity.DispatchRecord;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class EmergencyResponseRepositoryTest {

    @Autowired
    private EmergencyRepository emergencyRepository;

    @Autowired
    private DispatchRecordRepository dispatchRecordRepository;

    @Test
    void saveAndFindEmergency() {
        Emergency e = new Emergency();
        e.setType("medical");
        e.setSeverity("critical");
        e.setStatus("active");
        e.setDescription("Guest injury on Rocky Summit trail");
        e.setReportedBy("Guide-Martinez");

        Emergency saved = emergencyRepository.save(e);
        assertThat(saved.getEmergencyId()).isNotNull();

        Emergency found = emergencyRepository.findById(saved.getEmergencyId()).orElseThrow();
        assertThat(found.getType()).isEqualTo("medical");
        assertThat(found.getReportedBy()).isEqualTo("Guide-Martinez");
    }

    @Test
    void saveAndFindDispatchRecord() {
        DispatchRecord dr = new DispatchRecord();
        dr.setEmergencyId(UUID.randomUUID());
        dr.setRescueTeamId(UUID.randomUUID());
        dr.setPriority("high");
        dr.setStatus(DispatchRecord.Status.dispatched);
        dr.setEtaMinutes(15);

        DispatchRecord saved = dispatchRecordRepository.save(dr);
        assertThat(saved.getDispatchId()).isNotNull();

        DispatchRecord found = dispatchRecordRepository.findById(saved.getDispatchId()).orElseThrow();
        assertThat(found.getStatus()).isEqualTo(DispatchRecord.Status.dispatched);
        assertThat(found.getEtaMinutes()).isEqualTo(15);
    }
}
