package com.novatrek.reviews.repository;

import com.novatrek.reviews.entity.RatingSummary;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface RatingSummaryRepository extends JpaRepository<RatingSummary, UUID> {
}
