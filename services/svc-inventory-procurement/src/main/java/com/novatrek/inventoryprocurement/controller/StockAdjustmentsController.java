package com.novatrek.inventoryprocurement.controller;

import com.novatrek.inventoryprocurement.entity.StockAdjustment;
import com.novatrek.inventoryprocurement.repository.StockAdjustmentRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/stock-adjustments")
public class StockAdjustmentsController {

    private final StockAdjustmentRepository stockAdjustmentRepository;

    public StockAdjustmentsController(StockAdjustmentRepository stockAdjustmentRepository) {
        this.stockAdjustmentRepository = stockAdjustmentRepository;
    }

    @PostMapping
    public ResponseEntity<StockAdjustment> createStockAdjustment(@Valid @RequestBody StockAdjustment body) {
        StockAdjustment saved = stockAdjustmentRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}
