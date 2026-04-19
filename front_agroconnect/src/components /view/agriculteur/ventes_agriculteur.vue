<script setup lang="ts">
import { ref, computed } from 'vue'
import SidebarAgriculteur from '@/components /layout/sidebar-agriculteur.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import SaleDetailPopup from '@/components /view/popup/SaleDetailPopup.vue'
import type { Sale } from '@/interface/Sale'

const detailPopup = usePopup()
const selectedSale = ref<Sale | null>(null)

const openDetail = (sale: Sale) => {
  selectedSale.value = sale
  detailPopup.openPopup()
}

const stats = ref([
  { label: 'Ventes totales', value: '0 FCFA', trend: '+0%', trendUp: true, icon: 'trending', color: '#209216' },
  { label: 'Ventes Fruits', value: '0 FCFA', trend: '+0%', trendUp: true, icon: 'apple', color: '#f43f5e' },
  { label: 'Ventes Légumes', value: '0 FCFA', trend: '+0%', trendUp: true, icon: 'leaf', color: '#10b981' },
  { label: 'Ventes Céréales', value: '0 FCFA', trend: '+0%', trendUp: false, icon: 'wheat', color: '#8b5cf6' }
])

const searchQuery = ref('')
const selectedCategory = ref('Toutes les catégories')

const salesData = ref<Sale[]>([])

