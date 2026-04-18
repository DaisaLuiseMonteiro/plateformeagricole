<script setup lang="ts">
const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}
</script>

<template>
  <div class="popup-overlay" @click.self="closeModal">
    <div class="popup-modal">
      <div class="popup-header">
        <h2 class="popup-title">Détails de la Commande</h2>
        <button class="close-btn" @click="closeModal">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="detail-content">
        <!-- Order Identification -->
        <div class="order-id-banner">
          <div class="id-info">
            <span class="label">Numéro de Commande</span>
            <h3 class="id-value">#{{ order.id?.slice(0, 8) }}</h3>
          </div>
          <div class="order-status" :class="order.statut?.toLowerCase().replace('_', '-')">
            {{ order.statut }}
          </div>
        </div>

        <div class="info-layout">
          <!-- Left Column: Details -->
          <div class="details-column">
             <div class="section-title">Informations Client</div>
             <div class="client-card">
               <div class="client-avatar">
                 {{ order.client_id?.charAt(0) || 'C' }}
               </div>
               <div class="client-info">
                 <div class="client-name">ID Client: {{ order.client_id }}</div>
                 <div class="client-meta">Commande passée le {{ order.date_commande }}</div>
               </div>
             </div>

             <div class="section-title">Produits Commandés</div>
             <div class="products-list">
               <div v-for="item in order.details" :key="item.id" class="product-item">
                 <div class="p-dot"></div>
                 <div class="p-info">
                   <span class="p-name">Produit ID: {{ item.produit_id }}</span>
                   <span class="p-farmer" v-if="item.agriculteur_nom">Vendu par: <strong>{{ item.agriculteur_nom }}</strong></span>
                 </div>
                 <span class="p-qty">x {{ item.quantite }}</span>
               </div>
               <div v-if="!order.details || order.details.length === 0" class="empty-notif">
                 Aucun détail disponible.
               </div>
             </div>
          </div>

          <!-- Right Column: Summary -->
          <div class="summary-column">
             <div class="section-title">Résumé Financier</div>
             <div class="financial-card">
               <div class="row">
                 <span>Total HT</span>
                 <span>{{ order.montant_commande }} FCFA</span>
               </div>
               <div class="row">
                 <span>Frais de livraison</span>
                 <span>Gratuit</span>
               </div>
               <div class="row total">
                 <span>Total TTC</span>
                 <span>{{ order.montant_commande }} FCFA</span>
               </div>
             </div>

             <div class="section-title">Date de la commande</div>
             <div class="date-box">
               <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="20" height="20">
                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
               </svg>
               <span>{{ order.date_commande }}</span>
             </div>
          </div>
        </div>
      </div>

      <div class="popup-footer">
        <button class="btn-secondary" @click="closeModal">Retour</button>
        <div class="action-btns">
            <!-- Les actions sont gérées par le composant parent (Agriculteur) -->
        </div>
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
  border-radius: 24px;
  width: 90%;
  max-width: 800px;
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

.popup-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

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

.order-id-banner {
  background: #f9fafb;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border: 1px solid #f3f4f6;
}

.label { font-size: 0.85rem; font-weight: 700; color: #9ca3af; text-transform: uppercase; }
.id-value { font-size: 1.5rem; font-weight: 800; color: #111827; margin: 0; }

.order-status {
  padding: 0.6rem 1.25rem;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
}
.order-status.valide { background: #ecfdf5; color: #059669; }
.order-status.en-attente { background: #fffbeb; color: #d97706; }
.order-status.rejeté { background: #fef2f2; color: #dc2626; }

.info-layout { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 2.5rem; }

.section-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.client-card {
  background: #fff;
  border: 1px solid #f3f4f6;
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.client-avatar {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: #209216;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.25rem;
}

.client-name { font-weight: 700; color: #111827; }
.client-meta { font-size: 0.85rem; color: #9ca3af; }

.products-list { display: flex; flex-direction: column; gap: 0.75rem; }
.product-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border-radius: 12px;
}
.p-dot { width: 8px; height: 8px; border-radius: 50%; background: #209216; }
.p-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.p-name { font-weight: 600; color: #374151; }
.p-farmer { font-size: 0.8rem; color: #6b7280; }
.p-farmer strong { color: #209216; }
.p-qty { font-weight: 800; color: #9ca3af; }

.financial-card {
  background: #111827;
  color: white;
  border-radius: 20px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.row { display: flex; justify-content: space-between; font-size: 0.9rem; color: #9ca3af; }
.row.total {
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px dashed rgba(255,255,255,0.2);
  color: white;
  font-weight: 800;
  font-size: 1.1rem;
}

.date-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f3f4f6;
  border-radius: 14px;
  color: #4b5563;
  font-weight: 700;
}

.popup-footer {
  margin-top: 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-secondary { background: #f3f4f6; border: none; padding: 0.85rem 2rem; border-radius: 14px; font-weight: 700; cursor: pointer; }
.action-btns { display: flex; gap: 1rem; }
.btn-approve { background: #209216; color: white; border: none; padding: 0.85rem 2.5rem; border-radius: 14px; font-weight: 700; cursor: pointer; }
.btn-reject { background: #fef2f2; color: #ef4444; border: 1px solid #fecaca; padding: 0.85rem 2.5rem; border-radius: 14px; font-weight: 700; cursor: pointer; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(40px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
</style>
