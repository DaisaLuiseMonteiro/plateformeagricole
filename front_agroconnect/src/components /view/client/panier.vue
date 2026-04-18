<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import Header from '@/components /layout/header.vue';
import { usePanierStore } from '@/stores/panier/panier_store';
import { useAuthStore } from '@/stores/auth/auth_store';

const router = useRouter();
const panierStore = usePanierStore();
const authStore = useAuthStore();

const cartItems = computed(() => panierStore.items);

const updateQuantity = (id: string, delta: number) => {
  const item = panierStore.items.find(i => i.product.id === id);
  if (item) {
    panierStore.modifierQuantite(id, item.quantity + delta);
  }
};

const removeItem = (id: string) => {
  panierStore.supprimerDuPanier(id);
};

const itemTotal = (item: any) => item.product.prix_unitaire * item.quantity;

const grandTotal = computed(() => panierStore.totalPrice);

const formatPrice = (value: number) =>
  value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');

const handleCommander = async () => {
  if (!authStore.isAuthenticated) {
    alert('Veuillez vous connecter pour passer commande.');
    router.push('/login');
    return;
  }

  try {
    const clientId = authStore.user?.id;
    if (!clientId) throw new Error('ID Client manquant');
    
    await panierStore.commander(clientId);
    alert('Commande passée avec succès !');
    router.push('/mes-commandes'); // Correct redirection
  } catch (error: any) {
    alert('Erreur lors de la commande: ' + error.message);
  }
};

const goToHome = () => router.push('/');
</script>

<template>
  <Header />

  <main class="cart-main">
    <h1 class="cart-title">Mon panier</h1>

    <div class="cart-layout">
      <!-- Left: Cart Items -->
      <div class="cart-items">
        <div v-for="item in cartItems" :key="item.product.id" class="cart-item-card">
          <div class="item-image-box">
            <img :src="item.product.photo || '/images/client.png'" :alt="item.product.description" />
          </div>
          <div class="item-details">
            <h3 class="item-name">{{ item.product.name }}</h3>
            <p class="item-farm">Catégorie: {{ item.product.categorie }}</p>
            <p class="item-price">{{ formatPrice(item.product.prix_unitaire) }} FCFA</p>
          </div>
          <div class="item-controls">
            <button class="qty-btn" @click="updateQuantity(item.product.id, -1)">−</button>
            <span class="qty-value">{{ item.quantity }}</span>
            <button class="qty-btn" @click="updateQuantity(item.product.id, 1)">+</button>
            <button class="delete-btn" @click="removeItem(item.product.id)" aria-label="Supprimer">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Empty state -->
        <div v-if="cartItems.length === 0" class="empty-cart">
          <svg fill="none" stroke="#9ca3af" viewBox="0 0 24 24" stroke-width="1.5" class="empty-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <p>Votre panier est vide</p>
          <button class="back-btn" @click="goToHome">Retour aux produits</button>
        </div>
      </div>

      <!-- Right: Summary -->
      <div class="cart-summary" v-if="cartItems.length > 0">
        <h2 class="summary-title">Résumé</h2>
        <div class="summary-lines">
          <div v-for="item in cartItems" :key="'s-' + item.product.id" class="summary-line">
            <span class="summary-label">{{ item.product.name }} × {{ item.quantity }}</span>
            <span class="summary-value">{{ formatPrice(itemTotal(item)) }} FCFA</span>
          </div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-total">
          <span class="total-label">Total</span>
          <span class="total-value">{{ formatPrice(grandTotal) }} FCFA</span>
        </div>
        <button class="order-btn" @click="handleCommander">
          Commander
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5" class="arrow-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </button>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* ============================================================
   CART PAGE — MAIN CONTENT
   ============================================================ */
.cart-main {
  padding: 2.5rem 60px;
  background: rgb(238, 247, 241);
  min-height: calc(100vh - 140px);
  font-family: 'Inter', sans-serif;
}

.cart-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #111827;
  margin: 0 0 1.75rem 0;
}

.cart-layout {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

/* --- Cart Items Column --- */
.cart-items {
  flex: 1.6;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item-card {
  background: white;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
  transition: box-shadow 0.2s ease, transform 0.15s ease;
}

.cart-item-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.item-image-box {
  width: 90px;
  height: 90px;
  min-width: 90px;
  border-radius: 12px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.item-image-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.item-farm {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 2px 0 0 0;
  font-style: italic;
}

.item-price {
  font-size: 0.9rem;
  font-weight: 700;
  color: #209216;
  margin: 4px 0 0 0;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.qty-btn:hover {
  background: #f3f4f6;
  border-color: #209216;
  color: #209216;
}

.qty-value {
  min-width: 32px;
  text-align: center;
  font-weight: 700;
  font-size: 1rem;
  color: #111827;
}

.delete-btn {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 8px;
  background: #fef2f2;
  color: #dc2626;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
  transition: all 0.15s ease;
}

.delete-btn svg {
  width: 18px;
  height: 18px;
}

.delete-btn:hover {
  background: #fee2e2;
  transform: scale(1.1);
}

/* --- Summary Panel --- */
.cart-summary {
  flex: 1;
  background: white;
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
  position: sticky;
  top: 2rem;
}

.summary-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: #111827;
  margin: 0 0 1.25rem 0;
}

.summary-lines {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-label {
  font-size: 0.9rem;
  color: #374151;
}

.summary-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #111827;
}

.summary-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 1.25rem 0;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.total-label {
  font-size: 1rem;
  font-weight: 800;
  color: #111827;
}

.total-value {
  font-size: 1.15rem;
  font-weight: 800;
  color: #209216;
}

.order-btn {
  width: 100%;
  padding: 0.9rem 1.5rem;
  background: #209216;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

.order-btn:hover {
  background: #1a7a12;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(32, 146, 22, 0.3);
}

.arrow-icon {
  width: 18px;
  height: 18px;
}

/* --- Empty State --- */
.empty-cart {
  background: white;
  border-radius: 14px;
  padding: 3rem;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
}

.empty-cart p {
  font-size: 1.1rem;
  color: #6b7280;
  margin: 0 0 1.5rem 0;
}

.back-btn {
  padding: 0.75rem 2rem;
  background: #209216;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #1a7a12;
}

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 900px) {
  .cart-layout {
    flex-direction: column;
  }
  .cart-summary {
    position: static;
  }
  .cart-main {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .top-bar { height: auto; padding: 1rem 0; }
  .header-container { flex-direction: column; gap: 1rem; }
  .nav-links { display: none; }
}

@media (max-width: 1024px) {
  .search-section { display: none; }
}
</style>