const filteredSales = computed(() => {
  return salesData.value.filter(s => {
    const matchesSearch = s.client.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         s.id.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === 'Toutes les catégories' || s.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const { currentPage, totalPages, paginatedItems: paginatedSales, prevPage, nextPage } = usePagination(filteredSales, 3)
</script>

<template>
  <div class="agriculteur-layout">
    <SidebarAgriculteur />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats Grid -->
        <div class="stats-grid">
          <div v-for="item in stats" :key="item.label" class="stat-card">
            <div class="stat-header">
              <span class="stat-label">{{ item.label }}</span>
              <div class="stat-icon-wrapper" :style="{ backgroundColor: item.color + '15', color: item.color }">
                <svg v-if="item.icon === 'trending'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
                <svg v-else-if="item.icon === 'apple'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.084.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.084.477-4.5 1.253" /></svg>
                <svg v-else-if="item.icon === 'leaf'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 016.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" /></svg>
                <svg v-else-if="item.icon === 'wheat'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
              </div>
            </div>
            <div class="stat-value">{{ item.value }}</div>
            <div class="stat-footer">
              <span class="trend" :class="{ 'trend-up': item.trendUp, 'trend-down': !item.trendUp }">
                <svg class="icon-xs" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path v-if="item.trendUp" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 15l7-7 7 7" /><path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7" /></svg>
                {{ item.trend }}
              </span>
              <span class="period">vs mois dernier</span>
            </div>
          </div>
        </div>

        <!-- Page Header -->
        <div class="page-info-header">
          <h1 class="page-title">Mes Ventes</h1>
          <p class="page-description">Suivez l'historique de vos revenus et l'activité de vos clients.</p>
        </div>

        <!-- Toolbar: Search and Buttons Filters -->
        <div class="toolbar">
          <div class="search-box">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input type="text" v-model="searchQuery" placeholder="Rechercher un client ou une réf..." class="search-input" @input="currentPage = 1" />
          </div>
          <div class="filter-buttons">
            <button 
              v-for="cat in ['Toutes les catégories', 'Fruits', 'Légumes', 'Céréales']" 
              :key="cat"
              class="filter-btn"
              :class="{ active: selectedCategory === cat }"
              @click="selectedCategory = cat; currentPage = 1;"
            >
              {{ cat === 'Toutes les catégories' ? 'Tous' : cat }}
            </button>
          </div>
        </div>

        <!-- Sales Card View -->
        <div class="sales-list">
          <div v-for="sale in paginatedSales" :key="sale.id" class="sale-card">
            <div class="sale-main">
              <div class="sale-header">
                <h3 class="sale-title">{{ sale.client }}</h3>
                <span class="status-badge" :class="sale.status.toLowerCase().replace(' ', '-')">{{ sale.status }}</span>
              </div>
              <p class="sale-desc">Commande: <strong>{{ sale.id }}</strong> | Articles: <strong>{{ sale.itemsCount }}</strong></p>
              <div class="sale-meta">
                <span>Date: <strong>{{ sale.date }}</strong></span>
                <span class="sale-total">Total: <strong>{{ sale.total }}</strong></span>
              </div>
            </div>
            <div class="sale-actions">
              <button class="btn-details" @click="openDetail(sale)">
                <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                Détails
              </button>
            </div>
          </div>

          <!-- Pagination -->
          <div class="pagination-wrapper" v-if="totalPages > 1">
            <button class="pag-btn" :disabled="currentPage === 1" @click="prevPage">Précédent</button>
            <div class="pag-numbers">
              <span class="pag-info">Page {{ currentPage }} sur {{ totalPages }}</span>
            </div>
            <button class="pag-btn" :disabled="currentPage === totalPages" @click="nextPage">Suivant</button>
          </div>
        </div>
      </main>
    </div>
    
    <!-- Modal de détails de la vente -->
    <SaleDetailPopup 
      v-if="detailPopup.isOpen.value && selectedSale" 
      :sale="selectedSale" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.agriculteur-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 295px; padding: 2.5rem; transition: margin-left 0.3s; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.stat-card { background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); border: 1px solid #f3f4f6; display: flex; flex-direction: column; }
.stat-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.25rem; }
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

/* Header Info */
.page-info-header { margin-bottom: 2rem; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; }

/* Toolbar */
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; gap: 1rem; }
.search-box { position: relative; flex: 1; max-width: 400px; }
.search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; color: #9ca3af; }
.search-input { width: 100%; padding: 0.75rem 1rem 0.75rem 2.8rem; border-radius: 12px; border: 1px solid #e5e7eb; background: white; outline: none; transition: border-color 0.2s; font-size: 0.95rem; }
.search-input:focus { border-color: #209216; }

.filter-buttons { display: flex; gap: 0.5rem; }
.filter-btn { background: white; border: 1px solid #e5e7eb; padding: 0.6rem 1.25rem; border-radius: 10px; font-weight: 600; color: #6b7280; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.filter-btn:hover { border-color: #209216; color: #209216; }
.filter-btn.active { background-color: #209216; color: white; border-color: #209216; }

/* Sales List (Cards) */
.sales-list { display: flex; flex-direction: column; gap: 1rem; }
.sale-card { background: white; border-radius: 20px; padding: 1.5rem 2rem; border: 1px solid #f3f4f6; display: flex; align-items: center; justify-content: space-between; transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); }
.sale-card:hover { transform: scale(1.005); }

.sale-main { flex: 1; }
.sale-header { display: flex; align-items: center; gap: 1.5rem; margin-bottom: 0.75rem; }
.sale-title { font-size: 1.25rem; font-weight: 800; color: #111827; margin: 0; }
.status-badge { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }
.status-badge.terminée { background: #f0fdf4; color: #16a34a; }
.status-badge.en-cours { background: #fffbeb; color: #d97706; }
.status-badge.annulée { background: #fef2f2; color: #dc2626; }

.sale-desc { color: #6b7280; font-size: 0.95rem; margin-bottom: 0.75rem; }
.sale-meta { display: flex; gap: 2.5rem; font-size: 0.85rem; color: #9ca3af; align-items: center; }
.sale-meta strong { color: #4b5563; }
.sale-total strong { color: #209216; font-size: 1rem; font-weight: 800; }

.btn-details { background: #f3f4f6; color: #4b5563; border: none; padding: 0.65rem 1.5rem; border-radius: 10px; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s; }
.btn-details:hover { background: #e5e7eb; color: #111827; }
.icon-s { width: 18px; height: 18px; }

/* Pagination */
.pagination-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; margin-top: 1rem; }
.pag-btn { background: white; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; color: #4b5563; font-size: 0.9rem; }
.pag-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pag-btn:hover:not(:disabled) { background: #f9fafb; border-color: #d1d5db; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

@media (max-width: 1024px) { 
  .content { margin-left: 80px; }
}
@media (max-width: 900px) {
  .sale-card { flex-direction: column; align-items: flex-start; gap: 1.5rem; }
  .toolbar { flex-direction: column; align-items: stretch; }
  .search-box { max-width: none; }
}
</style>
