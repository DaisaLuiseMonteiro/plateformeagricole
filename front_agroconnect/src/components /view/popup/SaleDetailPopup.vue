<script setup lang="ts">
const props = defineProps({
  sale: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}

// Données fictives pour les articles de la vente si non fournis
const items = [
  { name: 'Tomates Bio', qty: '5kg', price: '1200 FCFA', subtotal: '6000 FCFA' },
  { name: 'Oignons Rouges', qty: '2kg', price: '800 FCFA', subtotal: '1600 FCFA' }
]
</script>

<template>
  <div class="popup-overlay" @click.self="closeModal">
    <div class="popup-modal">
      <div class="popup-header">
        <h2 class="popup-title">Détail de la Vente</h2>
        <button class="close-btn" @click="closeModal">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="sale-detail-grid">
        <!-- Left: Sale Summary -->
        <div class="sale-summary-card">
          <div class="summary-header">
            <div class="sale-ref">Réf: {{ sale.id || 'V-2026-001' }}</div>
            <span class="status-pill" :class="sale.status?.toLowerCase().replace(' ', '-')">{{ sale.status }}</span>
          </div>
          
          <div class="total-section">
            <span class="total-label">Montant Total</span>
            <div class="total-value">{{ sale.total || '0' }} FCFA</div>
          </div>

          <div class="detail-rows">
            <div class="detail-row">
              <span class="row-label">Date</span>
              <span class="row-value">{{ sale.date }}</span>
            </div>
            <div class="detail-row">
              <span class="row-label">Mode de paiement</span>
              <span class="row-value">Mobile Money</span>
            </div>
            <div class="detail-row">
              <span class="row-label">Nombre d'articles</span>
              <span class="row-value">{{ sale.itemsCount }}</span>
            </div>
          </div>
        </div>

        <!-- Right: Client & Items -->
        <div class="sale-details-main">
          <div class="section">
            <h3 class="section-title">Acheteur</h3>
            <div class="buyer-info">
              <div class="buyer-avatar">{{ sale.client?.charAt(0) || 'A' }}</div>
              <div class="buyer-meta">
                <div class="buyer-name">{{ sale.client }}</div>
                <div class="buyer-type">Client Particulier</div>
              </div>
            </div>
          </div>

          <div class="section">
            <h3 class="section-title">Articles Vendus</h3>
            <div class="items-table-wrapper">
              <table class="items-table">
                <thead>
                  <tr>
                    <th>Article</th>
                    <th>Qté</th>
                    <th>PU</th>
                    <th class="text-right">Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, idx) in items" :key="idx">
                    <td class="item-name">{{ item.name }}</td>
                    <td>{{ item.qty }}</td>
                    <td>{{ item.price }}</td>
                    <td class="text-right font-bold">{{ item.subtotal }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="popup-footer">
        <button class="btn-print">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="20" height="20">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          Imprimer Facture
        </button>
        <button class="btn-close-action" @click="closeModal">Fermer</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  animation: fadeIn 0.3s ease;
}

.popup-modal {
  background: white;
  border-radius: 28px;
  width: 90%;
  max-width: 850px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.popup-title { font-size: 1.6rem; font-weight: 800; color: #111827; margin: 0; }

.close-btn {
  background: #f3f4f6;
  border: none;
  border-radius: 12px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}
.close-btn:hover { background: #fef2f2; color: #ef4444; transform: rotate(90deg); }

.sale-detail-grid { display: grid; grid-template-columns: 300px 1fr; gap: 2rem; }

.sale-summary-card {
  background: #111827;
  border-radius: 24px;
  padding: 2rem;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.summary-header { display: flex; justify-content: space-between; align-items: flex-start; }
.sale-ref { font-size: 0.85rem; font-weight: 600; color: #9ca3af; }
.status-pill { padding: 0.35rem 0.75rem; border-radius: 20px; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; }
.status-pill.terminée { background: #059669; color: white; }
.status-pill.en-cours { background: #d97706; color: white; }

.total-section { display: flex; flex-direction: column; gap: 0.5rem; }
.total-label { color: #9ca3af; font-size: 0.9rem; font-weight: 600; }
.total-value { font-size: 1.8rem; font-weight: 800; color: #209216; }

.detail-rows { display: flex; flex-direction: column; gap: 1.25rem; }
.detail-row { display: flex; flex-direction: column; gap: 0.25rem; }
.row-label { font-size: 0.75rem; color: #6b7280; font-weight: 700; text-transform: uppercase; }
.row-value { font-size: 0.95rem; font-weight: 600; color: #e5e7eb; }

.section-title { font-size: 1rem; font-weight: 800; color: #111827; margin-bottom: 1.25rem; }

.buyer-info {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 18px;
  border: 1px solid #f3f4f6;
  margin-bottom: 2rem;
}

.buyer-avatar {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #209216;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.25rem;
}

.buyer-name { font-weight: 700; color: #111827; font-size: 1.1rem; }
.buyer-type { font-size: 0.85rem; color: #6b7280; }

.items-table-wrapper { border: 1px solid #f3f4f6; border-radius: 18px; overflow: hidden; }
.items-table { width: 100%; border-collapse: collapse; }
.items-table th { background: #f9fafb; padding: 1rem; text-align: left; font-size: 0.85rem; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.items-table td { padding: 1rem; font-size: 0.95rem; border-bottom: 1px solid #f3f4f6; }
.item-name { font-weight: 700; color: #111827; }
.text-right { text-align: right; }
.font-bold { font-weight: 700; }

.popup-footer {
  margin-top: 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
}

.btn-print {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: white;
  border: 1.5px solid #e5e7eb;
  padding: 0.85rem 1.75rem;
  border-radius: 14px;
  color: #374151;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-print:hover { background: #f9fafb; border-color: #209216; color: #209216; }

.btn-close-action {
  background: #111827;
  color: white;
  border: none;
  padding: 0.85rem 2.5rem;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-close-action:hover { background: #1f2937; transform: translateY(-2px); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(40px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
</style>
