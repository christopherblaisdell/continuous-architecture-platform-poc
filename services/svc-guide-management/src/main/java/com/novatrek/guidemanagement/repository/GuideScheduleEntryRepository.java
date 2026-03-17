package com.novatrek.guidemanagement.repository;

import com.novatrek.guidemanagement.entity.GuideScheduleEntry;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GuideScheduleEntryRepository extends JpaRepository<GuideScheduleEntry, UUID> {
}
