<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import SidebarAgriculteur from '@/components /layout/sidebar-agriculteur.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import { useCommandeStore } from '@/stores/commandes/commande_store'
import { useAuthStore } from '@/stores/auth/auth_store'
import OrderDetailPopup from '@/components /view/popup/OrderDetailPopup.vue'

const detailPopup = usePopup()
const commandeStore = useCommandeStore()
const authStore = useAuthStore()
const selectedOrder = ref(null)

const openDetail = (order: any) => {
  selectedOrder.value = order
  detailPopup.openPopup()
}

onMounted(async () => {
  if (authStore.user?.id) {
    await commandeStore.fetchCommandesAgriculteur(authStore.user.id)
  }
})

const stats = computed(() => {
  const all = commandeStore.orders.length
  const valides = commandeStore.orders.filter(o => o.statut === 'confirmée').length
  const attente = commandeStore.orders.filter(o => o.statut === 'En_attente').length
  const rejetees = commandeStore.orders.filter(o => o.statut === 'annulée').length

  return [
    { label: 'Commandes totales', value: all.toString(), trend: '+0%', trendUp: true, icon: 'shopping-cart', color: '#209216' },
    { label: 'Commandes confirmées', value: valides.toString(), trend: '+0%', trendUp: true, icon: 'check-circle', color: '#10b981' },
    { label: 'En attente', value: attente.toString(), trend: '0%', trendUp: false, icon: 'clock', color: '#f59e0b' },
    { label: 'Commandes rejetées', value: rejetees.toString(), trend: '0%', trendUp: true, icon: 'x-circle', color: '#ef4444' }
  ]
})

const searchQuery = ref('')
const activeFilter = ref('Tous')

const filteredOrders = computed(() => {
  return commandeStore.orders.filter(o => {
    // Les produits sont dans o.details
    const productNames = o.details?.map(d => d.produit_id).join(' ') || ''
    const matchesSearch = productNames.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesFilter = activeFilter.value === 'Tous' || 
                         (activeFilter.value === 'Valides' && o.statut === 'confirmée') ||
                         (activeFilter.value === 'Rejetées' && o.statut === 'annulée') ||
                         (activeFilter.value === 'Attente' && o.statut === 'En_attente')
    return matchesSearch && matchesFilter
  })
})

const { currentPage, totalPages, paginatedItems: paginatedOrders, prevPage, nextPage } = usePagination(filteredOrders, 5)

const handleConfirm = async (id: string) => {
  if (confirm('Voulez-vous confirmer cette commande ?')) {
    await commandeStore.confirmerCommande(id)
    await commandeStore.fetchCommandesAgriculteur(authStore.user!.id)
  }
}

const handleReject = async (id: string) => {
  if (confirm('Voulez-vous rejeter cette commande ?')) {
    await commandeStore.rejeterCommande(id)
    await commandeStore.fetchCommandesAgriculteur(authStore.user!.id)
  }
}

