package com.novatrek.inventoryprocurement.repository;

import com.novatrek.inventoryprocurement.entity.PurchaseOrder;
import com.novatrek.inventoryprocurement.entity.StockAdjustment;
import com.novatrek.inventoryprocurement.entity.Supplier;
import com.novatrek.inventoryprocurement.entity.ReorderAlert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class InventoryProcurementRepositoryTest {

    @Autowired
    private PurchaseOrderRepository purchaseOrderRepository;

    @Autowired
    private StockAdjustmentRepository stockAdjustmentRepository;

    @Autowired
    private SupplierRepository supplierRepository;

    @Test
    void saveAndFindSupplier() {
        Supplier s = new Supplier();
        s.setName("Mountain Gear Inc");
        s.setLeadTimeDays(14);
        s.setRating(new BigDecimal("4.50"));
        s.setActive(true);

        Supplier saved = supplierRepository.save(s);
        assertThat(saved.getId()).isNotNull();

        Supplier found = supplierRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getName()).isEqualTo("Mountain Gear Inc");
        assertThat(found.getLeadTimeDays()).isEqualTo(14);
    }

    @Test
    void saveAndFindPurchaseOrder() {
        PurchaseOrder po = new PurchaseOrder();
        po.setSupplierId(UUID.randomUUID());
        po.setStatus(PurchaseOrder.PurchaseOrderStatus.DRAFT);
        po.setTotalAmount(new BigDecimal("5000.00"));
        po.setCurrency("USD");
        po.setExpectedDeliveryDate(LocalDate.of(2026, 8, 1));
        po.setNotes("Urgent summer stock");

        PurchaseOrder saved = purchaseOrderRepository.save(po);
        assertThat(saved.getId()).isNotNull();

        PurchaseOrder found = purchaseOrderRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getStatus()).isEqualTo(PurchaseOrder.PurchaseOrderStatus.DRAFT);
        assertThat(found.getTotalAmount()).isEqualByComparingTo(new BigDecimal("5000.00"));
    }

    @Test
    void saveAndFindStockAdjustment() {
        StockAdjustment adj = new StockAdjustment();
        adj.setItemCategory("helmets");
        adj.setQuantityChange(-3);
        adj.setReason("Damaged items removed");

        StockAdjustment saved = stockAdjustmentRepository.save(adj);
        assertThat(saved.getId()).isNotNull();

        StockAdjustment found = stockAdjustmentRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getItemCategory()).isEqualTo("helmets");
        assertThat(found.getQuantityChange()).isEqualTo(-3);
    }
}
