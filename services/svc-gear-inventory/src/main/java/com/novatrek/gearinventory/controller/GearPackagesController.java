package com.novatrek.gearinventory.controller;

import com.novatrek.gearinventory.entity.GearPackage;
import com.novatrek.gearinventory.repository.GearPackageRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/gear-packages")
public class GearPackagesController {

    private final GearPackageRepository gearPackageRepository;

    public GearPackagesController(GearPackageRepository gearPackageRepository) {
        this.gearPackageRepository = gearPackageRepository;
    }

    @GetMapping
    public List<GearPackage> listGearPackages() {
        return gearPackageRepository.findAll();
    }

    @GetMapping("/{package_id}")
    public List<GearPackage> getGearPackage() {
        return gearPackageRepository.findAll();
    }

}
