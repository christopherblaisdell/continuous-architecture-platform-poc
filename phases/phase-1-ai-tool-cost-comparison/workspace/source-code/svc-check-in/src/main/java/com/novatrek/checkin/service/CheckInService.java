package com.novatrek.checkin.service;

import com.novatrek.checkin.model.CheckInRecord;
import com.novatrek.checkin.repository.CheckInRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class CheckInService {

    private final CheckInRepository checkInRepository;
    private final AdventureCategoryClassifier categoryClassifier;

    @Transactional
    public CheckInRecord processCheckIn(CheckInRecord request) {
        log.info("Processing check-in for reservation {}", request.getReservationId());

        CheckInRecord.UiPattern uiPattern = categoryClassifier.getUiPattern(
                request.getAdventureCategory(), null);

        request.setCheckInTime(Instant.now());
        request.setUiPattern(uiPattern);
        request.setStatus(CheckInRecord.CheckInStatus.PROCESSING);

        CheckInRecord saved = checkInRepository.save(request);
        saved.setStatus(CheckInRecord.CheckInStatus.COMPLETED);
        return checkInRepository.save(saved);
    }

    public Optional<CheckInRecord> getCheckIn(UUID id) {
        return checkInRepository.findById(id);
    }

    public Optional<CheckInRecord> lookupReservation(String confirmationCode, String lastName) {
        log.info("Looking up reservation: code={}, lastName={}", confirmationCode, lastName);
        return checkInRepository.findByWristbandId(confirmationCode);
    }

    public List<CheckInRecord> getTodayCheckIns(String locationId) {
        Instant startOfDay = LocalDate.now().atStartOfDay(ZoneOffset.UTC).toInstant();
        Instant endOfDay = LocalDate.now().plusDays(1).atStartOfDay(ZoneOffset.UTC).toInstant();
        return checkInRepository.findByLocationIdAndCheckInTimeBetween(
                locationId, startOfDay, endOfDay);
    }
}
