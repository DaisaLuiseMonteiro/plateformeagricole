<script setup lang="ts">
import { onMounted, computed, ref } from 'vue';
import Header from '@/components /layout/header.vue';
import { useCommandeStore } from '@/stores/commandes/commande_store';
import { useAuthStore } from '@/stores/auth/auth_store';
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store';
import OrderDetailPopup from '@/components /view/popup/OrderDetailPopup.vue';
import type { Order } from '@/interface/Order';

const commandeStore = useCommandeStore();
const authStore = useAuthStore();
const detailPopup = usePopup();
const selectedOrder = ref<Order | null>(null);

const activeFilter = ref('Tous');
const filters = ['Tous', 'En attente', 'Confirmée', 'Validée', 'Annulée'];

onMounted(async () => {
  if (authStore.user?.id) {
    await commandeStore.fetchCommandesClient(authStore.user.id);
  }
});

const orders = computed(() => commandeStore.orders);

const filteredOrders = computed(() => {
  if (activeFilter.value === 'Tous') return orders.value;
  return orders.value.filter(o => o.statut === activeFilter.value);
});

const { currentPage, totalPages, paginatedItems: paginatedOrders, prevPage, nextPage } = usePagination(filteredOrders, 5);

const orderStats = computed(() => {
  const all = orders.value.length;
  const pending = orders.value.filter(o => o.statut === 'En_attente').length;
  const confirmed = orders.value.filter(o => o.statut === 'confirmée').length;
  const validated = orders.value.filter(o => o.statut === 'validée').length;
  const cancelled = orders.value.filter(o => o.statut === 'annulée').length;

  return [
    { label: 'Total commandes', value: all.toString(), color: '#209216' },
    { label: 'En attente', value: pending.toString(), color: '#f59e0b' },
    { label: 'Confirmées', value: confirmed.toString(), color: '#10b981' },
    { label: 'Annulées', value: cancelled.toString(), color: '#ef4444' }
  ];
});

const getStatusClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'en_attente': return 'status-pending';
    case 'confirmée': return 'status-confirmed';
    case 'validée': return 'status-validated';
    case 'annulée': return 'status-cancelled';
    default: return '';
  }
};

const formatPrice = (value: number) =>
  value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') || '0';

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
};

const openDetail = (order: any) => {
  selectedOrder.value = order;
  detailPopup.openPopup();
};

const handleCancel = async (id: string) => {
  if (confirm('Voulez-vous vraiment annuler cette commande ?')) {
    await commandeStore.rejeterCommande(id);
    if (authStore.user?.id) {
      await commandeStore.fetchCommandesClient(authStore.user.id);
    }
  }
};

const handleValidate = async (id: string) => {
  // Logic to validate receipt of order
};
</script>

<template>
  <Header />

  <main class="orders-main">
    <div class="content-container">
      <!-- Stats Row -->
      <div class="stats-grid">
        <div v-for="stat in orderStats" :key="stat.label" class="stat-card">
          <div class="stat-header">
            <span class="stat-label">{{ stat.label }}</span>
            <div class="stat-icon-wrapper" :style="{ backgroundColor: stat.color + '15', color: stat.color }">
              <svg class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
            </div>
          </div>
          <div class="stat-value">{{ stat.value }}</div>
        </div>
      </div>

      <div class="page-header">
        <h1 class="page-title">Mes Commandes</h1>
        <p class="page-subtitle">Suivez l'état de vos achats et gérez vos livraisons.</p>
      </div>

      <!-- Controls -->
      <div class="controls-section">
        <div class="filter-wrap">
          <button 
            v-for="f in filters" 
            :key="f" 
            class="filter-tab"
            :class="{ active: activeFilter === f }"
            @click="activeFilter = f; currentPage = 1;"
          >{{ f }}</button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="commandeStore.loading" class="loading-state">
        <div class="spinner"></div>
        <p>Chargement de vos commandes...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="orders.length === 0" class="empty-state">
        <div class="empty-icon-box">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
        </div>
        <h3>Aucune commande</h3>
        <p>Vous n'avez pas encore passé de commande sur AgroConnect.</p>
        <router-link to="/" class="shop-btn">Commencer mes achats</router-link>
      </div>

      <!-- Table Section -->
      <div v-else class="table-card">
        <table class="orders-table">
          <thead>
            <tr>
              <th>ID Commande</th>
              <th>Date</th>
              <th>Agriculteur(s)</th>
              <th>Total</th>
              <th>Statut</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in paginatedOrders" :key="order.id">
              <td class="id-cell">#{{ order.id.slice(0, 8) }}</td>
              <td class="date-cell">{{ formatDate(order.date_commande) }}</td>
              <td class="farmer-cell">
                <div class="farmer-info">
                  <span class="farmer-name" v-for="(detail, index) in order.details" :key="detail.id">
                    {{ detail.agriculteur_nom }}{{ index < order.details.length - 1 ? ', ' : '' }}
                  </span>
                </div>
              </td>
              <td class="price-cell">{{ formatPrice(order.montant_commande) }} FCFA</td>
              <td>
                <span class="status-badge" :class="getStatusClass(order.statut)">
                  {{ order.statut }}
                </span>
              </td>
              <td class="actions-col">
                <div class="action-btn-group">
                  <button class="icon-btn view" title="Voir détails" @click="openDetail(order)">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  </button>
                  <button 
                    class="icon-btn validate" 
                    title="Valider la réception" 
                    @click="handleValidate(order.id)"
                    v-if="order.statut === 'confirmée'"
                  >
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                  </button>
                  <button 
                    class="icon-btn delete" 
                    title="Annuler la commande" 
                    @click="handleCancel(order.id)"
                    v-if="order.statut === 'En_attente'"
                  >
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div class="pagination-wrapper" v-if="totalPages > 1">
          <button class="pag-btn" :disabled="currentPage === 1" @click="prevPage">Précédent</button>
          <div class="pag-numbers">
            <span class="pag-info">Page {{ currentPage }} sur {{ totalPages }}</span>
          </div>
          <button class="pag-btn" :disabled="currentPage === totalPages" @click="nextPage">Suivant</button>
        </div>
      </div>
    </div>

    <!-- Detail Popup -->
    <OrderDetailPopup 
      v-if="detailPopup.isOpen.value && selectedOrder" 
      :order="selectedOrder" 
      @close="detailPopup.closePopup" 
    />
  </main>
