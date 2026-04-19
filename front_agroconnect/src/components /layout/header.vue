<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '@/stores/utilitaires/notification_store'
import { useAuthStore } from '@/stores/auth/auth_store'
import { usePanierStore } from '@/stores/panier/panier_store'
import AuthPopup from '@/components /view/popup/AuthPopup.vue'
import ProductionFormPopup from '@/components /view/popup/ProductionFormPopup.vue'

const router = useRouter();
const notificationStore = useNotificationStore()
const authStore = useAuthStore()
const panierStore = usePanierStore()
const emit = defineEmits(['category-selected']);

const isCategoryOpen = ref(false);
const isAuthPopupOpen = ref(false);
const isProductionPopupOpen = ref(false);
const authPopupMessage = ref('');
const authPopupVerb = ref('');

const goToHome = () => router.push('/');
const goToPanier = () => checkAuthForAction(() => router.push('/panier'), 'pour pouvoir commander', 'commander');
const goToCommandes = () => {
  if (authStore.isAuthenticated) {
    router.push('/mes-commandes');
  } else {
    authPopupMessage.value = 'pour voir vos commandes';
    authPopupVerb.value = 'voir';
    isAuthPopupOpen.value = true;
  }
};

const checkAuthForAction = (action: () => void, message: string, verb: string) => {
  if (authStore.isAuthenticated) {
    action();
  } else {
    authPopupMessage.value = message;
    authPopupVerb.value = verb;
    isAuthPopupOpen.value = true;
  }
};
const goToNotifications = () => {
  checkAuthForAction(() => {
    notificationStore.markAsRead()
    router.push('/user') // Ou une page spécifique de notifications si elle existe
  }, 'pour voir vos notifications', 'voir');
}

const goToProfile = () => {
  if (authStore.isAuthenticated) {
    router.push('/user'); // Ou une page de profil spécifique
  } else {
    router.push('/login');
  }
};

const selectCategory = (category: string) => {
  emit('category-selected', category);
  isCategoryOpen.value = false;
};
</script>

<template>
  <header class="app-header">
    <!-- Top Bar: Logo, Search, Icons -->
    <div class="top-bar">
      <div class="header-container">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-box">
            <img src="/images/logo.jpeg" alt="AgroConnect Logo" class="logo-image" />
          </div>
          <span class="brand-name">AGROCONNECT</span>
        </div>

        <!-- Search Section -->
        <div class="search-section">
          <div class="search-wrapper">
            <input type="text" placeholder="Search products..." class="search-input" />
            <button class="search-button">Search</button>
          </div>
        </div>

        <!-- Actions Section -->
        <div class="actions-section">
          <div class="notification-trigger" @click="goToNotifications">
            <svg class="icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span v-if="notificationStore.hasUnread" class="dot-badge badge-red"></span>
          </div>
          <div class="action-icons">
            <div class="icon-wrapper">
              <button class="icon-btn" aria-label="Profile" @click="goToProfile">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </button>
              <span v-if="authStore.isAuthenticated" class="dot-badge badge-green"></span>
            </div>
            
            <button class="icon-btn" aria-label="Wishlist">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
            </button>

            <div class="icon-wrapper">
              <button class="icon-btn" aria-label="Cart" @click="goToPanier">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              </button>
              <span v-if="panierStore.totalItems > 0" class="dot-badge badge-red"></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Nav Bar: Categories, Links, CTA -->
    <nav class="nav-bar">
      <div class="header-container">
        <div class="category-wrapper" style="position: relative; margin-left: 50px;">
          <button class="category-btn" @click="isCategoryOpen = !isCategoryOpen" style="margin-left: 0;">
            <svg class="icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            Choisir une catégorie
          </button>
          <div v-if="isCategoryOpen" class="category-dropdown-content">
            <div class="dropdown-item" @click="selectCategory('Tous les produits')">Tous les produits</div>
            <div class="dropdown-item" @click="selectCategory('Céréales')">Céréales</div>
            <div class="dropdown-item" @click="selectCategory('Fruits')">Fruits</div>
            <div class="dropdown-item" @click="selectCategory('Légumes')">Légumes</div>
          </div>
        </div>

        <ul class="nav-links">
          <li><a @click.prevent="goToHome" href="#" :class="{ active: $route.path === '/' }">Accueil</a></li>
          <li><a @click.prevent="checkAuthForAction(() => isProductionPopupOpen = true, 'pour faire une demande de production', 'commander')" href="#">Production sur commande</a></li>
          <li><a @click.prevent="goToCommandes" href="#" :class="{ active: $route.path === '/mes-commandes' }">Mes commandes</a></li>
          <li><a @click.prevent="goToPanier" href="#" :class="{ active: $route.path === '/panier' }">Aide clientèle</a></li>
          <li><a href="#">À propos de nous</a></li>
        </ul>

        <button class="sell-btn">
          Vendre sur AgroConnect
        </button>
      </div>
    </nav>
    
    <AuthPopup 
      v-if="isAuthPopupOpen" 
      :message="authPopupMessage" 
      :verb="authPopupVerb" 
      @close="isAuthPopupOpen = false" 
    />
    
    <ProductionFormPopup 
      :isOpen="isProductionPopupOpen"
      @close="isProductionPopupOpen = false"
      @submitted="isProductionPopupOpen = false"
    />
  </header>
