package com.novatrek.scheduling.repository;

import com.novatrek.scheduling.model.DailySchedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;
import java.util.UUID;

@Repository
public interface ScheduleRepository extends JpaRepository<DailySchedule, UUID> {

    List<DailySchedule> findByScheduleDateAndLocationId(LocalDate scheduleDate, UUID locationId);

    List<DailySchedule> findByGuideIdAndScheduleDate(UUID guideId, LocalDate scheduleDate);

    @Query("SELECT s FROM DailySchedule s WHERE s.scheduleDate = :date " +
           "AND s.locationId = :locationId " +
           "AND s.startTime < :endTime AND s.endTime > :startTime")
    List<DailySchedule> findConflictingSchedules(
            @Param("date") LocalDate date,
            @Param("locationId") UUID locationId,
            @Param("startTime") LocalTime startTime,
            @Param("endTime") LocalTime endTime);
}
