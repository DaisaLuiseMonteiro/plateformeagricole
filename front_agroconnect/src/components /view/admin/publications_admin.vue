<script setup lang="ts">
import { ref } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import ProductDetailPopup from '@/components /view/popup/ProductDetailPopup.vue'
import type { Product } from '@/interface/Product'

const detailPopup = usePopup()
const selectedPub = ref<Product | null>(null)

const openDetail = (pub: any) => {
  // Mapper les champs de publication vers le format attendu par ProductDetailPopup
  selectedPub.value = {
    id: pub.id.toString(),
    name: pub.title,
    photo: '', // pas d'image dans le mock actuel
    prix_unitaire: 0,
    quantite_stock: parseInt(pub.quantity.replace(/[^0-9]/g, '')),
    categorie: 'Production',
    description: pub.description,
    agriculteur_id: ''
  } as Product
  detailPopup.openPopup()
}

const pubStats = ref([
  { label: 'Total publication', value: '0', color: '#209216' },
  { label: 'Publications validées', value: '0', color: '#3b82f6' },
  { label: 'En attentes', value: '0', color: '#f59e0b' },
  { label: 'Publication rejets', value: '0', color: '#ef4444' }
])

const publications = ref([])

const { currentPage, totalPages, paginatedItems: paginatedPublications, prevPage, nextPage } = usePagination(publications, 4)
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats -->
        <div class="stats-row">
          <div v-for="stat in pubStats" :key="stat.label" class="stat-card">
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
            <h1 class="page-title">Demandes de publication</h1>
            <p class="page-description">Validez les publications et relancez les agriculteurs</p>
          </div>
          <div class="filter-dropdown">
            <button class="filter-btn-main">
              <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" /></svg>
              Filtrer par statut
              <svg class="icon-xs" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
            </button>
            <div class="dropdown-content">
              <span>Validée</span>
              <span>Rejetée</span>
              <span>En attente</span>
            </div>
          </div>
        </div>

        <!-- Publications List -->
        <div class="pub-list">
          <div v-for="pub in paginatedPublications" :key="pub.id" class="pub-card">
            <div class="pub-main">
              <div class="pub-header">
                <h3 class="pub-title">{{ pub.title }}</h3>
                <span class="badge-pending">{{ pub.status }}</span>
              </div>
              <p class="pub-desc">{{ pub.description }}</p>
              <div class="pub-meta">
                <span>Agriculteur: <strong>{{ pub.farmer }}</strong></span>
                <span>Quantité: <strong>{{ pub.quantity }}</strong></span>
                <span>{{ pub.date }}</span>
              </div>
            </div>
            <div class="pub-actions">
              <button class="btn-details-action" @click="openDetail(pub)">
                <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                Détails
              </button>
              <button class="btn-approve">
                <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                Valider
              </button>
              <button class="btn-reject">
                <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                Rejeter
              </button>
            </div>
          </div>

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
    
    <!-- Modal de détails de la publication -->
    <ProductDetailPopup 
      v-if="detailPopup.isOpen.value && selectedPub" 
      :product="selectedPub" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 275px; padding: 2.5rem; transition: margin-left 0.3s; }

.btn-details-action { background: #f3f4f6; color: #4b5563; border: none; padding: 0.65rem 1.25rem; border-radius: 10px; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s; }
.btn-details-action:hover { background: #e5e7eb; color: #111827; }

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 2rem; }
.page-title { font-size: 1.75rem; font-weight: 800; color: #111827; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; }

/* Filter Dropdown */
.filter-dropdown { position: relative; }
.filter-btn-main { background: white; border: 1px solid #e5e7eb; padding: 0.6rem 1.25rem; border-radius: 12px; font-weight: 600; color: #4b5563; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.dropdown-content { position: absolute; right: 0; top: 110%; background: white; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); width: 160px; display: none; z-index: 10; }
.dropdown-content span { display: block; padding: 0.75rem 1rem; font-size: 0.9rem; color: #111827; font-weight: 500; cursor: pointer; }
.dropdown-content span:hover { background: #f9fafb; color: #209216; }
.filter-dropdown:hover .dropdown-content { display: block; }
.icon-s { width: 18px; height: 18px; }
.icon-xs { width: 14px; height: 14px; }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 0; margin-bottom: 2.5rem; }
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

/* Pub List */
.pub-list { display: flex; flex-direction: column; gap: 1rem; }
.pub-card { background: white; border-radius: 20px; padding: 1.5rem 2rem; border: 1px solid #f3f4f6; display: flex; align-items: center; justify-content: space-between; transition: transform 0.2s; }
.pub-card:hover { transform: scale(1.005); }

.pub-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem; }
.pub-title { font-size: 1.25rem; font-weight: 800; color: #111827; margin: 0; }
.badge-pending { background: #fff7ed; color: #f59e0b; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }

.pub-desc { color: #6b7280; font-size: 0.95rem; margin-bottom: 1rem; }
.pub-meta { display: flex; gap: 1.5rem; font-size: 0.85rem; color: #9ca3af; }
.pub-meta strong { color: #4b5563; }

.pub-actions { display: flex; gap: 0.75rem; }
.btn-approve { background: #209216; color: white; border: none; padding: 0.65rem 1.5rem; border-radius: 10px; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.btn-reject { background: white; color: #ef4444; border: 1px solid #e5e7eb; padding: 0.65rem 1.5rem; border-radius: 10px; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }

/* Pagination */
.pagination-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; margin-top: 0.5rem; }
.pag-btn { background: white; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; color: #4b5563; }
.pag-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pag-btn:hover:not(:disabled) { background: #f9fafb; color: #111827; border-color: #d1d5db; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

@media (max-width: 1024px) { .content { margin-left: 80px; } }
@media (max-width: 900px) { .pub-card { flex-direction: column; align-items: flex-start; gap: 1.5rem; } .stats-row { grid-template-columns: repeat(2, 1fr); } }
</style>
