<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
import { usePagination } from '@/stores/utilitaires/utilitaire_store'
import { useNotificationStore } from '@/stores/utilitaires/notification_store'

const notificationStore = useNotificationStore()
const isProcessingAction = ref<string | null>(null)

onMounted(async () => {
  await notificationStore.fetchNotifications()
})

const unreadCount = computed(() => notificationStore.notifications.filter(n => !n.est_lue).length)

const {
  currentPage,
  totalPages,
  paginatedItems: notifications,
  prevPage,
  nextPage,
  goToPage
} = usePagination(computed(() => notificationStore.notifications), 6)

const toggleRead = (notif: any) => {
  if (!notif.est_lue) {
    notificationStore.markAsRead(notif.id)
  }
}

const handleAction = async (notif: any, action: 'publier' | 'rejeter') => {
  isProcessingAction.value = notif.id
  const success = await notificationStore.performAction(notif, action)
  if (success) {
    alert(`Le produit a été ${action === 'publier' ? 'publié' : 'rejeté'} avec succès.`)
  } else {
    alert('Erreur lors de l\'action.')
  }
  isProcessingAction.value = null
  await notificationStore.fetchNotifications()
}

const markAllAsRead = async () => {
  await notificationStore.markAsRead()
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('fr-FR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

const getColor = (type: string) => {
  if (type === 'action_required') return '#3b82f6'
  return '#209216'
}
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <div class="page-header">
          <div>
            <h1 class="page-title">Notifications Admin</h1>
            <p class="unread-status">{{ unreadCount }} non lue(s)</p>
          </div>
          <button class="mark-read-btn" @click="markAllAsRead">
            Tout marquer comme lu
          </button>
        </div>

        <div v-if="notifications.length === 0" class="empty-state">
          <p>Aucune notification administrative.</p>
        </div>

        <div class="notifications-list">
          <div 
            v-for="notif in notifications" 
            :key="notif.id" 
            class="notification-card"
            :class="{ unread: !notif.est_lue, 'action-required': notif.type === 'action_required' }"
            @click="toggleRead(notif)"
          >
            <div class="notif-icon-section">
              <div class="icon-circle" :style="{ backgroundColor: getColor(notif.type) + '15', color: getColor(notif.type) }">
                <svg v-if="notif.type === 'action_required'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                <svg v-else class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
            </div>
            
            <div class="notif-content">
              <div class="notif-header">
                <h3 class="notif-title">{{ notif.titre }}</h3>
                <span v-if="notif.type === 'action_required'" class="action-badge">Validation requise</span>
              </div>
              <p class="notif-desc">{{ notif.message }}</p>
              
              <!-- Boutons d'action pour l'admin -->
              <div v-if="notif.type === 'action_required' && notif.data?.type === 'product_validation'" class="action-buttons" @click.stop>
                <button 
                  class="btn-publish" 
                  :disabled="isProcessingAction === notif.id"
                  @click="handleAction(notif, 'publier')"
                >
                  Publier
                </button>
                <button 
                  class="btn-reject" 
                  :disabled="isProcessingAction === notif.id"
                  @click="handleAction(notif, 'rejeter')"
                >
                  Rejeter
                </button>
              </div>

              <span class="notif-time">{{ formatDate(notif.date_creation) }}</span>
            </div>

            <div class="notif-status-section">
              <div v-if="!notif.est_lue" class="unread-dot"></div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-container">
          <div class="pagination-wrapper">
            <button class="pagin-btn" :disabled="currentPage === 1" @click="prevPage">
              Précédent
            </button>
            <div class="pages-list">
              <button 
                v-for="page in totalPages" 
                :key="page" 
                class="page-btn"
                :class="{ active: page === currentPage }"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>
            </div>
            <button class="pagin-btn" :disabled="currentPage === totalPages" @click="nextPage">
              Suivant
            </button>
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

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 2rem; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0; }
.unread-status { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; font-weight: 500; }

.mark-read-btn { background: white; border: 1px solid #e5e7eb; padding: 0.6rem 1.25rem; border-radius: 12px; font-weight: 600; color: #374151; cursor: pointer; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.mark-read-btn:hover { background: #f9fafb; border-color: #d1d5db; }

.notifications-list { display: flex; flex-direction: column; gap: 0.75rem; }
.notification-card { background: white; border-radius: 16px; padding: 1.25rem 1.5rem; display: flex; align-items: flex-start; gap: 1.25rem; border: 1px solid #f3f4f6; transition: all 0.2s; cursor: pointer; position: relative; }
.notification-card:hover { border-color: #20921640; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transform: translateY(-1px); }
.notification-card.unread { border-left: 4px solid #3b82f6; background: #eff6ff; }
.notification-card.action-required { border-left: 4px solid #f59e0b; background: #fffbeb; }

.notif-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.25rem; }
.action-badge { background: #fef3c7; color: #92400e; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 4px; text-transform: uppercase; }

.notif-icon-section { flex-shrink: 0; padding-top: 0.25rem; }
.icon-circle { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.icon-m { width: 22px; height: 22px; }

.notif-content { flex: 1; }
.notif-title { font-size: 1.05rem; font-weight: 700; color: #111827; margin: 0; }
.notif-desc { color: #4b5563; font-size: 0.95rem; margin: 0.35rem 0; line-height: 1.5; }
.notif-time { font-size: 0.85rem; color: #9ca3af; font-weight: 500; display: block; margin-top: 0.75rem; }

.action-buttons { display: flex; gap: 0.75rem; margin-top: 1rem; }
.action-buttons button { padding: 0.5rem 1rem; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.btn-publish { background: #209216; color: white; border: none; }
.btn-publish:hover { background: #1a7a12; transform: translateY(-1px); }
.btn-reject { background: #ef4444; color: white; border: none; }
.btn-reject:hover { background: #dc2626; transform: translateY(-1px); }

.notif-status-section { width: 20px; display: flex; justify-content: center; padding-top: 0.5rem; }
.unread-dot { width: 8px; height: 8px; background-color: #3b82f6; border-radius: 50%; }

.empty-state { text-align: center; padding: 4rem; color: #6b7280; font-style: italic; }

/* Pagination Styles */
.pagination-container { margin-top: 2.5rem; display: flex; justify-content: center; }
.pagination-wrapper { display: flex; align-items: center; gap: 1.5rem; background: white; padding: 0.75rem 1.5rem; border-radius: 16px; border: 1px solid #f3f4f6; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.pages-list { display: flex; gap: 0.5rem; }
.page-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: transparent; color: #6b7280; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.page-btn:hover { background: #f3f4f6; color: #111827; }
.page-btn.active { background: #209216; color: white; }
.pagin-btn { background: #f9fafb; border: 1px solid #e5e7eb; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; color: #374151; cursor: pointer; transition: all 0.2s; }
.pagin-btn:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 1024px) { .content { margin-left: 80px; } }
@media (max-width: 640px) {
  .notification-card { padding: 1rem; }
  .action-buttons { flex-direction: column; }
}
</style>
