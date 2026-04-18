<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

const navItems = [
  { name: 'Tableau de bord', path: '/agriculteur/dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { name: 'Mes produits', path: '/agriculteur/produits', icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { name: 'Mes commandes', path: '/agriculteur/commandes', icon: 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z' },
  { name: 'Mes ventes', path: '/agriculteur/ventes', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' },
  { name: 'Notifications', path: '/agriculteur/notifications', icon: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' }
]

const activeItem = computed(() => route.path)

const navigate = (path: string) => {
  router.push(path)
}
const logout = () => {
  router.push('/login')
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="brand">
        <div class="logo-box">
          <img src="/images/logo.jpeg" alt="Logo" class="logo-img" />
        </div>
        <h2 class="app-name">AgroConnect</h2>
      </div>

      <nav class="nav-menu">
        <button 
          v-for="item in navItems" 
          :key="item.name"
          class="nav-item"
          :class="{ active: activeItem === item.path }"
          @click="navigate(item.path)"
        >
          <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
          </svg>
          <span class="nav-label">{{ item.name }}</span>
        </button>
      </nav>
    </div>

    <div class="sidebar-bottom">
      <button class="logout-btn" @click="logout">
        <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        <span class="nav-label">Déconnexion</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 15%;
  height: 97%;
  min-width: 180px;
  background-color: #209216;
  border-right: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem 0.75rem;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  font-family: 'Inter', sans-serif;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.05);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2.5rem;
  text-align: center;
  margin-left: 1.5rem;
}

.logo-box {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.app-name {
  font-size: 0.85rem;
  font-weight: 800;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 1rem;
  padding: 0.85rem 1.25rem;
  border: none;
  background: none;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.75);
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  font-weight: 700;
}

.nav-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.nav-label {
  font-size: 0.95rem;
  font-weight: 500;
  text-align: left;
  line-height: 1.2;
}

.logout-btn {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 1rem;
  padding: 0.85rem 1.25rem;
  border: none;
  background: none;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.75);
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  margin-top: auto;
}

.logout-btn:hover {
  background-color: rgba(239, 68, 68, 0.2);
  color: #ffffff;
}

@media (max-width: 1024px) {
  .sidebar {
    width: 80px;
  }
  .app-name, .nav-label {
    display: none;
  }
}
</style>