</template>

<style scoped>
.orders-main {
  padding: 3rem 0;
  background: rgb(238, 247, 241);
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #f3f4f6;
  transition: transform 0.2s;
}

.stat-card:hover { transform: translateY(-5px); }

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.stat-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6b7280;
}

.stat-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-m { width: 22px; height: 22px; }

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
}

/* Page Header */
.page-header { margin-bottom: 2.5rem; }
.page-title { font-size: 2.2rem; font-weight: 800; color: #111827; margin: 0; letter-spacing: -0.5px; }
.page-subtitle { color: #6b7280; margin-top: 0.5rem; font-size: 1.1rem; }

/* Controls */
.controls-section { margin-bottom: 2rem; display: flex; justify-content: flex-end; }
.filter-wrap { display: flex; gap: 0.5rem; background: white; padding: 0.4rem; border-radius: 14px; border: 1px solid #e5e7eb; }
.filter-tab { padding: 0.6rem 1.25rem; border-radius: 10px; border: none; background: transparent; color: #6b7280; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
.filter-tab.active { background: #209216; color: white; box-shadow: 0 4px 10px rgba(32, 146, 22, 0.2); }

/* Table Card */
.table-card {
  background: white;
  border-radius: 24px;
  border: 1px solid #f3f4f6;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.orders-table { width: 100%; border-collapse: collapse; }
.orders-table th { text-align: left; padding: 1.5rem; background: #f9fafb; font-size: 0.85rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
.orders-table td { padding: 1.5rem; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }

.id-cell { font-family: monospace; font-weight: 700; color: #6b7280; }
.date-cell { color: #4b5563; font-weight: 500; }
.farmer-name { font-weight: 600; color: #209216; display: inline-block; }
.price-cell { font-weight: 800; color: #111827; }

.status-badge { padding: 0.5rem 1rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; text-transform: capitalize; }
.status-pending { background: #fffbeb; color: #d97706; }
.status-confirmed { background: #ecfdf5; color: #059669; }
.status-validated { background: #eff6ff; color: #3b82f6; }
.status-cancelled { background: #fef2f2; color: #dc2626; }

/* Actions */
.action-btn-group { display: flex; gap: 0.75rem; }
.icon-btn { width: 40px; height: 40px; border-radius: 12px; border: 1px solid #e5e7eb; background: white; display: flex; align-items: center; justify-content: center; color: #6b7280; cursor: pointer; transition: all 0.2s; }
.icon-btn:hover { background: #f9fafb; border-color: #209216; color: #209216; transform: scale(1.05); }
.icon-btn.delete:hover { background: #fef2f2; border-color: #fecaca; color: #dc2626; }
.icon-btn.validate:hover { background: #ecfdf5; border-color: #a7f3d0; color: #059669; }
.icon-btn svg { width: 20px; height: 20px; }

/* States */
.loading-state, .empty-state { text-align: center; padding: 5rem 2rem; }
.spinner { width: 50px; height: 50px; border: 5px solid #f3f3f3; border-top: 5px solid #209216; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1.5rem; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.empty-icon-box { width: 100px; height: 100px; background: #f3f4f6; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; color: #9ca3af; }
.empty-icon-box svg { width: 50px; height: 50px; }
.empty-state h3 { font-size: 1.5rem; font-weight: 800; color: #111827; margin: 0 0 0.5rem 0; }
.empty-state p { color: #6b7280; margin-bottom: 2rem; }
.shop-btn { background: #209216; color: white; padding: 1rem 2rem; border-radius: 16px; text-decoration: none; font-weight: 700; transition: all 0.3s; display: inline-block; }
.shop-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(32, 146, 22, 0.2); }

/* Pagination */
.pagination-wrapper { display: flex; align-items: center; justify-content: space-between; padding: 1.5rem 2rem; background: #f9fafb; }
.pag-btn { padding: 0.6rem 1.25rem; border-radius: 12px; border: 1px solid #e5e7eb; background: white; color: #4b5563; font-weight: 700; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
.pag-btn:hover:not(:disabled) { border-color: #209216; color: #209216; }
.pag-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pag-info { font-weight: 600; color: #6b7280; }

@media (max-width: 1024px) {
  .content-container { padding: 0 20px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .controls-section { justify-content: center; }
  .orders-table thead { display: none; }
  .orders-table tr { display: flex; flex-direction: column; padding: 1.5rem; border-bottom: 1px solid #f3f4f6; }
  .orders-table td { padding: 0.5rem 0; border: none; }
}
</style>
