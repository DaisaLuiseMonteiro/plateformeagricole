<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'
import { useNotificationStore } from '@/stores/utilitaires/notification_store'

const router = useRouter()
const route = useRoute()
const notificationStore = useNotificationStore()

const user = {
  firstName: 'Jean',
  lastName: 'Dupont',
  photo: '/images/client.png' // Placeholder image
}

const roleLabel = computed(() => {
  if (route.path.startsWith('/admin')) return 'Administrateur'
  if (route.path.startsWith('/agriculteur')) return 'Agriculteur'
  return ''
})

const goToNotifications = () => {
  notificationStore.markAsRead()
  if (route.path.startsWith('/admin')) {
    router.push('/admin/notifications')
  } else if (route.path.startsWith('/agriculteur')) {
    router.push('/agriculteur/notifications')
  } else {
    router.push('/notifications')
  }
}
</script>

<template>
  <nav class="navbar">
    <!-- Left: User Info -->
    <div class="profile-section">
      <div class="profile-img-container">
        <img :src="user.photo" alt="Profile Photo" class="profile-img" />
      </div>
      <div class="user-info">
        <span class="user-name">{{ user.firstName }} {{ user.lastName }}</span>
        <span v-if="roleLabel" class="user-role">{{ roleLabel }}</span>
      </div>
    </div>

    <!-- Right: Action Icons -->
    <div class="actions-section">
      <button class="action-btn" aria-label="Notifications" @click="goToNotifications">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="icon-svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <span v-if="notificationStore.hasUnread" class="badge"></span>
      </button>

      <button class="action-btn" aria-label="Settings">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="icon-svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>

      <button class="action-btn" aria-label="Go to Home" @click="router.push('/')">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="icon-svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 260px;
  width: calc(100% - 260px);
  box-sizing: border-box;
  height: 100px;
  background-color: #209216;
  padding: 0 2.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 90;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.profile-section:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.profile-img-container {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.2);
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.user-name {
  font-weight: 700;
  color: #ffffff;
  font-size: 1rem;
  line-height: 1.2;
}

.user-role {
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
}

.actions-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.action-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.action-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 10px;
  height: 10px;
  background-color: #fbbf24;
  border: 2px solid #209216;
  border-radius: 50%;
}

.icon-svg {
  width: 22px;
  height: 22px;
}

@media (max-width: 1024px) {
  .navbar {
    left: 80px;
    width: calc(100% - 80px);
  }
}

@media (max-width: 640px) {
  .user-name {
    display: none;
  }
}
</style>
