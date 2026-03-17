package com.novatrek.transportlogistics.repository;

import com.novatrek.transportlogistics.entity.TransportRoute;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface TransportRouteRepository extends JpaRepository<TransportRoute, UUID> {
}
