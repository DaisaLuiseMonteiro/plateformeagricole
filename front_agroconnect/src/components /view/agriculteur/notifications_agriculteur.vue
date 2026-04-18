<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import SidebarAgriculteur from '@/components /layout/sidebar-agriculteur.vue'
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

const handleAction = async (notif: any, action: 'accepter' | 'rejeter') => {
  isProcessingAction.value = notif.id
  const success = await notificationStore.performAction(notif, action)
  if (success) {
    if (action === 'accepter') {
      alert('Vous avez accepté la production. Le client a été averti.')
    }
  } else {
    alert('Action impossible. Il est possible que cette commande ait déjà été acceptée par un autre agriculteur.')
  }
  isProcessingAction.value = null
  await notificationStore.fetchNotifications() // Rafraîchir
}

const markAllAsRead = async () => {
  await notificationStore.markAsRead()
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('fr-FR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

const getIcon = (type: string) => {
  if (type === 'action_required') return 'star'
  return 'info'
}

const getColor = (type: string) => {
  if (type === 'action_required') return '#ef7d00'
  return '#209216'
}
</script>

<template>
  <div class="agriculteur-layout">
    <SidebarAgriculteur />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <div class="page-header">
          <div>
            <h1 class="page-title">Notifications</h1>
            <p class="unread-status">{{ unreadCount }} non lue(s)</p>
          </div>
          <button class="mark-read-btn" @click="markAllAsRead">
            Tout marquer comme lu
          </button>
        </div>

        <div v-if="notifications.length === 0" class="empty-state">
          <p>Aucune notification pour le moment.</p>
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
                <svg v-if="notif.type === 'action_required'" class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.382-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>
                <svg v-else class="icon-m" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
            </div>
            
            <div class="notif-content">
              <div class="notif-header">
                <h3 class="notif-title">{{ notif.titre }}</h3>
                <span v-if="notif.type === 'action_required'" class="action-badge">Action requise</span>
              </div>
              <p class="notif-desc">{{ notif.message }}</p>
              
              <!-- Boutons d'action -->
              <div v-if="notif.type === 'action_required'" class="action-buttons" @click.stop>
                <button 
                  class="btn-accept" 
                  :disabled="isProcessingAction === notif.id"
                  @click="handleAction(notif, 'accepter')"
                >
                  Accepter
                </button>
                <button 
                  class="btn-reject" 
                  :disabled="isProcessingAction === notif.id"
                  @click="handleAction(notif, 'rejeter')"
                >
                  Refuser / Ignorer
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
.agriculteur-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); font-family: 'Inter', sans-serif; }
.main-container { flex: 1; display: flex; flex-direction: column; width: 100%; }
.content { margin-top: 75px; margin-left: 295px; padding: 2.5rem; transition: margin-left 0.3s; }

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 2rem; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0; }
.unread-status { color: #6b7280; font-size: 0.95rem; margin-top: 0.25rem; font-weight: 500; }

.mark-read-btn { background: white; border: 1px solid #e5e7eb; padding: 0.6rem 1.25rem; border-radius: 12px; font-weight: 600; color: #374151; cursor: pointer; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.mark-read-btn:hover { background: #f9fafb; border-color: #d1d5db; }

.notifications-list { display: flex; flex-direction: column; gap: 0.75rem; }
.notification-card { background: white; border-radius: 16px; padding: 1.25rem 1.5rem; display: flex; align-items: flex-start; gap: 1.25rem; border: 1px solid #f3f4f6; transition: all 0.2s; cursor: pointer; position: relative; }
.notification-card:hover { border-color: #20921640; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transform: translateY(-1px); }
.notification-card.unread { border-left: 4px solid #209216; background: #f0fdf4; }
.notification-card.action-required { border-left: 4px solid #ef7d00; background: #fffbeb; }

.notif-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.25rem; }
.action-badge { background: #fee2e2; color: #b91c1c; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 4px; text-transform: uppercase; }

.notif-icon-section { flex-shrink: 0; padding-top: 0.25rem; }
.icon-circle { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.icon-m { width: 22px; height: 22px; }

.notif-content { flex: 1; }
.notif-title { font-size: 1.05rem; font-weight: 700; color: #111827; margin: 0; }
.notif-desc { color: #4b5563; font-size: 0.95rem; margin: 0.35rem 0; line-height: 1.5; }
.notif-time { font-size: 0.85rem; color: #9ca3af; font-weight: 500; display: block; margin-top: 0.75rem; }

.action-buttons { display: flex; gap: 0.75rem; margin-top: 1rem; }
.action-buttons button { padding: 0.5rem 1rem; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.btn-accept { background: #209216; color: white; border: none; }
.btn-accept:hover { background: #1a7a12; transform: translateY(-1px); }
.btn-reject { background: white; color: #4b5563; border: 1px solid #d1d5db; }
.btn-reject:hover { background: #f9fafb; border-color: #9ca3af; }

.notif-status-section { width: 20px; display: flex; justify-content: center; padding-top: 0.5rem; }
.unread-dot { width: 8px; height: 8px; background-color: #209216; border-radius: 50%; }

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
  .icon-circle { width: 40px; height: 40px; }
  .action-buttons { flex-direction: column; }
}
</style>
