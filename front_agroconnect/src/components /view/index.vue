<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import Header from '@/components /layout/header.vue';
import AuthPopup from '@/components /view/popup/AuthPopup.vue';
import { usePagination } from '@/stores/utilitaires/utilitaire_store';
import { useAuthStore } from '@/stores/auth/auth_store';
import { usePanierStore } from '@/stores/panier/panier_store';
import type { Product } from '@/interface/Product';

interface Category {
  id: number;
  name: string;
  count: number;
  icon: string;
}

const authStore = useAuthStore();
const panierStore = usePanierStore();

const isAuthPopupOpen = ref(false);
const authPopupMessage = ref('');
const authPopupVerb = ref('');

const products = ref<Product[]>([]);

const categories = ref<Category[]>([
  { id: 1, name: 'Tous les produits', count: 0, icon: '📦' },
  { id: 2, name: 'Légumes', count: 0, icon: '🥬' },
  { id: 3, name: 'Fruits', count: 0, icon: '🥭' },
  { id: 4, name: 'Céréales', count: 0, icon: '🌾' }
]);

const selectedCategory = ref('Tous les produits');

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'Tous les produits') {
    return products.value;
  }
  return products.value.filter(p => p.categorie === selectedCategory.value);
});

const { currentPage, totalPages, paginatedItems: paginatedProducts, goToPage } = usePagination(filteredProducts, 10);

const handleCategoryChange = (category: string) => {
  selectedCategory.value = category;
  currentPage.value = 1;
};

const fetchProducts = async () => {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
    const response = await fetch(`${API_BASE_URL}/produits`);
    if (response.ok) {
      const data = await response.json();
      // Filtrer uniquement les produits publiés
      const publishedProducts = data.filter((p: any) => p.statut_publication === 'publie');
      
      products.value = publishedProducts.map((p: any) => ({
        id: p.id,
        name: p.nom || p.description?.substring(0, 20) || 'Sans nom',
        prix_unitaire: p.prix_unitaire,
        description: p.description,
        quantite_stock: p.quantite_stock,
        photo: p.photo || 'https://via.placeholder.com/300x200',
        categorie: p.categorie,
        agriculteur_id: p.agriculteur_id
      }));

      // Mettre à jour les compteurs de manière sûre
      categories.value = categories.value.map(cat => {
        if (cat.name === 'Tous les produits') {
          return { ...cat, count: products.value.length };
        }
        // Mapping des catégories pour le filtre
        const catMap: Record<string, string> = {
          'Légumes': 'legume',
          'Fruits': 'fruit',
          'Céréales': 'cereale'
        };
        const backendCat = catMap[cat.name];
        return { 
          ...cat, 
          count: products.value.filter(p => p.categorie === backendCat).length 
        };
      });
    }
  } catch (error) {
    console.error('Erreur lors du chargement des produits:', error);
  }
};

onMounted(() => {
  fetchProducts();
});

const handleAddToCart = (product: Product) => {
  console.log('Ajout au panier:', product);
  if (authStore.isAuthenticated) {
    panierStore.ajouterAuPanier({
      id: product.id,
      name: product.name,
      prix_unitaire: product.prix_unitaire,
      description: product.description,
      quantite_stock: product.quantite_stock,
      photo: product.photo,
      categorie: product.categorie,
      agriculteur_id: product.agriculteur_id
    });
    console.log('Produit ajouté avec succès');
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
          <img :src="product.photo || 'https://via.placeholder.com/300x200'" :alt="product.name" class="product-image" />
        </div>
        <div class="product-info-row">
          <div class="text-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-category-text">{{ product.categorie }}</p>
            <p class="product-price">{{ product.prix_unitaire }} CFA/kg</p>
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
  padding: 0.6rem 20px;
    background: rgb(238, 247, 241);

  min-height: calc(100vh - 140px);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.25rem;
}

.product-card {
  height: 280px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.product-image-container {
  height: 65%;
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
  font-size: 1.5rem;
  font-weight: 700;
  color: #209216;
  margin: 0;
}

.product-category-text {
  font-size: 0.85rem; /* Increased from 0.75rem */
  color: #209216; /* Changed to green */
  transform: translateY(-5px);
  font-weight: 600;
  margin: 0;
  
  text-transform: capitalize;
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
  margin-bottom: 1.5rem;
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
  margin-top: 0.5rem; /* Reduced from 3rem */
  padding-bottom: 9rem; /* Increased slightly to ensure space at the absolute bottom */
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