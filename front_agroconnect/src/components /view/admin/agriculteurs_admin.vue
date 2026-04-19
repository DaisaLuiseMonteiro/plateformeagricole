<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import { useAuthStore } from '@/stores/auth/auth_store'
import UserDetailPopup from '@/components /view/popup/UserDetailPopup.vue'
import type { Agriculteur } from '@/interface/Agriculteur'

const detailPopup = usePopup()
const authStore = useAuthStore()
const selectedFarmer = ref<Agriculteur | null>(null)
const farmersList = ref<Agriculteur[]>([])

const openDetail = (farmer: Agriculteur) => {
  selectedFarmer.value = { ...farmer }
  detailPopup.openPopup()
}

const loadFarmers = async () => {
  try {
    farmersList.value = await authStore.fetchAgriculteurs()
  } catch (err) {
    console.error(err)
  }
}

onMounted(loadFarmers)

const farmerStats = computed(() => {
  const total = farmersList.value.length
  const actifs = farmersList.value.filter(f => f.is_actif).length
  const inactifs = total - actifs

  return [
    { label: 'Agriculteurs total', value: total.toString(), color: '#c38219ff' },
    { label: 'Agriculteurs actifs', value: actifs.toString(), color: '#65d41bff' },
    { label: 'Inactifs', value: inactifs.toString(), color: '#ef4444' },
    { label: 'Inscrits cette semaine', value: 'N/A', color: '#93c2d6ff' }
  ]
})

const searchQuery = ref('')
const activeFilter = ref('Tous')

const filteredFarmers = computed(() => {
  return farmersList.value.filter(f => {
    // f est un AgriculteurModel, donc f.user contient les infos du UserModel
    const fullName = `${f.user?.prenom} ${f.user?.nom}`
    const matchesSearch = fullName.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesFilter = activeFilter.value === 'Tous' || 
                         (activeFilter.value === 'Actif' && f.is_actif) ||
                         (activeFilter.value === 'Inactif' && !f.is_actif)
    return matchesSearch && matchesFilter
  })
})

const { currentPage, totalPages, paginatedItems: paginatedFarmers, prevPage, nextPage } = usePagination(filteredFarmers, 5)

const toggleActivation = async (farmer: any) => {
  const action = farmer.is_actif ? 'désactiver' : 'activer'
  if (confirm(`Voulez-vous vraiment ${action} cet agriculteur ?`)) {
    try {
      if (farmer.is_actif) {
        await authStore.desactiverAgriculteur(farmer.id)
      } else {
        await authStore.validerAgriculteur(farmer.id)
      }
      await loadFarmers()
    } catch (err) {
      alert("Erreur lors de l'opération")
    }
  }
}
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats -->
        <div class="stats-row">
          <div v-for="stat in farmerStats" :key="stat.label" class="stat-card">
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
          <h1 class="page-title">Agriculteurs</h1>
        </div>

        <div class="main-card">
          <div class="controls-row">
            <div class="search-box">
              <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <input type="text" placeholder="Rechercher un agriculteur..." />
            </div>
            <div class="filter-btns">
              <button class="f-btn">Inactif</button>
              <button class="f-btn active">Actif</button>
            </div>
          </div>

          <table class="farmer-table">
            <thead>
              <tr>
                <th>Agriculteur</th>
                <th>Inscrit le</th>
                <th>Statut</th>
                <th>Commandes</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="f in paginatedFarmers" :key="f.id">
                <td class="f-name">{{ f.user?.prenom }} {{ f.user?.nom }}</td>
                <td class="f-date">N/A</td>
                <td>
                  <span class="badge" :class="f.is_actif ? 'badge-green' : 'badge-red'">{{ f.is_actif ? 'Actif' : 'Inactif' }}</span>
                </td>
                <td class="f-orders">--</td>
                <td class="actions-row">
                  <button class="i-btn" :title="f.is_actif ? 'Désactiver' : 'Activer'" @click="toggleActivation(f)">
                    <svg v-if="f.is_actif" class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" /></svg>
                    <svg v-else class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </button>
                  <button class="details-btn-small" @click="openDetail(f)">Détails</button>
                </td>
              </tr>
            </tbody>
          </table>

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
    
    <!-- Modal de détails de l'agriculteur -->
    <UserDetailPopup 
      v-if="detailPopup.isOpen.value && selectedFarmer" 
      :user="selectedFarmer" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 275px; padding: 2.5rem; transition: margin-left 0.3s; }

.page-title { font-size: 1.75rem; font-weight: 800; color: #111827; }

/* Stats Mini */
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

/* Main Card Table */
.main-card { background: white; border-radius: 20px; border: 1px solid #f3f4f6; margin-top: 2rem; overflow: hidden; }
.controls-row { padding: 1.5rem; border-bottom: 1px solid #f3f4f6; display: flex; align-items: center; justify-content: space-between; }
.search-box { position: relative; max-width: 320px; flex: 1; }
.icon-s { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: #9ca3af; }
.search-box input { width: 100%; background: #f9fafb; border: 1px solid #e5e7eb; padding: 0.65rem 1rem 0.65rem 2.6rem; border-radius: 10px; font-size: 0.9rem; }

.filter-btns { display: flex; gap: 0.5rem; }
.f-btn { padding: 0.5rem 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb; background: white; color: #4b5563; font-weight: 600; font-size: 0.85rem; cursor: pointer; }
.f-btn.active { background: #209216; color: white; border-color: #209216; }

.farmer-table { width: 100%; border-collapse: collapse; }
.farmer-table th { text-align: left; padding: 1rem 2rem; background: #f9fafb; font-size: 0.8rem; font-weight: 600; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.farmer-table td { padding: 1.25rem 2rem; border-bottom: 1px solid #f3f4f6; font-size: 0.95rem; vertical-align: middle; }

.f-name { font-weight: 700; color: #111827; }
.f-date { color: #9ca3af; font-size: 0.9rem; }
.f-orders { font-weight: 700; color: #4b5563; }

.badge { padding: 0.2rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
.badge-green { background: #ecfdf5; color: #059669; }
.badge-red { background: #fef2f2; color: #ef4444; }

.actions-row { display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; }
.i-btn { width: 34px; height: 34px; border-radius: 50%; border: 1px solid #e5e7eb; background: white; display: flex; align-items: center; justify-content: center; color: #6b7280; cursor: pointer; transition: all 0.2s; }
.i-btn:hover { border-color: #209216; color: #209216; background: #ecfdf5; }

.details-btn-small { background: white; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.details-btn-small:hover { border-color: #209216; color: #209216; }

/* Pagination */
.pagination-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-top: 1px solid #f3f4f6; }
.pag-btn { background: white; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; color: #4b5563; }
.pag-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pag-btn:hover:not(:disabled) { background: #f9fafb; color: #111827; border-color: #d1d5db; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

@media (max-width: 1024px) { .content { margin-left: 80px; } }
@media (max-width: 800px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }
</style>
