import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim() || 'http://127.0.0.1:8000'

export const useProduitStore = defineStore('produit', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const successMessage = ref<string | null>(null)
  const produits = ref<any[]>([])

  const ajouterProduit = async (data: {
    prix_unitaire: number
    description: string
    quantite_stock: number
    photo: string
    categorie: string
    agriculteur_id: string
  }) => {
    loading.value = true
    error.value = null
    successMessage.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/produits/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      const result = await response.json()

      if (!response.ok) {
        const status = response.status

        if (status === 400) {
          error.value = result.detail || 'Les données du produit sont invalides. Vérifiez les champs et réessayez.'
        } else if (status === 401) {
          error.value = 'Vous devez être connecté pour ajouter un produit.'
        } else if (status === 403) {
          error.value = 'Seul un agriculteur actif peut ajouter un produit.'
        } else if (status === 422) {
          error.value = 'Certains champs sont manquants ou incorrects. Veuillez vérifier le formulaire.'
        } else {
          error.value = result.detail || 'Une erreur inattendue est survenue. Veuillez réessayer plus tard.'
        }
        throw new Error(error.value!)
      }

      successMessage.value = result.message || 'Produit ajouté avec succès !'
      return result
    } catch (err: any) {
      if (!error.value) {
        error.value = 'Impossible de joindre le serveur. Vérifiez votre connexion internet.'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchProduitsAgriculteur = async (agriculteurId: string) => {
    loading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/produits/agriculteur/${agriculteurId}`)
      if (!response.ok) throw new Error('Erreur de récupération')
      produits.value = await response.json()
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const supprimerProduit = async (produitId: string) => {
    loading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/produits/${produitId}`, { method: 'DELETE' })
      if (!response.ok) throw new Error('Erreur lors de la suppression')
      return await response.json()
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const resetMessages = () => {
    error.value = null
    successMessage.value = null
  }

  return {
    loading,
    error,
    successMessage,
    produits,
    ajouterProduit,
    fetchProduitsAgriculteur,
    supprimerProduit,
    resetMessages
  }
})
