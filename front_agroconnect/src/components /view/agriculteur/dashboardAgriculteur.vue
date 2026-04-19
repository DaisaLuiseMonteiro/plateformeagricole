<script setup lang="ts">
import { ref } from 'vue'
import SidebarAgriculteur from '@/components /layout/sidebar-agriculteur.vue'
import Navebar from '@/components /layout/navebar.vue'

const stats = ref([
  { id: 1, label: 'Ventes totales', value: '0', trend: '+0%', trendUp: true, icon: 'cart', color: '#209216' },
  { id: 2, label: 'Produits actifs', value: '0', trend: '+0%', trendUp: true, icon: 'box', color: '#3b82f6' },
  { id: 3, label: 'Revenus', value: '0 FCFA', trend: '+0%', trendUp: true, icon: 'trending', color: '#10b981' },
  { id: 4, label: 'Alertes stock', value: '0', trend: '+0%', trendUp: false, icon: 'alert', color: '#ef4444' }
])

const salesData: number[] = []
const months = ['Jan', 'Féb', 'Mar', 'Avr', 'Mai', 'Juin']

const categoryStats = [
  { label: 'Céréales', value: 0, color: '#8b5cf6' },
  { label: 'Légumes', value: 0, color: '#10b981' },
  { label: 'Fruits', value: 0, color: '#f43f5e' }
]

const recentProducts = ref<{ id: number; name: string; date: string; published: boolean }[]>([])
</script>

<template>
  <div class="agriculteur-layout">
    <SidebarAgriculteur />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats Grid -->
        <div class="stats-grid">
          <div v-for="item in stats" :key="item.id" class="stat-card">
            <div class="stat-header">
              <span class="stat-label">{{ item.label }}</span>
              <div class="stat-icon-wrapper" :style="{ backgroundColor: item.color + '15', color: item.color }">
                <svg v-if="item.icon === 'cart'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                <svg v-else-if="item.icon === 'box'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                <svg v-else-if="item.icon === 'trending'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
                <svg v-else-if="item.icon === 'alert'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
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

        <div class="page-header">
          <h1 class="page-title">Tableau de bord</h1>
          <p class="page-description">Simplifiez la gestion de votre exploitation agricole.</p>
        </div>

        <!-- Dashboard Widgets Grid -->
        <div class="widgets-grid">
          <!-- Evolution des ventes (Curve) -->
          <div class="widget-card">
            <h3 class="widget-title">Évolution des ventes (6 mois)</h3>
            <div class="curve-chart">
              <svg viewBox="0 0 300 100" class="curve-svg">
                <polyline
                  fill="none"
                  stroke="#209216"
                  stroke-width="3"
                  points="0,65 60,58 120,62 180,45 240,52 300,13"
                />
                <!-- Points -->
                <circle cx="0" cy="65" r="4" fill="#209216" />
                <circle cx="60" cy="58" r="4" fill="#209216" />
                <circle cx="120" cy="62" r="4" fill="#209216" />
                <circle cx="180" cy="45" r="4" fill="#209216" />
                <circle cx="240" cy="52" r="4" fill="#209216" />
                <circle cx="300" cy="13" r="4" fill="#209216" />
              </svg>
              <div class="curve-labels">
                <span v-for="m in months" :key="m">{{ m }}</span>
              </div>
            </div>
          </div>

          <!-- Stats par Catégorie (Donut) -->
          <div class="widget-card">
            <h3 class="widget-title">Répartition par Catégorie</h3>
            <div class="donut-box">
              <svg viewBox="0 0 100 100" class="donut-sm">
                <circle r="40" cx="50" cy="50" fill="transparent" stroke="#8b5cf6" stroke-width="12" stroke-dasharray="113 251.3" transform="rotate(-90 50 50)" />
                <circle r="40" cx="50" cy="50" fill="transparent" stroke="#10b981" stroke-width="12" stroke-dasharray="75.4 251.3" stroke-dashoffset="-113" transform="rotate(-90 50 50)" />
                <circle r="40" cx="50" cy="50" fill="transparent" stroke="#f43f5e" stroke-width="12" stroke-dasharray="62.8 251.3" stroke-dashoffset="-188.4" transform="rotate(-90 50 50)" />
                <circle r="30" cx="50" cy="50" fill="white" />
              </svg>
              <div class="donut-legend-v">
                <div v-for="item in categoryStats" :key="item.label" class="leg-row">
                  <span class="leg-dot" :style="{ backgroundColor: item.color }"></span>
                  <span class="leg-txt">{{ item.label }}</span>
                  <span class="leg-val">{{ item.value }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Produits Récents (Table) -->
          <div class="widget-card products-widget">
            <h3 class="widget-title">Produits ajoutés récemment</h3>
            <div class="table-mini-wrap">
              <table class="table-mini">
                <thead>
                  <tr>
                    <th>Produit</th>
                    <th>Ajouté le</th>
                    <th class="center-col">Publié</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="prod in recentProducts" :key="prod.id">
                    <td>{{ prod.name }}</td>
                    <td>{{ prod.date }}</td>
                    <td class="center-col">
                      <div class="status-icon" :class="prod.published ? 'status-ok' : 'status-err'">
                        <svg v-if="prod.published" fill="currentColor" viewBox="0 0 20 20" class="icon-s"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                        <svg v-else fill="currentColor" viewBox="0 0 20 20" class="icon-s"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Alignement sur Design Admin */
.agriculteur-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 295px; padding: 2.5rem; transition: margin-left 0.3s; }

