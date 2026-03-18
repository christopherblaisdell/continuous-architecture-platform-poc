package com.novatrek.inventoryprocurement.controller;

import com.novatrek.inventoryprocurement.entity.PurchaseOrder;
import com.novatrek.inventoryprocurement.entity.StockAdjustment;
import com.novatrek.inventoryprocurement.entity.Supplier;
import com.novatrek.inventoryprocurement.repository.PurchaseOrderRepository;
import com.novatrek.inventoryprocurement.repository.StockAdjustmentRepository;
import com.novatrek.inventoryprocurement.repository.SupplierRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({StockLevelsController.class, StockAdjustmentsController.class,
        SuppliersController.class, PurchaseOrdersController.class, ReorderAlertsController.class})
@ActiveProfiles("test")
class InventoryProcurementControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PurchaseOrderRepository purchaseOrderRepository;

    @MockBean
    private StockAdjustmentRepository stockAdjustmentRepository;

    @MockBean
    private SupplierRepository supplierRepository;

    // --- StockLevelsController ---

    @Test
    void getStockLevels_returnsList() throws Exception {
        when(purchaseOrderRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/stock-levels"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }

    // --- StockAdjustmentsController ---

    @Test
    void createStockAdjustment_returns201() throws Exception {
        StockAdjustment adj = new StockAdjustment();
        adj.setId(UUID.randomUUID());
        adj.setItemCategory("climbing_gear");
        adj.setQuantityChange(10);
        adj.setReason("Restocking");
        when(stockAdjustmentRepository.save(any(StockAdjustment.class))).thenReturn(adj);

        mockMvc.perform(post("/stock-adjustments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"itemCategory\":\"climbing_gear\",\"quantityChange\":10,\"reason\":\"Restocking\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.itemCategory").value("climbing_gear"));
    }

    // --- SuppliersController ---

    @Test
    void listSuppliers_returnsList() throws Exception {
        Supplier s = new Supplier();
        s.setName("Alpine Gear Co");
        s.setActive(true);
        when(supplierRepository.findAll()).thenReturn(List.of(s));

        mockMvc.perform(get("/suppliers"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Alpine Gear Co"));
    }

    @Test
    void createSupplier_returns201() throws Exception {
        Supplier s = new Supplier();
        s.setId(UUID.randomUUID());
        s.setName("Summit Supplies");
        s.setLeadTimeDays(7);
        s.setActive(true);
        when(supplierRepository.save(any(Supplier.class))).thenReturn(s);

        mockMvc.perform(post("/suppliers")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Summit Supplies\",\"leadTimeDays\":7,\"active\":true}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Summit Supplies"));
    }

    // --- PurchaseOrdersController ---

    @Test
    void createPurchaseOrder_returns201() throws Exception {
        PurchaseOrder po = new PurchaseOrder();
        po.setId(UUID.randomUUID());
        po.setStatus(PurchaseOrder.PurchaseOrderStatus.DRAFT);
        po.setTotalAmount(new BigDecimal("1500.00"));
        po.setCurrency("USD");
        when(purchaseOrderRepository.save(any(PurchaseOrder.class))).thenReturn(po);

        mockMvc.perform(post("/purchase-orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\":\"DRAFT\",\"totalAmount\":1500.00,\"currency\":\"USD\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.currency").value("USD"));
    }

    @Test
    void getPurchaseOrder_found() throws Exception {
        UUID poId = UUID.randomUUID();
        PurchaseOrder po = new PurchaseOrder();
        po.setId(poId);
        po.setStatus(PurchaseOrder.PurchaseOrderStatus.SUBMITTED);
        po.setTotalAmount(new BigDecimal("2000.00"));
        when(purchaseOrderRepository.findById(poId)).thenReturn(Optional.of(po));

        mockMvc.perform(get("/purchase-orders/{poId}", poId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("SUBMITTED"));
    }

    @Test
    void getPurchaseOrder_notFound() throws Exception {
        UUID poId = UUID.randomUUID();
        when(purchaseOrderRepository.findById(poId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/purchase-orders/{poId}", poId))
                .andExpect(status().isNotFound());
    }

    @Test
    void updatePurchaseOrder_found() throws Exception {
        UUID poId = UUID.randomUUID();
        PurchaseOrder existing = new PurchaseOrder();
        existing.setId(poId);
        existing.setStatus(PurchaseOrder.PurchaseOrderStatus.DRAFT);
        existing.setTotalAmount(new BigDecimal("1500.00"));
        when(purchaseOrderRepository.findById(poId)).thenReturn(Optional.of(existing));
        when(purchaseOrderRepository.save(any(PurchaseOrder.class))).thenReturn(existing);

        mockMvc.perform(patch("/purchase-orders/{poId}", poId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\":\"APPROVED\"}"))
                .andExpect(status().isOk());
    }

    // --- ReorderAlertsController ---

    @Test
    void listReorderAlerts_returnsList() throws Exception {
        when(purchaseOrderRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/reorder-alerts"))
                .andExpect(status().isOk())
                .andExpect(content().json("[]"));
    }
}
