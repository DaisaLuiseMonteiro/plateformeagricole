<script setup lang="ts">
import { ref } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import ProductDetailPopup from '@/components /view/popup/ProductDetailPopup.vue'
import type { Product } from '@/interface/Product'

const detailPopup = usePopup()
const selectedProduct = ref<Product | null>(null)

const openDetail = (prod: Product) => {
  selectedProduct.value = prod
  detailPopup.openPopup()
}

const productStats = ref([
  { label: 'Tous les produits', value: '0', icon: 'box', color: '#209216' },
  { label: 'Produits publiés', value: '0', icon: 'check', color: '#3b82f6' },
  { label: 'Produits rejetés', value: '0', icon: 'x', color: '#ef4444' },
  { label: 'Stocks finis', value: '0', icon: 'alert', color: '#f59e0b' }
])

const activeFilter = ref('Tous')
const filters = ['Tous', 'Légumes', 'Céréales', 'Fruits']

const products = ref<Product[]>([])

const getStatusClass = (quantity: number) => {
  if (quantity > 10) return 'status-active'
  if (quantity > 0) return 'status-low'
  return 'status-out'
}

const getStatusLabel = (quantity: number) => {
  if (quantity > 10) return 'Disponible'
  if (quantity > 0) return 'Stock faible'
  return 'Rupture'
}

const { currentPage, totalPages, paginatedItems: paginatedProducts, prevPage, nextPage } = usePagination(products, 5)
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats Row -->
        <div class="stats-row">
          <div v-for="stat in productStats" :key="stat.label" class="stat-card">
            <div class="stat-header">
              <span class="stat-label">{{ stat.label }}</span>
              <div class="stat-icon-wrapper" :style="{ backgroundColor: stat.color + '15', color: stat.color }">
                <svg v-if="stat.icon === 'box'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                <svg v-else-if="stat.icon === 'check'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                <svg v-else-if="stat.icon === 'x'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                <svg v-else-if="stat.icon === 'alert'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
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
            <h1 class="page-title">Produits</h1>
            <p class="page-description">{{ products.length }} produits enregistrés</p>
          </div>
        </div>

        <div class="table-container">
          <!-- Filters & Search -->
          <div class="controls-row">
            <div class="search-box">
              <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <input type="text" placeholder="Rechercher un produit..." />
            </div>
            <div class="filter-group">
              <button 
                v-for="f in filters" 
                :key="f" 
                class="filter-btn" 
                :class="{ active: activeFilter === f }"
                @click="activeFilter = f"
              >{{ f }}</button>
            </div>
          </div>

          <!-- Table -->
          <table class="products-table">
            <thead>
              <tr>
                <th>Produit</th>
                <th>Catégorie</th>
                <th>Prix</th>
                <th>Stock</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in paginatedProducts" :key="product.id">
                <td class="name-cell">{{ product.name }}</td>
                <td class="cat-cell">{{ product.categorie }}</td>
                <td class="price-cell">{{ product.prix_unitaire }} CFA</td>
                <td class="stock-cell">{{ product.quantite_stock }}</td>
                <td>
                  <span class="status-badge" :class="getStatusClass(product.quantite_stock)">{{ getStatusLabel(product.quantite_stock) }}</span>
                </td>
                <td class="actions-cell">
                  <button class="icon-btn view-btn" title="Voir" @click="openDetail(product)"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></button>
                  <button class="icon-btn edit-btn" title="Modifier"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></button>
                  <button class="icon-btn delete-btn" title="Supprimer"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination Controls -->
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
    
    <!-- Modal de détails du produit -->
    <ProductDetailPopup 
      v-if="detailPopup.isOpen.value && selectedProduct" 
      :product="selectedProduct" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; overflow-x: hidden; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 275px; padding: 2.5rem; transition: margin-left 0.3s; }

.page-header { display: flex; align-items: center; justify-content: space-between; }
.page-title { font-size: 1.75rem; font-weight: 800; color: #111827; margin: 0; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; }

.add-btn { background: #209216; color: white; border: none; padding: 0.75rem 1.25rem; border-radius: 12px; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: background 0.2s; }
.add-btn:hover { background: #1a7a12; }
.icon-s { width: 18px; height: 18px; }

/* Stats Row */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 0; margin-bottom: 1rem; }
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

/* Table Container */
.table-container {background:white; border-radius: 20px; border: 1px solid #f3f4f6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; }

.controls-row { padding: 1.5rem; border-bottom: 1px solid #f3f4f6; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; }
.search-box { flex: 1; max-width: 400px; position: relative; }
.search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; color: #9ca3af; }
.search-box input { width: 100%; background: #f9fafb; border: 1px solid #e5e7eb; padding: 0.75rem 1rem 0.75rem 2.8rem; border-radius: 12px; font-family: inherit; font-size: 0.95rem; }
.search-box input:focus { outline: none; border-color: #209216; background: white; }

.filter-group { display: flex; gap: 0.5rem; }
.filter-btn { padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid #e5e7eb; background: white; color: #4b5563; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
.filter-btn.active { background: #209216; color: white; border-color: #209216; }
.filter-btn:hover:not(.active) { background: #f3f4f6; }

/* Products Table */
.products-table { width: 100%; border-collapse: collapse; }
.products-table th { text-align: left; padding: 1rem 1.5rem; background: #f9fafb; font-size: 0.85rem; font-weight: 600; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.products-table td { padding: 1.25rem 1.5rem; border-bottom: 1px solid #f3f4f6; font-size: 0.95rem; vertical-align: middle; }

.name-cell { font-weight: 700; color: #111827; }
.cat-cell { color: #9ca3af; }
.price-cell { color: #111827; font-weight: 500; }
.stock-cell { font-family: monospace; font-weight: 600; color: #4b5563; }

.status-badge { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.status-active { background: #ecfdf5; color: #059669; }
.status-out { background: #fef2f2; color: #dc2626; }
.status-low { background: #fffbeb; color: #d97706; }

.actions-cell { display: flex; gap: 0.75rem; }
.icon-btn { width: 32px; height: 32px; border-radius: 8px; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.icon-btn svg { width: 18px; height: 18px; }

.view-btn { color: #6b7280; }
.view-btn:hover { background: #f3f4f6; color: #111827; }
.edit-btn { color: #3b82f6; }
.edit-btn:hover { background: #eff6ff; }
.delete-btn { color: #ef4444; }
.delete-btn:hover { background: #fef2f2; }

/* Pagination */
.pagination-wrapper { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-top: 1px solid #f3f4f6; }
.pag-btn { background: white; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; color: #4b5563; }
.pag-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pag-btn:hover:not(:disabled) { background: #f9fafb; color: #111827; border-color: #d1d5db; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

@media (max-width: 1024px) { 
  .content { margin-left: 80px; } 
}

@media (max-width: 768px) {
  .controls-row { flex-direction: column; align-items: stretch; }
  .products-table th:nth-child(2), .products-table td:nth-child(2) { display: none; }
}
</style>
