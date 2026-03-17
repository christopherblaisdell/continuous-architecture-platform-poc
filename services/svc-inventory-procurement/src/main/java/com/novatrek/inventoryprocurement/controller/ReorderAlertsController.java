package com.novatrek.inventoryprocurement.controller;

import com.novatrek.inventoryprocurement.entity.PurchaseOrder;
import com.novatrek.inventoryprocurement.repository.PurchaseOrderRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/reorder-alerts")
public class ReorderAlertsController {

    private final PurchaseOrderRepository purchaseOrderRepository;

    public ReorderAlertsController(PurchaseOrderRepository purchaseOrderRepository) {
        this.purchaseOrderRepository = purchaseOrderRepository;
    }

    @GetMapping
    public List<PurchaseOrder> listReorderAlerts() {
        return purchaseOrderRepository.findAll();
    }

}
