package com.novatrek.weather.controller;

import com.novatrek.weather.entity.WeatherAlert;
import com.novatrek.weather.repository.WeatherAlertRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/weather")
public class WeatherController {

    private final WeatherAlertRepository weatherAlertRepository;

    public WeatherController(WeatherAlertRepository weatherAlertRepository) {
        this.weatherAlertRepository = weatherAlertRepository;
    }

    @GetMapping("/current")
    public List<WeatherAlert> getCurrentWeather() {
        return weatherAlertRepository.findAll();
    }

    @GetMapping("/forecast")
    public List<WeatherAlert> getWeatherForecast() {
        return weatherAlertRepository.findAll();
    }

    @GetMapping("/alerts")
    public List<WeatherAlert> getWeatherAlerts() {
        return weatherAlertRepository.findAll();
    }

    @PostMapping("/alerts")
    public ResponseEntity<WeatherAlert> createWeatherAlert(@Valid @RequestBody WeatherAlert body) {
        WeatherAlert saved = weatherAlertRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}
