import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim() || 'http://127.0.0.1:8000'

export interface OrderDetail {
  id: string
  produit_id: string
  quantite: number
  montant: number
  agriculteur_nom?: string
}

export interface Order {
  id: string
  date_commande: string
  statut: string
  montant_commande: number
  client_id: string
  details: OrderDetail[]
}

export const useCommandeStore = defineStore('commande', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const successMessage = ref<string | null>(null)
  const orders = ref<Order[]>([])

  const fetchCommandesClient = async (clientId: string) => {
    loading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/commandes/client/${clientId}`)
      if (!response.ok) throw new Error('Erreur lors du chargement des commandes client')
      orders.value = await response.json()
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchCommandesAgriculteur = async (agriculteurId: string) => {
    loading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/commandes/agriculteur/${agriculteurId}`)
      if (!response.ok) throw new Error('Erreur lors du chargement des commandes agriculteur')
      orders.value = await response.json()
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const creerCommande = async (commandeData: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE_URL}/commandes/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(commandeData)
      })
      if (!response.ok) throw new Error('Erreur lors de la validation du panier')
      const result = await response.json()
      successMessage.value = 'Commande validée avec succès !'
      return result
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const confirmerCommande = async (commandeId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/commandes/${commandeId}/confirmer`, { method: 'PATCH' })
      if (!response.ok) throw new Error('Erreur lors de la confirmation')
      return await response.json()
    } catch (err: any) {
      error.value = err.message
    }
  }

  const rejeterCommande = async (commandeId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/commandes/${commandeId}/rejeter`, { method: 'PATCH' })
      if (!response.ok) throw new Error('Erreur lors du rejet')
      return await response.json()
    } catch (err: any) {
      error.value = err.message
    }
  }

  return {
    loading,
    error,
    successMessage,
    orders,
    fetchCommandesClient,
    fetchCommandesAgriculteur,
    creerCommande,
    confirmerCommande,
    rejeterCommande
  }
})
