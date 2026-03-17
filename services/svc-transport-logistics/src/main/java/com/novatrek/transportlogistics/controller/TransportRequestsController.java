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
@RequestMapping("/transport-requests")
public class TransportRequestsController {

    private final TransportRouteRepository transportRouteRepository;

    public TransportRequestsController(TransportRouteRepository transportRouteRepository) {
        this.transportRouteRepository = transportRouteRepository;
    }

    @PostMapping
    public ResponseEntity<TransportRoute> createTransportRequest(@Valid @RequestBody TransportRoute body) {
        TransportRoute saved = transportRouteRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{requestId}")
    public TransportRoute getTransportRequest(@PathVariable UUID requestId) {
        return transportRouteRepository.findById(requestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "TransportRoute not found"));
    }

}
