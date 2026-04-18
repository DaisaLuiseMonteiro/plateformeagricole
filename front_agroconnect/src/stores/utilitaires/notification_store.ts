import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth/auth_store'

export interface Notification {
  id: string
  titre: string
  message: string
  type: 'info' | 'action_required'
  date_creation: string
  est_lue: boolean
  data?: any
}

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  const hasUnread = ref(false)
  const authStore = useAuthStore()

  const fetchNotifications = async () => {
    if (!authStore.user) return
    try {
      const response = await fetch(`http://127.0.0.1:8000/notifications/user/${authStore.user.id}`)
      if (response.ok) {
        const data = await response.json()
        notifications.value = data.map((n: any) => ({
          ...n,
          data: n.data ? JSON.parse(n.data) : null
        }))
        hasUnread.value = notifications.value.some(n => !n.est_lue)
      }
    } catch (error) {
      console.error('Erreur fetch notifications:', error)
    }
  }

  const markAsRead = async (id?: string) => {
    // Si ID fourni, marque une seule, sinon toutes
    const url = id 
      ? `http://127.0.0.1:8000/notifications/${id}/lire` 
      : `http://127.0.0.1:8000/notifications/user/${authStore.user?.id}/lire-tout`
    
    try {
      await fetch(url, { method: 'PATCH' })
      if (id) {
        const notif = notifications.value.find(n => n.id === id)
        if (notif) notif.est_lue = true
      } else {
        notifications.value.forEach(n => n.est_lue = true)
      }
      hasUnread.value = notifications.value.some(n => !n.est_lue)
    } catch (error) {
      console.error('Erreur markAsRead:', error)
    }
  }

  const performAction = async (notif: Notification, action: 'accepter' | 'rejeter' | 'publier') => {
    if (!notif.data) return

    let url = ''
    let method = 'POST'

    if (notif.data.type === 'product_validation') {
      method = 'PATCH'
      url = `http://127.0.0.1:8000/produits/${notif.data.produit_id}/${action === 'publier' ? 'publier' : 'rejeter'}`
    } else if (notif.data.type === 'production_opportunity') {
      if (action === 'accepter') {
        url = `http://127.0.0.1:8000/production/accepter/${notif.data.relance_id}`
      } else {
        // Pour rejeter une opportunité, on peut juste marquer la notif comme lue ou avoir un endpoint dédié
        return markAsRead(notif.id)
      }
    }

    if (!url) return

    try {
      const response = await fetch(url, { method })
      if (response.ok) {
        await markAsRead(notif.id)
        return true
      }
    } catch (error) {
      console.error('Erreur action notification:', error)
    }
    return false
  }

  return {
    notifications,
    hasUnread,
    fetchNotifications,
    markAsRead,
    performAction
  }
})
