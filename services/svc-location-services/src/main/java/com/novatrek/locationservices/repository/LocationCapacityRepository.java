package com.novatrek.locationservices.repository;

import com.novatrek.locationservices.entity.LocationCapacity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface LocationCapacityRepository extends JpaRepository<LocationCapacity, UUID> {
}
