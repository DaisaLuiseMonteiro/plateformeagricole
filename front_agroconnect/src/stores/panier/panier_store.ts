import { defineStore } from 'pinia'

export interface Product {
  id: string;
  name: string;
  prix_unitaire: number;
  description: string | null;
  quantite_stock: number;
  photo: string | null;
  categorie: string;
  agriculteur_id: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export const usePanierStore = defineStore('panier', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('panier_items') || '[]') as CartItem[],
    errorMessage: null as string | null,
  }),

  getters: {
    totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    totalPrice: (state) => state.items.reduce((sum, item) => sum + item.product.prix_unitaire * item.quantity, 0),
  },

  actions: {
    // ============================================================
    // AJOUTER UN PRODUIT AU PANIER
    // ============================================================
    ajouterAuPanier(product: Product, quantity: number = 1) {
      const existingItem = this.items.find(item => item.product.id === product.id);

      if (existingItem) {
        // Vérification du stock
        if (existingItem.quantity + quantity <= product.quantite_stock) {
          existingItem.quantity += quantity;
        } else {
          this.errorMessage = 'Stock insuffisant pour augmenter la quantité.';
          setTimeout(() => this.errorMessage = null, 3000);
        }
      } else {
        // Nouveau produit
        if (quantity <= product.quantite_stock) {
          this.items.push({ product, quantity });
        } else {
          this.errorMessage = 'Stock insuffisant.';
          setTimeout(() => this.errorMessage = null, 3000);
        }
      }
      this.sauvegarderPanier();
    },

    // ============================================================
    // SUPPRIMER UN PRODUIT
    // ============================================================
    supprimerDuPanier(productId: string) {
      this.items = this.items.filter(item => item.product.id !== productId);
      this.sauvegarderPanier();
    },

    // ============================================================
    // MODIFIER LA QUANTITÉ
    // ============================================================
    modifierQuantite(productId: string, newQuantity: number) {
      const item = this.items.find(i => i.product.id === productId);
      if (item) {
        if (newQuantity <= item.product.quantite_stock && newQuantity > 0) {
          item.quantity = newQuantity;
          this.sauvegarderPanier();
        } else if (newQuantity <= 0) {
          this.supprimerDuPanier(productId);
        } else {
          this.errorMessage = 'Stock insuffisant.';
          setTimeout(() => this.errorMessage = null, 3000);
        }
      }
    },

    // ============================================================
    // VIDER LE PANIER
    // ============================================================
    viderPanier() {
      this.items = [];
      this.sauvegarderPanier();
    },

    // ============================================================
    // SAUVEGARDE LOCALE
    // ============================================================
    sauvegarderPanier() {
      localStorage.setItem('panier_items', JSON.stringify(this.items));
    },

    // ============================================================
    // VALIDER LA COMMANDE (BACKEND)
    // ============================================================
    async commander(clientId: string) {
      const commandeStore = (await import('../commandes/commande_store')).useCommandeStore();
      
      const commandeData = {
        client_id: clientId,
        montant_total: this.totalPrice,
        items: this.items.map(item => ({
          produit_id: item.product.id,
          quantite: item.quantity,
          montant: item.product.prix_unitaire * item.quantity
        }))
      };

      try {
        await commandeStore.creerCommande(commandeData);
        this.viderPanier();
      } catch (error) {
        console.error('Erreur lors de la commande:', error);
        throw error;
      }
    }
  }
})