.page-header { margin-bottom: 2rem; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; }

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

/* Widgets Grid */
.widgets-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
.widget-card { background: white; border-radius: 16px; padding: 1.5rem; border: 1px solid #f3f4f6; display: flex; flex-direction: column; height: 320px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); }
.widget-title { font-size: 1rem; font-weight: 700; color: #111827; margin-bottom: 1.5rem; }

/* Curve Chart */
.curve-chart { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.curve-svg { width: 100%; height: 140px; overflow: visible; }
.curve-labels { display: flex; justify-content: space-between; margin-top: 1rem; padding: 0 5px; }
.curve-labels span { font-size: 0.75rem; color: #9ca3af; font-weight: 600; }

/* Donut */
.donut-box { display: flex; flex-direction: column; align-items: center; gap: 1rem; flex: 1; }
.donut-sm { width: 160px; height: 160px; }
.donut-legend-v { width: 100%; display: flex; flex-direction: column; gap: 0.4rem; margin-top: 45px;}
.leg-row { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; }
.leg-dot { width: 8px; height: 8px; border-radius: 50%; }
.leg-txt { flex: 1; color: #4b5563; font-weight: 500; }
.leg-val { font-weight: 700; color: #111827; }

/* Table */
.table-mini-wrap { flex: 1; overflow-y: auto; }
.table-mini { width: 100%; border-collapse: collapse; }
.table-mini th { text-align: left; font-size: 0.75rem; color: #9ca3af; padding-bottom: 0.75rem; border-bottom: 1px solid #f3f4f6; }
.table-mini td { padding: 0.75rem 0; font-size: 0.85rem; color: #111827; font-weight: 600; border-bottom: 1px solid #f3f4f6; }
.center-col { text-align: center !important; }

.status-icon { display: inline-flex; }
.status-ok { color: #10b981; } 
.status-err { color: #ef4444; }
.icon-s { width: 22px; height: 22px; }

@media (max-width: 1200px) { 
  .widgets-grid { grid-template-columns: repeat(2, 1fr); }
  .products-widget { grid-column: span 2; }
}
@media (max-width: 1024px) { 
  .content { margin-left: 80px; } 
}
@media (max-width: 768px) { 
  .widgets-grid { grid-template-columns: 1fr; } 
  .products-widget { grid-column: span 1; }
  .widget-card { height: auto; min-height: 280px; } 
}
</style>