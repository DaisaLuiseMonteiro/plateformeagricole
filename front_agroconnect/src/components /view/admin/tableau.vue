<script setup lang="ts">
import { ref } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'

const stats = ref([
  { id: 1, label: 'Commandes totales', value: '1,248', trend: '+12.5%', trendUp: true, icon: 'cart', color: '#209216' },
  { id: 2, label: 'Produits actifs', value: '356', trend: '+4.2%', trendUp: true, icon: 'box', color: '#3b82f6' },
  { id: 3, label: 'Agriculteurs', value: '89', trend: '+8.1%', trendUp: true, icon: 'users', color: '#8b5cf6' },
  { id: 4, label: 'Revenus (FCFA)', value: '12.4M', trend: '-2.3%', trendUp: false, icon: 'chart', color: '#ef4444' }
])

const orderBars = [
  { label: 'Validées', value: 160, color: '#209216' },
  { label: 'En attente', value: 90, color: '#f59e0b' },
  { label: 'Rejetées', value: 40, color: '#ef4444' }
]

const categoryStats = [
  { label: 'Fruits', value: 40, color: '#f43f5e' },
  { label: 'Céréales', value: 35, color: '#8b5cf6' },
  { label: 'Légumes', value: 25, color: '#10b981' }
]

const recentUsers = ref([
  { name: 'Moussa Sow', email: 'moussa@email.com' },
  { name: 'Fatou Diop', email: 'fatou@email.com' },
  { name: 'Ibrahima Fall', email: 'ibra@email.com' },
  { name: 'Awa Ndiaye', email: 'awa@email.com' },
  { name: 'Samba Kane', email: 'samba@email.com' },
  { name: 'Binta Tall', email: 'binta@email.com' },
  { name: 'Ousmane Sy', email: 'ousmane@email.com' },
  { name: 'Mariam Ba', email: 'mariam@email.com' },
  { name: 'Modou Faye', email: 'modou@email.com' },
  { name: 'Yacine Gaye', email: 'yacine@email.com' }
])
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
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
                <svg v-else-if="item.icon === 'users'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                <svg v-else-if="item.icon === 'chart'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
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
          <p class="page-description">Vue d'ensemble de votre plateforme agricole</p>
        </div>

        <!-- Dashboard Widgets Grid -->
        <div class="widgets-grid">
          <!-- Col 1: Detail Commande (Bar Chart) -->
          <div class="widget-card">
            <h3 class="widget-title">Détail des Commandes</h3>
            <div class="bar-chart-v">
              <div v-for="bar in orderBars" :key="bar.label" class="bar-v-item">
                <div class="bar-v-fill" :style="{ height: bar.value + 'px', backgroundColor: bar.color }"></div>
                <span class="bar-v-label">{{ bar.label }}</span>
              </div>
            </div>
          </div>

          <!-- Col 2: Stats Catégorie (Donut) -->
          <div class="widget-card">
            <h3 class="widget-title">Stats par Catégorie</h3>
            <div class="donut-box">
              <svg viewBox="0 0 100 100" class="donut-sm">
                <circle r="40" cx="50" cy="50" fill="transparent" stroke="#f43f5e" stroke-width="12" stroke-dasharray="100.5 251.3" transform="rotate(-90 50 50)" />
                <circle r="40" cx="50" cy="50" fill="transparent" stroke="#8b5cf6" stroke-width="12" stroke-dasharray="88 251.3" stroke-dashoffset="-100.5" transform="rotate(-90 50 50)" />
                <circle r="40" cx="50" cy="50" fill="transparent" stroke="#10b981" stroke-width="12" stroke-dasharray="62.8 251.3" stroke-dashoffset="-188.5" transform="rotate(-90 50 50)" />
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

          <!-- Col 3: Utilisateurs Récents (Table) -->
          <div class="widget-card">
            <h3 class="widget-title">Utilisateurs récents</h3>
            <div class="table-mini-wrap">
              <table class="table-mini">
                <thead>
                  <tr>
                    <th>Utilisateur</th>
                    <th>Email</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in recentUsers" :key="user.email">
                    <td>{{ user.name }}</td>
                    <td class="email-td">{{ user.email }}</td>
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
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 275px; padding: 2.5rem; transition: margin-left 0.3s; }

.page-title { font-size: 1.75rem; font-weight: 800; color: #111827; margin: 0; }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 0; margin-bottom: 2.5rem; }
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

/* Widgets Grid */
.widgets-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 2.5rem; }
.widget-card { background: white; border-radius: 16px; padding: 1.5rem; border: 1px solid #f3f4f6; display: flex; flex-direction: column; height: 320px; }
.widget-title { font-size: 1rem; font-weight: 700; color: #111827; margin-bottom: 1.5rem; }

/* Bar Chart Vertical */
.bar-chart-v { display: flex; align-items: flex-end; justify-content: center; gap: 2rem; height: 100%; padding-bottom: 1rem; }
.bar-v-item { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; width: 65px; }
.bar-v-fill { width: 100%; border-radius: 4px; transition: height 0.5s; }
.bar-v-label { font-size: 0.75rem; color: #6b7280; font-weight: 600; white-space: nowrap; }

/* Donut */
.donut-box { display: flex; flex-direction: column; align-items: center; gap: 1.5rem; flex: 1; margin-top: 1.5rem; }
.donut-sm { width: 150px; height: 150px; }
.donut-legend-v { width: 100%; display: flex; flex-direction: column; gap: 0.5rem; }
.leg-row { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; }
.leg-dot { width: 8px; height: 8px; border-radius: 50%; }
.leg-txt { flex: 1; color: #4b5563; font-weight: 500; }
.leg-val { font-weight: 700; color: #111827; }

/* Mini Table */
.table-mini-wrap { flex: 1; overflow-y: auto; }
.table-mini { width: 100%; border-collapse: collapse; }
.table-mini th { text-align: left; font-size: 0.75rem; color: #9ca3af; padding-bottom: 0.5rem; border-bottom: 1px solid #f3f4f6; }
.table-mini td { padding: 0.5rem 0; font-size: 0.85rem; color: #111827; font-weight: 500; border-bottom: 1px solid #f3f4f6; }
.email-td { color: #6b7280 !important; font-size: 0.75rem !important; }

@media (max-width: 1200px) { .widgets-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 1024px) { .content { margin-left: 80px; } }
@media (max-width: 768px) { .widgets-grid { grid-template-columns: 1fr; } .widget-card { height: auto; min-height: 250px; } }
</style>
e>