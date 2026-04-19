<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import SidebarAgriculteur from '@/components /layout/sidebar-agriculteur.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import { useProduitStore } from '@/stores/produit/produit_store'
import { useAuthStore } from '@/stores/auth/auth_store'
import AddProd from '@/components /view/produit/add_prod.vue'
import ProductDetailPopup from '@/components /view/popup/ProductDetailPopup.vue'
import type { Product } from '@/interface/Product'

const { isOpen, openPopup, closePopup } = usePopup()
const detailPopup = usePopup()
const produitStore = useProduitStore()
const authStore = useAuthStore()
const selectedProduct = ref<Product | null>(null)

const openDetail = (prod: Product) => {
  selectedProduct.value = prod
  detailPopup.openPopup()
}

onMounted(async () => {
  if (authStore.user?.id) {
    await produitStore.fetchProduitsAgriculteur(authStore.user.id)
  }
})

const stats = computed(() => {
  const all = produitStore.produits.length
  const publies = produitStore.produits.filter(p => p.statut_publication === 'PUBLIE').length
  const attente = produitStore.produits.filter(p => p.statut_publication === 'EN_ATTENTE').length
  const rejetes = produitStore.produits.filter(p => p.statut_publication === 'REJETE').length

  return [
    { label: 'Total produits', value: all.toString(), trend: '0%', trendUp: true, icon: 'box', color: '#209216' },
    { label: 'Produits publiés', value: publies.toString(), trend: '0%', trendUp: true, icon: 'check', color: '#10b981' },
    { label: 'En attente', value: attente.toString(), trend: '0%', trendUp: false, icon: 'clock', color: '#f59e0b' },
    { label: 'Rejetés', value: rejetes.toString(), trend: '0%', trendUp: true, icon: 'x', color: '#ef4444' }
  ]
})

const searchQuery = ref('')
const activeFilter = ref('Tous')

const filteredProducts = computed(() => {
  return produitStore.produits.filter(p => {
    const matchesSearch = p.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesFilter = activeFilter.value === 'Tous' || 
                         (activeFilter.value === 'Publiés' && p.statut_publication === 'PUBLIE') ||
                         (activeFilter.value === 'Rejetés' && p.statut_publication === 'REJETE') ||
                         (activeFilter.value === 'Ajoutés' && p.statut_publication === 'EN_ATTENTE')
    return matchesSearch && matchesFilter
  })
})

const { currentPage, totalPages, paginatedItems: paginatedProducts, prevPage, nextPage } = usePagination(filteredProducts, 4)

const handleSuccess = async () => {
  closePopup()
  if (authStore.user?.id) {
    await produitStore.fetchProduitsAgriculteur(authStore.user.id)
  }
}

const handleDelete = async (id: string) => {
  if (confirm('Voulez-vous vraiment supprimer ce produit ?')) {
    await produitStore.supprimerProduit(id)
    await produitStore.fetchProduitsAgriculteur(authStore.user!.id)
  }
}
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
                <svg v-if="item.icon === 'box'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                <svg v-else-if="item.icon === 'check'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <svg v-else-if="item.icon === 'clock'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 2m6-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <svg v-else-if="item.icon === 'x'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
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

        <!-- Page Header Action -->
        <div class="page-action-header">
          <h1 class="page-title">Mes produits</h1>
          <button class="add-btn" @click="openPopup">
            + Ajouter produit
          </button>
        </div>

        <!-- Toolbar: Search and Filters -->
        <div class="toolbar">
          <div class="search-box">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input type="text" v-model="searchQuery" placeholder="Rechercher un produit..." class="search-input" @input="currentPage = 1" />
          </div>
          <div class="filter-buttons">
            <button 
              v-for="f in ['Tous', 'Ajoutés', 'Publiés', 'Rejetés']" 
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
          <table class="products-table">
            <thead>
              <tr>
                <th>Produit</th>
                <th>Prix</th>
                <th>Statut</th>
                <th class="actions-col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prod in paginatedProducts" :key="prod.id">
                <td class="product-cell">
                  <div class="p-img">
                    <img :src="prod.photo || '/images/client.png'" :alt="prod.description" />
                  </div>
                  <div class="p-info">
                    <span class="p-name">{{ prod.description }}</span>
                    <span class="p-category">{{ prod.categorie }}</span>
                  </div>
                </td>
                <td class="p-price">{{ prod.prix_unitaire }} FCFA</td>
                <td>
                  <span class="status-badge" :class="prod.statut_publication.toLowerCase().replace('_', '-')">
                    {{ prod.statut_publication }}
                  </span>
                </td>
                <td class="actions-col">
                  <div class="action-icons">
                    <button class="icon-action" aria-label="Voir" @click="openDetail(prod)"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></button>
                    <button class="icon-action" aria-label="Modifier"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></button>
                    <button class="icon-action delete" aria-label="Supprimer" @click="handleDelete(prod.id)"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
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
    
    <!-- Modal d'ajout de produit -->
    <AddProd v-if="isOpen" @close="closePopup" @success="handleSuccess" />

    <!-- Modal de détails du produit -->
    <ProductDetailPopup 
      v-if="detailPopup.isOpen.value && selectedProduct" 
      :product="selectedProduct" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.agriculteur-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 295px; padding: 2.5rem; transition: margin-left 0.3s; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
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

/* Page Header Action */
.page-action-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0; }
.add-btn { background-color: #209216; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 700; cursor: pointer; transition: transform 0.2s; }
.add-btn:hover { transform: scale(1.02); background-color: #1a7a12; }

/* Toolbar */
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; gap: 1.5rem; }
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
.products-table { width: 100%; border-collapse: collapse; }
.products-table th { text-align: left; padding: 1.25rem 1.5rem; background: #f9fafb; font-size: 0.85rem; font-weight: 600; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.products-table td { padding: 1.25rem 1.5rem; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }

.product-cell { display: flex; align-items: center; gap: 1rem; }
.p-img { width: 48px; height: 48px; border-radius: 10px; overflow: hidden; background: #f3f4f6; }
.p-img img { width: 100%; height: 100%; object-fit: cover; }
.p-info { display: flex; flex-direction: column; }
.p-name { font-weight: 700; color: #111827; font-size: 0.95rem; }
.p-category { font-size: 0.75rem; color: #6b7280; font-weight: 500; }
.p-price { font-weight: 600; color: #374151; }

.status-badge { padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.status-badge.publié { background-color: #ecfdf5; color: #059669; }
.status-badge.en-attente { background-color: #fffbeb; color: #d97706; }
.status-badge.rejeté { background-color: #fef2f2; color: #dc2626; }

.actions-col { text-align: right; width: 120px; }
.action-icons { display: flex; gap: 0.5rem; justify-content: flex-end; }
.icon-action { width: 36px; height: 36px; border-radius: 8px; border: none; background: #f3f4f6; color: #6b7280; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }
.icon-action:hover { background: #e5e7eb; color: #111827; }
.icon-action.delete:hover { background-color: #fee2e2; color: #ef4444; }
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
