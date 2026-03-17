package com.novatrek.weather.repository;

import com.novatrek.weather.entity.TrailCondition;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface TrailConditionRepository extends JpaRepository<TrailCondition, UUID> {
}
