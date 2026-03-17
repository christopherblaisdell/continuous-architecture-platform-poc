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
@RequestMapping("/purchase-orders")
public class PurchaseOrdersController {

    private final PurchaseOrderRepository purchaseOrderRepository;

    public PurchaseOrdersController(PurchaseOrderRepository purchaseOrderRepository) {
        this.purchaseOrderRepository = purchaseOrderRepository;
    }

    @PostMapping
    public ResponseEntity<PurchaseOrder> createPurchaseOrder(@Valid @RequestBody PurchaseOrder body) {
        PurchaseOrder saved = purchaseOrderRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{poId}")
    public PurchaseOrder getPurchaseOrder(@PathVariable UUID poId) {
        return purchaseOrderRepository.findById(poId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "PurchaseOrder not found"));
    }

    @PatchMapping("/{poId}")
    public PurchaseOrder updatePurchaseOrder(@PathVariable UUID poId, @Valid @RequestBody PurchaseOrder body) {
        PurchaseOrder existing = purchaseOrderRepository.findById(poId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "PurchaseOrder not found"));

        if (body.getSupplierId() != null) existing.setSupplierId(body.getSupplierId());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());
        if (body.getTotalAmount() != null) existing.setTotalAmount(body.getTotalAmount());
        if (body.getCurrency() != null) existing.setCurrency(body.getCurrency());
        if (body.getDeliveryLocationId() != null) existing.setDeliveryLocationId(body.getDeliveryLocationId());
        if (body.getExpectedDeliveryDate() != null) existing.setExpectedDeliveryDate(body.getExpectedDeliveryDate());
        if (body.getNotes() != null) existing.setNotes(body.getNotes());
        if (body.getCreatedBy() != null) existing.setCreatedBy(body.getCreatedBy());

        return purchaseOrderRepository.save(existing);
    }

}
