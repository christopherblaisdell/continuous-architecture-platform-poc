package com.novatrek.transportlogistics.controller;

import com.novatrek.transportlogistics.entity.Vehicle;
import com.novatrek.transportlogistics.repository.VehicleRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/vehicles")
public class VehiclesController {

    private final VehicleRepository vehicleRepository;

    public VehiclesController(VehicleRepository vehicleRepository) {
        this.vehicleRepository = vehicleRepository;
    }

    @GetMapping
    public List<Vehicle> listVehicles() {
        return vehicleRepository.findAll();
    }

    @PatchMapping("/{vehicleId}")
    public Vehicle updateVehicle(@PathVariable UUID vehicleId, @Valid @RequestBody Vehicle body) {
        Vehicle existing = vehicleRepository.findById(vehicleId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Vehicle not found"));

        if (body.getType() != null) existing.setType(body.getType());
        if (body.getCapacity() != null) existing.setCapacity(body.getCapacity());
        if (body.getLicensePlate() != null) existing.setLicensePlate(body.getLicensePlate());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());
        if (body.getAssignedLocationId() != null) existing.setAssignedLocationId(body.getAssignedLocationId());
        if (body.getMileage() != null) existing.setMileage(body.getMileage());
        if (body.getLastMaintenanceDate() != null) existing.setLastMaintenanceDate(body.getLastMaintenanceDate());
        if (body.getNextMaintenanceDate() != null) existing.setNextMaintenanceDate(body.getNextMaintenanceDate());

        return vehicleRepository.save(existing);
    }

}
