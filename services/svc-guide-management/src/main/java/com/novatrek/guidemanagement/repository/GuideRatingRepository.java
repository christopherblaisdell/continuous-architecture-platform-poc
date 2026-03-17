package com.novatrek.guidemanagement.repository;

import com.novatrek.guidemanagement.entity.GuideRating;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GuideRatingRepository extends JpaRepository<GuideRating, UUID> {
}
