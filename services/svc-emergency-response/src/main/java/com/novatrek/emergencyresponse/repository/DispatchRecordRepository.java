package com.novatrek.emergencyresponse.repository;

import com.novatrek.emergencyresponse.entity.DispatchRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface DispatchRecordRepository extends JpaRepository<DispatchRecord, UUID> {
}