</template>

<style scoped>
.app-header {
  width: 100%;
  font-family: 'Inter', sans-serif;
}

.header-container {
  width: 100%;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.top-bar {
  background-color: #209216;
  color: white;
  height: 80px;
}

.logo-section {
  display: flex;
  align-items: center;
  margin-left: 50px;
}

.logo-box {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-left: 10px;
}

.search-section {
  flex: 1;
  max-width: 600px;
  padding: 0 2rem;
}

.search-wrapper {
  display: flex;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  height: 44px;
}

.search-input {
  flex: 1;
  border: none;
  padding: 0 1.25rem;
  font-size: 0.95rem;
  outline: none;
  color: #333;
}

.search-button {
  background: black;
  color: white;
  border: none;
  padding: 0 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.search-button:hover {
  opacity: 0.8;
}

.actions-section {
  display: flex;
  align-items: center;
  gap: 1.4rem;
  margin-right: 50px;
}

.action-icons {
  display: flex;
  gap: 1.25rem;
}

.icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.icon-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0.25rem;
  transition: transform 0.2s;
}

.icon-btn:hover {
  transform: scale(1.1);
}

.icon-btn svg {
  width: 24px;
  height: 24px;
}

.dot-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 10px;
  height: 10px;
  border: 2px solid #209216;
  border-radius: 50%;
}

.badge-red {
  background-color: #ef4444; /* Rouge vif */
}

.badge-green {
  background-color: #10b981; /* Vert émeraude */
}

.icon-btn:hover {
  transform: scale(1.1);
}

.icon-btn svg {
  width: 24px;
  height: 24px;
}

.nav-bar {
  background-color: #209216;
  height: 60px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.category-btn {
  background-color: #ef7d00;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.category-btn:hover {
  background-color: #d66f00;
}

.category-dropdown-content {
  position: absolute;
  top: 110%;
  left: 0;
  background: white;
  min-width: 200px;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 50;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.dropdown-item {
  padding: 0.75rem 1.25rem;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
  color: #209216;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  opacity: 0.9;
  transition: opacity 0.2s;
  cursor: pointer;
}

.nav-links li a:hover,
.nav-links li a.active {
  opacity: 1;
  font-weight: 700;
}

.sell-btn {
  background: black;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s;
  margin-right: 50px;
}

.sell-btn:hover {
  transform: scale(1.02);
}

@media (max-width: 1024px) {
  .search-section {
    display: none;
  }
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: 1rem;
  }
  .nav-links {
    display: none;
  }
}
</style>