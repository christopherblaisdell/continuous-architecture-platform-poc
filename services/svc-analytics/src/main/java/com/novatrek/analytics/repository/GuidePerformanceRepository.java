package com.novatrek.analytics.repository;

import com.novatrek.analytics.entity.GuidePerformance;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GuidePerformanceRepository extends JpaRepository<GuidePerformance, UUID> {
}
