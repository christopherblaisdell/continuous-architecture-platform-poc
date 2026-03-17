package com.novatrek.inventoryprocurement.repository;

import com.novatrek.inventoryprocurement.entity.ReorderAlert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ReorderAlertRepository extends JpaRepository<ReorderAlert, UUID> {
}
