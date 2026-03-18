package com.novatrek.weather.controller;

import com.novatrek.weather.entity.WeatherAlert;
import com.novatrek.weather.entity.TrailCondition;
import com.novatrek.weather.repository.WeatherAlertRepository;
import com.novatrek.weather.repository.TrailConditionRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({WeatherController.class, TrailConditionsController.class})
@ActiveProfiles("test")
class WeatherControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private WeatherAlertRepository weatherAlertRepository;

    @MockBean
    private TrailConditionRepository trailConditionRepository;

    @Test
    void getCurrentWeather_returnsList() throws Exception {
        when(weatherAlertRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/weather/current"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    @Test
    void getWeatherForecast_returnsList() throws Exception {
        when(weatherAlertRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/weather/forecast"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    @Test
    void getWeatherAlerts_returnsList() throws Exception {
        WeatherAlert alert = new WeatherAlert();
        alert.setTitle("High Wind Warning");
        alert.setAlertType(WeatherAlert.AlertType.HIGH_WIND);
        alert.setSeverity(WeatherAlert.AlertSeverity.WARNING);
        when(weatherAlertRepository.findAll()).thenReturn(List.of(alert));

        mockMvc.perform(get("/weather/alerts"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("High Wind Warning"));
    }

    @Test
    void createWeatherAlert_returns201() throws Exception {
        WeatherAlert saved = new WeatherAlert();
        saved.setId(UUID.randomUUID());
        saved.setTitle("Flash Flood Advisory");
        saved.setAlertType(WeatherAlert.AlertType.FLASH_FLOOD);
        saved.setSeverity(WeatherAlert.AlertSeverity.ADVISORY);
        when(weatherAlertRepository.save(any(WeatherAlert.class))).thenReturn(saved);

        mockMvc.perform(post("/weather/alerts")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\"Flash Flood Advisory\",\"alertType\":\"FLASH_FLOOD\",\"severity\":\"ADVISORY\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.title").value("Flash Flood Advisory"));
    }

    @Test
    void getTrailConditions_returnsList() throws Exception {
        TrailCondition tc = new TrailCondition();
        tc.setTrailName("Eagle Ridge Trail");
        tc.setOverallStatus(TrailCondition.OverallStatus.GOOD);
        tc.setSurfaceCondition(TrailCondition.SurfaceCondition.DRY);
        when(trailConditionRepository.findAll()).thenReturn(List.of(tc));

        mockMvc.perform(get("/trail-conditions"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].trailName").value("Eagle Ridge Trail"));
    }
}
