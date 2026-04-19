<script setup lang="ts">
import { ref, computed } from 'vue';
import Header from '@/components /layout/header.vue';
import AuthPopup from '@/components /view/popup/AuthPopup.vue';
import { usePagination } from '@/stores/utilitaires/utilitaire_store';
import { useAuthStore } from '@/stores/auth/auth_store';
import { usePanierStore } from '@/stores/panier/panier_store';

const authStore = useAuthStore();
const panierStore = usePanierStore();

const isAuthPopupOpen = ref(false);
const authPopupMessage = ref('');
const authPopupVerb = ref('');

const products: { id: string; name: string; category: string; price: number; displayPrice: string; image: string; stock: number; agriculteur_id: string }[] = [];

const categories = [
  { id: 1, name: 'Tous les produits', count: 0, icon: '📦' },
  { id: 2, name: 'Légumes', count: 0, icon: '🥬' },
  { id: 3, name: 'Fruits', count: 0, icon: '🥭' },
  { id: 4, name: 'Céréales', count: 0, icon: '🌾' }
];

const selectedCategory = ref('Tous les produits');

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'Tous les produits') {
    return products;
  }
  return products.filter(p => p.category === selectedCategory.value);
});

const { currentPage, totalPages, paginatedItems: paginatedProducts, goToPage } = usePagination(filteredProducts, 10);

const handleCategoryChange = (category: string) => {
  selectedCategory.value = category;
  currentPage.value = 1;
};

const handleAddToCart = (product: any) => {
  if (authStore.isAuthenticated) {
    panierStore.ajouterAuPanier({
      id: product.id,
      name: product.name,
      prix_unitaire: product.price,
      description: '',
      quantite_stock: product.stock,
      photo: product.image,
      categorie: product.category,
      agriculteur_id: product.agriculteur_id
    });
  } else {
    authPopupMessage.value = 'pour pouvoir commander';
    authPopupVerb.value = 'commander';
    isAuthPopupOpen.value = true;
  }
};


</script>

<template>
  <Header @category-selected="handleCategoryChange" />
  
  <main class="main-content">
    <!-- Category Statistics Cards -->
    <div class="category-stats-grid">
      <div v-for="category in categories" :key="category.id" class="stat-card" @click="handleCategoryChange(category.name)">
        <div class="stat-icon">{{ category.icon }}</div>
        <h3 class="stat-name">{{ category.name }}</h3>
        <p class="stat-count">{{ category.count }} produits</p>
      </div>
    </div>

    <div class="product-grid">
      <div v-for="product in paginatedProducts" :key="product.id" class="product-card">
        <div class="product-image-container">
          <img :src="product.image" :alt="product.name" class="product-image" />
        </div>
        <div class="product-info-row">
          <div class="text-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-price">{{ product.displayPrice }}</p>
          </div>
          <div class="action-buttons">
            <button class="action-btn favorite-btn" aria-label="Add to favorites">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-svg">
                <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
            <button class="action-btn plus-btn" aria-label="Add to cart" @click="handleAddToCart(product)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="icon-svg">
                <path d="M12 5v14M5 12h14" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination Controls -->
    <div class="pagination-container" v-if="totalPages > 1">
      <button 
        class="pagination-btn arrow-btn" 
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="icon-small">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <div class="page-numbers">
        <button 
          v-for="page in totalPages" 
          :key="page"
          class="pagination-btn page-num"
          :class="{ active: currentPage === page }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </div>

      <button 
        class="pagination-btn arrow-btn" 
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="icon-small">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <!-- Auth Protection Popup -->
    <AuthPopup 
      v-if="isAuthPopupOpen" 
      :message="authPopupMessage" 
      :verb="authPopupVerb" 
      @close="isAuthPopupOpen = false" 
    />
  </main>
</template>

<style scoped>


/* --- Main Content --- */
.main-content {
  padding: 2rem 50px;
    background: rgb(238, 247, 241);

  min-height: calc(100vh - 140px);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.25rem;
}

.product-card {
  height: 270px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.product-image-container {
  height: 70%;
  width: 100%;
  background: white;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info-row {
  height: 30%;
  padding: 0.25rem 0.75rem 0.75rem 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center; /* Adjusted to center for better horizontal alignment */
}

.text-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.product-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: #000000;
  margin: 0;
}

.product-price {
  font-size: 0.9rem;
  font-weight: 700;
  color: #209216;
  margin: 0;
}

.action-buttons {
  display: flex;
  flex-direction: row; /* Horizontal alignment */
  gap: 0.5rem;
}

.action-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid #209216;
  background: white;
  color: #209216;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover, .action-btn:active {
  background: #209216;
  color: white;
  border-color: #209216;
}

.favorite-btn:hover, .favorite-btn:active {
  background: #209216;
  color: white;
  border-color: #209216;
}

.icon-svg {
  width: 18px;
  height: 18px;
}

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 1024px) {
  .search-section {
    display: none; /* Hide search on medium screens for simplicity in this example */
  }
}

@media (max-width: 768px) {
  .top-bar {
    height: auto;
    padding: 1rem 0;
  }
  .header-container {
    flex-direction: column;
    gap: 1rem;
  }
  .nav-links {
    display: none;
  }
}

/* ============================================================
   CATEGORY STATS CARDS
   ============================================================ */
.category-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border-color: #209216;
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.stat-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.stat-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
  margin: 0;
}

@media (max-width: 1024px) {
  .category-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .category-stats-grid {
    grid-template-columns: 1fr;
  }
}

/* ============================================================
   PAGINATION STYLES
   ============================================================ */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 3rem;
  padding-bottom: 2rem;
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.pagination-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e5e7eb;
  background-color: white;
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f3f4f6;
  border-color: #209216;
  color: #209216;
}

.pagination-btn.active {
  background-color: #209216;
  color: white;
  border-color: #209216;
  box-shadow: 0 4px 6px -1px rgba(32, 146, 22, 0.2);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #f9fafb;
}

.arrow-btn {
  width: 44px;
  height: 44px;
}
</style>