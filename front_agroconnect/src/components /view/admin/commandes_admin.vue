<script setup lang="ts">
import { ref, computed } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import OrderDetailPopup from '@/components /view/popup/OrderDetailPopup.vue'
import type { Order } from '@/interface/Order'

const detailPopup = usePopup()
const selectedOrder = ref<Order | null>(null)

const openDetail = (order: Order) => {
  selectedOrder.value = order
  detailPopup.openPopup()
}

const orderStats = ref([
  { label: 'Commandes totales', value: '0', color: '#209216' },
  { label: 'Commandes en attente', value: '0', color: '#f59e0b' },
  { label: 'Commandes rejetées', value: '0', color: '#ef4444' },
  { label: 'Commande par production', value: '0', color: '#3b82f6' }
])

const activeFilter = ref('Tous')
const filters = ['Tous', 'En cours', 'Validée', 'En attente', 'Livrée']

const orders = ref<Order[]>([])

const getStatusClass = (status: string) => {
  if (status === 'En cours') return 'status-ongoing'
  if (status === 'Validée') return 'status-validated'
  if (status === 'En attente') return 'status-pending'
  if (status === 'Livrée') return 'status-delivered'
  return ''
}

const filteredOrders = computed(() => {
  if (activeFilter.value === 'Tous') return orders.value
  return orders.value.filter(o => o.statut === activeFilter.value)
})

const { currentPage, totalPages, paginatedItems: paginatedOrders, prevPage, nextPage } = usePagination(filteredOrders, 3)
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats Mini Cards -->
        <div class="order-stats-grid">
          <div v-for="stat in orderStats" :key="stat.label" class="stat-card">
            <div class="stat-header">
              <span class="stat-label">{{ stat.label }}</span>
              <div class="stat-icon-wrapper" :style="{ backgroundColor: stat.color + '15', color: stat.color }">
                <svg class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
              </div>
            </div>
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-footer">
              <span class="trend trend-up">
                <svg class="icon-xs" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 15l7-7 7 7" /></svg>
                +12.5%
              </span>
              <span class="period">vs mois dernier</span>
            </div>
          </div>
        </div>

        <div class="page-header">
          <div>
            <h1 class="page-title">Commandes</h1>
            <p class="page-description">Suivi de production par commande</p>
          </div>
        </div>

        <!-- Search & Filters -->
        <div class="controls-section">
          <div class="search-wrap">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input type="text" placeholder="Rechercher..." />
          </div>
          <div class="filter-wrap">
            <button 
              v-for="f in filters" 
              :key="f" 
              class="filter-tab"
              :class="{ active: activeFilter === f }"
              @click="activeFilter = f"
            >{{ f }}</button>
          </div>
        </div>

        <!-- Orders List -->
        <div class="orders-cards-list">
          <div v-for="order in paginatedOrders" :key="order.id" class="order-item-card">
            <div class="order-card-left">
              <div class="order-top-meta">
                <span class="order-id">{{ order.id }}</span>
                <span class="status-badge" :class="getStatusClass(order.statut)">{{ order.statut }}</span>
              </div>
              <h2 class="order-location">{{ order.date_commande }}</h2>
              <p class="order-details-txt">{{ order.details.length }} articles - {{ order.montant_commande }} CFA</p>
            </div>
            
            <div class="order-card-right">
              <div class="production-tracking">
                <div class="tracking-labels">
                  <span class="track-label">Production</span>
                  <span class="track-val">100%</span>
                </div>
                <div class="progress-bar-bg">
                  <div class="progress-bar-fill" :style="{ width: '100%' }"></div>
                </div>
              </div>
              <button class="details-btn" @click="openDetail(order)">
                <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                Détails
              </button>
            </div>
          </div>
        </div>

        <div class="pagination-wrapper" v-if="totalPages > 1">
          <button class="pag-btn" :disabled="currentPage === 1" @click="prevPage">Précédent</button>
          <div class="pag-numbers">
            <span class="pag-info">Page {{ currentPage }} sur {{ totalPages }}</span>
          </div>
          <button class="pag-btn" :disabled="currentPage === totalPages" @click="nextPage">Suivant</button>
        </div>
      </main>
    </div>
    
    <!-- Modal de détails de la commande -->
    <OrderDetailPopup 
      v-if="detailPopup.isOpen.value && selectedOrder" 
      :order="selectedOrder" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; overflow-x: hidden; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-bottom: 2.5rem; margin-left: 275px; padding: 2.5rem; transition: margin-left 0.3s; }

