package com.novatrek.partnerintegrations.repository;

import com.novatrek.partnerintegrations.entity.Partner;
import com.novatrek.partnerintegrations.entity.PartnerBooking;
import com.novatrek.partnerintegrations.entity.CommissionReport;
import com.novatrek.partnerintegrations.entity.CommissionLineItem;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class PartnerIntegrationsRepositoryTest {

    @Autowired
    private PartnerRepository partnerRepository;

    @Autowired
    private PartnerBookingRepository partnerBookingRepository;

    @Autowired
    private CommissionReportRepository commissionReportRepository;

    @Autowired
    private CommissionLineItemRepository commissionLineItemRepository;

    @Test
    void saveAndFindPartner() {
        Partner p = new Partner();
        p.setName("Mountain Expeditions Ltd");
        p.setType(Partner.PartnerType.TRAVEL_AGENT);
        p.setCommissionRate(new BigDecimal("15.00"));
        p.setStatus(Partner.PartnerStatus.ACTIVE);
        p.setContactEmail("info@mountain-exp.novatrek.example.com");

        Partner saved = partnerRepository.save(p);
        assertThat(saved.getId()).isNotNull();

        Partner found = partnerRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getName()).isEqualTo("Mountain Expeditions Ltd");
        assertThat(found.getType()).isEqualTo(Partner.PartnerType.TRAVEL_AGENT);
    }

    @Test
    void saveAndFindPartnerBooking() {
        PartnerBooking b = new PartnerBooking();
        b.setPartnerId(UUID.randomUUID());
        b.setExternalReference("OTA-REF-12345");
        b.setCommissionRate(new BigDecimal("10.00"));
        b.setBookingTotal(new BigDecimal("599.99"));
        b.setCommissionAmount(new BigDecimal("60.00"));
        b.setStatus(PartnerBooking.BookingStatus.PENDING);
        b.setParticipantCount(4);
        b.setTripDate(LocalDate.of(2026, 7, 15));

        PartnerBooking saved = partnerBookingRepository.save(b);
        assertThat(saved.getId()).isNotNull();

        PartnerBooking found = partnerBookingRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getExternalReference()).isEqualTo("OTA-REF-12345");
        assertThat(found.getBookingTotal()).isEqualByComparingTo(new BigDecimal("599.99"));
    }

    @Test
    void saveAndFindCommissionReport() {
        CommissionReport r = new CommissionReport();
        r.setPeriodStart(LocalDate.of(2026, 1, 1));
        r.setPeriodEnd(LocalDate.of(2026, 3, 31));
        r.setTotalBookings(42);
        r.setTotalRevenue(new BigDecimal("25000.00"));
        r.setTotalCommission(new BigDecimal("2500.00"));

        CommissionReport saved = commissionReportRepository.save(r);
        assertThat(saved.getPartnerId()).isNotNull();

        CommissionReport found = commissionReportRepository.findById(saved.getPartnerId()).orElseThrow();
        assertThat(found.getTotalBookings()).isEqualTo(42);
    }

    @Test
    void saveAndFindCommissionLineItem() {
        CommissionLineItem li = new CommissionLineItem();
        li.setExternalReference("EXT-LI-001");
        li.setTripDate(LocalDate.of(2026, 5, 20));
        li.setBookingTotal(new BigDecimal("350.00"));
        li.setCommissionRate(new BigDecimal("12.00"));
        li.setCommissionAmount(new BigDecimal("42.00"));

        CommissionLineItem saved = commissionLineItemRepository.save(li);
        assertThat(saved.getBookingId()).isNotNull();

        CommissionLineItem found = commissionLineItemRepository.findById(saved.getBookingId()).orElseThrow();
        assertThat(found.getCommissionAmount()).isEqualByComparingTo(new BigDecimal("42.00"));
    }
}
