package com.novatrek.transportlogistics.controller;

import com.novatrek.transportlogistics.entity.TransportRoute;
import com.novatrek.transportlogistics.repository.TransportRouteRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/routes")
public class RoutesController {

    private final TransportRouteRepository transportRouteRepository;

    public RoutesController(TransportRouteRepository transportRouteRepository) {
        this.transportRouteRepository = transportRouteRepository;
    }

    @GetMapping
    public List<TransportRoute> listRoutes() {
        return transportRouteRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<TransportRoute> createRoute(@Valid @RequestBody TransportRoute body) {
        TransportRoute saved = transportRouteRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{routeId}/schedule")
    public TransportRoute getRouteSchedule(@PathVariable UUID routeId) {
        return transportRouteRepository.findById(routeId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "TransportRoute not found"));
    }

}