.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 0.5rem; }
.page-title { font-size: 1.75rem; font-weight: 800; color: #111827; margin: 0; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.45rem; }

/* Controls Section */
.controls-section { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem; }
.search-wrap { flex: 1; max-width: 320px; position: relative; }
.search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: #9ca3af; }
.search-wrap input { width: 100%; background: white; border: 1px solid #e5e7eb; padding: 0.65rem 1rem 0.65rem 2.6rem; border-radius: 10px; font-size: 0.9rem; }

.filter-wrap { display: flex; gap: 0.5rem; }
.filter-tab { padding: 0.6rem 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb; background: white; color: #4b5563; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
.filter-tab.active { background: #209216; color: white; border-color: #209216; }

/* Stats Grid */
.order-stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 0; margin-bottom: 1.5rem; }
.stat-card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); border: 1px solid #f3f4f6; }
.stat-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.75rem; }
.stat-label { font-size: 0.9rem; font-weight: 600; color: #6b7280; }
.stat-icon-wrapper { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.icon-m { width: 22px; height: 22px; }
.stat-value { font-size: 2rem; font-weight: 800; color: #111827; line-height: 1; }
.stat-footer { display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem; }
.trend { display: flex; align-items: center; gap: 0.2rem; font-size: 0.85rem; font-weight: 700; padding: 2px 8px; border-radius: 20px; }
.trend-up { color: #059669; background-color: #ecfdf5; }
.trend-down { color: #dc2626; background-color: #fef2f2; }
.icon-xs { width: 14px; height: 14px; }
.period { font-size: 0.85rem; color: #9ca3af; }

/* Orders List */
.orders-cards-list { margin-top: 2rem; display: flex; flex-direction: column; gap: 1rem; }
.order-item-card { background: white; border-radius: 20px; padding: 1.5rem 2rem; border: 1px solid #f3f4f6; display: flex; align-items: center; justify-content: space-between; transition: transform 0.2s; }
.order-item-card:hover { transform: scale(1.005); border-color: #20921640; }

.order-top-meta { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; }
.order-id { font-size: 0.85rem; color: #9ca3af; font-family: monospace; font-weight: 600; }
.status-badge { padding: 0.2rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
.status-ongoing { background: #eff6ff; color: #3b82f6; }
.status-validated { background: #ecfdf5; color: #059669; }
.status-pending { background: #fff7ed; color: #f59e0b; }
.status-delivered { background: #f0fdf4; color: #10b981; }

.order-location { font-size: 1.25rem; font-weight: 800; color: #111827; margin: 0; }
.order-details-txt { font-size: 0.95rem; color: #6b7280; margin-top: 0.25rem; }

.order-card-right { display: flex; align-items: center; gap: 2.5rem; }
.production-tracking { width: 180px; }
.tracking-labels { display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.8rem; font-weight: 600; }
.track-label { color: #9ca3af; }
.track-val { color: #111827; }

.progress-bar-bg { width: 100%; height: 8px; background: #f3f4f6; border-radius: 4px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: #209216; border-radius: 4px; transition: width 0.5s ease; }

.details-btn { border: 1px solid #e5e7eb; background: white; color: #111827; padding: 0.6rem 1.25rem; border-radius: 12px; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s; }
.details-btn:hover { background: #f9fafb; border-color: #d1d5db; }
.icon-s { width: 18px; height: 18px; }

@media (max-width: 1200px) {
  .order-card-right { gap: 1rem; }
  .order-stats-grid { grid-template-columns: repeat(2, 1fr); }
}

/* Pagination */
.pagination-wrapper { display: flex; align-items: center; justify-content: center; gap: 1.5rem; padding: 1.25rem; margin-top: 2rem; background: white; border-radius: 16px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.pag-btn { padding: 0.5rem 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb; background: white; color: #4b5563; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.pag-btn:hover:not(:disabled) { background: #209216; color: white; border-color: #209216; }
.pag-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 600; }

@media (max-width: 1024px) { 
  .content { margin-left: 80px; } 
  .order-stats-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .order-item-card { flex-direction: column; align-items: flex-start; gap: 1.5rem; }
  .order-card-right { width: 100%; justify-content: space-between; }
  .production-tracking { width: 60%; }
}
</style>
