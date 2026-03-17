package com.novatrek.inventoryprocurement.controller;

import com.novatrek.inventoryprocurement.entity.Supplier;
import com.novatrek.inventoryprocurement.repository.SupplierRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/suppliers")
public class SuppliersController {

    private final SupplierRepository supplierRepository;

    public SuppliersController(SupplierRepository supplierRepository) {
        this.supplierRepository = supplierRepository;
    }

    @GetMapping
    public List<Supplier> listSuppliers() {
        return supplierRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Supplier> createSupplier(@Valid @RequestBody Supplier body) {
        Supplier saved = supplierRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}
