<script setup lang="ts">
import { ref } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination, usePopup } from '@/stores/utilitaires/utilitaire_store'
import UserDetailPopup from '@/components /view/popup/UserDetailPopup.vue'
import type { User } from '@/interface/User'

const detailPopup = usePopup()
const selectedUser = ref<User | null>(null)

const openDetail = (user: User) => {
  selectedUser.value = user
  detailPopup.openPopup()
}

const userStats = ref([
  { label: 'Nombres inscrits', value: '0', color: '#209216' },
  { label: 'Agriculteurs', value: '0', color: '#3b82f6' },
  { label: 'Clients', value: '0', color: '#f59e0b' },
  { label: 'Inscrits ce mois', value: '0', color: '#8b5cf6' }
])

const users = ref<User[]>([])

const getStatusClass = (user: User) => {
  return user.is_actif ? 'status-active' : 'status-suspended'
}

const getStatusLabel = (user: User) => {
  return user.is_actif ? 'Actif' : 'Suspendu'
}

const { currentPage, totalPages, paginatedItems: paginatedUsers, prevPage, nextPage } = usePagination(users, 5)
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <!-- Stats Grid -->
        <div class="stats-row">
          <div v-for="stat in userStats" :key="stat.label" class="stat-card">
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
            <h1 class="page-title">Gestion des utilisateurs</h1>
            <p class="page-description">Validation des comptes et modération</p>
          </div>
        </div>

        <div class="table-card">
          <div class="search-bar">
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input type="text" placeholder="Rechercher un utilisateur..." />
          </div>

          <table class="user-table">
            <thead>
              <tr>
                <th>Utilisateur</th>
                <th>Rôle</th>
                <th>Statut</th>
                <th>Inscription</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginatedUsers" :key="user.email">
                <td class="user-info">
                  <span class="u-name">{{ user.prenom }} {{ user.nom }}</span>
                  <span class="u-email">{{ user.email }}</span>
                </td>
                <td><span class="role-badge">{{ user.role }}</span></td>
                <td><span class="status-badge" :class="getStatusClass(user)">{{ getStatusLabel(user) }}</span></td>
                <td class="date-cell">N/A</td>
                <td class="text-right">
                  <div class="action-icons">
                    <button class="icon-action view" title="Voir" @click="openDetail(user)">
                      <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                    </button>
                    <button class="icon-action suspend" :title="user.is_actif ? 'Suspendre' : 'Activer'">
                      <svg class="icon-s" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" /></svg>
                    </button>
                  </div>
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
    
    <!-- Modal de détails utilisateur -->
    <UserDetailPopup 
      v-if="detailPopup.isOpen.value && selectedUser" 
      :user="selectedUser" 
      @close="detailPopup.closePopup" 
    />
  </div>
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 275px; padding: 2.5rem; transition: margin-left 0.3s; }

.action-icons { display: flex; gap: 0.5rem; justify-content: flex-end; }
.icon-action { width: 36px; height: 36px; border-radius: 8px; border: none; background: #f3f4f6; color: #6b7280; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }
.icon-action:hover { transform: scale(1.05); background: #e5e7eb; color: #111827; }
.icon-action.suspend:hover { background-color: #fef2f2; color: #dc2626; }
.icon-action.view:hover { background-color: #eff6ff; color: #3b82f6; }
.icon-s { width: 18px; height: 18px; }

.page-title { font-size: 1.75rem; font-weight: 800; color: #111827;  }
.page-description { color: #6b7280; font-size: 0.95rem; margin-top: -1rem;}

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-top: 0; margin-bottom: 0.15rem }
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

/* Table Section */
.table-card { background: white; border-radius: 20px; border: 1px solid #f3f4f6; margin-top: 1rem; overflow: hidden; }
.search-bar { padding: 1.5rem; border-bottom: 1px solid #f3f4f6; position: relative; max-width: 400px; }
.search-icon { position: absolute; left: 2.25rem; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: #9ca3af; }
.search-bar input { width: 100%; background: #f9fafb; border: 1px solid #e5e7eb; padding: 0.65rem 1rem 0.65rem 2.5rem; border-radius: 10px; font-size: 0.9rem; }

.user-table { width: 100%; border-collapse: collapse; }
.user-table th { text-align: left; padding: 1rem 2rem; background: #f9fafb; font-size: 0.8rem; font-weight: 600; color: #6b7280; border-bottom: 1px solid #f3f4f6; }
.user-table td { padding: 1.25rem 2rem; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }

.user-info { display: flex; flex-direction: column; }
.u-name { font-weight: 700; color: #111827; font-size: 0.95rem; }
.u-email { font-size: 0.8rem; color: #9ca3af; }

.role-badge { background: #f0f9ff; color: #0369a1; padding: 0.2rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.status-badge { padding: 0.2rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.status-active { background: #ecfdf5; color: #059669; }
.status-suspended { background: #fef2f2; color: #ef4444; }

.date-cell { color: #6b7280; font-size: 0.9rem; }
.text-right { text-align: right; }
.action-btn-red { background: transparent; border: none; color: #ef4444; cursor: pointer; padding: 0.5rem; border-radius: 50%; transition: background 0.2s; }
.action-btn-red:hover { background: #fef2f2; }
.icon-s { width: 20px; height: 20px; }

/* Pagination */
.pagination-wrapper { display: flex; align-items: center; justify-content: center; gap: 1.5rem; padding: 1.5rem; border-top: 1px solid #f3f4f6; }
.pag-btn { padding: 0.5rem 1.25rem; border-radius: 10px; border: 1px solid #e5e7eb; background: white; color: #4b5563; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.pag-btn:hover:not(:disabled) { background: #209216; color: white; border-color: #209216; }
.pag-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pag-info { font-size: 0.9rem; color: #6b7280; font-weight: 600; }

@media (max-width: 1024px) { .content { margin-left: 80px; } }
</style>
