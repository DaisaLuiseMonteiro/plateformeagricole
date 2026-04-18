<script setup lang="ts">
import SidebarAdmin from '@/components /layout/sidebar-admin.vue'
import Navebar from '@/components /layout/navebar.vue'
</script>

<template>
  <div class="admin-layout">
    <SidebarAdmin />
    <div class="main-container">
      <Navebar />
      <main class="content">
        <div class="page-header">
          <h1 class="page-title">Statistiques Globales</h1>
          <p class="page-description">Analysez les performances et la croissance de la plateforme.</p>
        </div>
        <div class="placeholder-content">
          <p>Graphiques et analyses de données...</p>
        </div>
      </main>
    </div>
  </div>Commandes
Suivi de production par commande
Suivi de production par commande
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background-color: rgb(238, 247, 241); }
.main-container { flex: 1; display: flex; flex-direction: column; }
.content {
  margin-top: 75px;
  margin-left: 275px;
  padding: 2.5rem;
  transition: all 0.3s ease;
}
.page-title { font-size: 1.875rem; font-weight: 700; color: #111827; }
.page-description { color: #6b7280; margin-top: 0.5rem; }
.placeholder-content { background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
@media (max-width: 1024px) { .content { margin-left: 80px; } }
</style>