const formatPrice = (value: number) =>
  value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') || '0'
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
                <svg v-if="item.icon === 'shopping-cart'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                <svg v-else-if="item.icon === 'check-circle'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <svg v-else-if="item.icon === 'clock'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 2m6-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <svg v-else-if="item.icon === 'x-circle'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
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

        <!-- Breadcrumb / Title -->
        <div class="page-info-header">
          <h1 class="page-title">Mes Commandes</h1>
          <p class="page-description">Gérez les demandes de vos clients et suivez leur statut.</p>
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
          <div class="search-box">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input type="text" v-model="searchQuery" placeholder="Rechercher des produits..." class="search-input" @input="currentPage = 1" />
          </div>
          <div class="filter-buttons">
            <button 
              v-for="f in ['Tous', 'Attente', 'Valides', 'Rejetées']" 
              :key="f"
              class="filter-btn"
              :class="{ active: activeFilter === f }"
              @click="activeFilter = f; currentPage = 1;"
            >
              {{ f }}
            </button>
          </div>
        </div>

        <!-- Table Content -->
        <div class="table-card">
          <table class="orders-table">
            <thead>
              <tr>
                <th>Produit(s)</th>
                <th>Date commande</th>
                <th>Statut</th>
                <th>Montant</th>
                <th class="actions-col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in paginatedOrders" :key="order.id">
                <td class="products-cell">
                  <div class="p-list-text">{{ order.details?.length || 0 }} article(s)</div>
                </td>
                <td class="date-cell">{{ order.date_commande }}</td>
                <td>
                  <span class="status-badge" :class="order.statut.toLowerCase().replace('é', 'e').replace('_', '-')">
                    {{ order.statut }}
                  </span>
                </td>
                <td class="amount-cell">{{ formatPrice(order.montant_commande) }} FCFA</td>
                <td class="actions-col">
                  <div class="action-icons">
                    <button class="icon-action approve" title="Valider" @click="handleConfirm(order.id)" v-if="order.statut === 'En_attente'"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg></button>
                    <button class="icon-action reject" title="Rejeter" @click="handleReject(order.id)" v-if="order.statut === 'En_attente'"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg></button>
                    <button class="icon-action view" title="Voir détail" @click="openDetail(order)"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></button>
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
      </main>
    </div>
    
    <!-- Modal de détails de la commande -->
    <OrderDetailPopup 
      v-if="detailPopup.isOpen.value" 
      :order="selectedOrder" 
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
.stat-value { font-size: 2rem; font-weight: 800; color: #111827; line-height: 1; margin-bottom: 0.5rem; }

.stat-footer { display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem; }
.trend { display: flex; align-items: center; gap: 0.2rem; font-size: 0.85rem; font-weight: 700; padding: 2px 8px; border-radius: 20px; }
.trend-up { color: #059669; background-color: #ecfdf5; }
.trend-down { color: #dc2626; background-color: #fef2f2; }
.icon-xs { width: 14px; height: 14px; }
.period { font-size: 0.85rem; color: #9ca3af; }

/* Header Info */
.page-info-header { margin-bottom: 0.5rem; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; }

/* Toolbar */
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; gap: 1rem; }
.search-box { position: relative; flex: 1; max-width: 400px; }
.search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; color: #9ca3af; }
.search-input { width: 100%; padding: 0.75rem 1rem 0.75rem 2.8rem; border-radius: 12px; border: 1px solid #e5e7eb; background: white; outline: none; transition: border-color 0.2s; font-size: 0.95rem; }
.search-input:focus { border-color: #209216; }

.filter-buttons { display: flex; gap: 0.5rem; }
.filter-btn { background: white; border: 1px solid #e5e7eb; padding: 0.6rem 1.25rem; border-radius: 10px; font-weight: 600; color: #6b7280; cursor: pointer; transition: all 0.2s; }
.filter-btn:hover { border-color: #209216; color: #209216; }
.filter-btn.active { background-color: #209216; color: white; border-color: #209216; }

/* Table */
.table-card { background: white; border-radius: 16px; border: 1px solid #f3f4f6; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); }
.orders-table { width: 100%; border-collapse: collapse; }
.orders-table th { text-align: left; padding: 1.25rem 1.5rem; background: #f9fafb; font-size: 0.85rem; font-weight: 600; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.orders-table td { padding: 1.25rem 1.5rem; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }

.products-cell { max-width: 300px; }
.p-list-text { font-weight: 600; color: #111827; font-size: 0.95rem; line-height: 1.4; }
.date-cell { color: #6b7280; font-size: 0.9rem; }
.amount-cell { font-weight: 700; color: #111827; }

.status-badge { padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.status-badge.validee { background-color: #ecfdf5; color: #059669; }
.status-badge.en-attente { background-color: #fffbeb; color: #d97706; }
.status-badge.rejetee { background-color: #fef2f2; color: #dc2626; }

.actions-col { text-align: right; width: 150px; }
.action-icons { display: flex; gap: 0.5rem; justify-content: flex-end; }
.icon-action { width: 36px; height: 36px; border-radius: 8px; border: none; background: #f3f4f6; color: #6b7280; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }
.icon-action:hover { transform: scale(1.05); background: #e5e7eb; color: #111827; }
.icon-action.approve:hover { background-color: #ecfdf5; color: #059669; }
.icon-action.reject:hover { background-color: #fef2f2; color: #dc2626; }
.icon-action.view:hover { background-color: #eff6ff; color: #3b82f6; }
.icon-action svg { width: 18px; height: 18px; }

/* Pagination */
.pagination-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-top: 1px solid #f3f4f6; }
.pag-btn { background: white; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; color: #4b5563; font-size: 0.9rem; }
.pag-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pag-btn:hover:not(:disabled) { background: #f9fafb; border-color: #d1d5db; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

@media (max-width: 1024px) { 
  .content { margin-left: 80px; }
  .toolbar { flex-direction: column; align-items: stretch; }
  .search-box { max-width: none; }
}
</style>
