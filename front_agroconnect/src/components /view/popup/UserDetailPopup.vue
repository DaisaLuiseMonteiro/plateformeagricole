<script setup lang="ts">
const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}
</script>

<template>
  <div class="popup-overlay" @click.self="closeModal">
    <div class="popup-modal">
      <div class="popup-header">
        <h2 class="popup-title">Détails de l'Utilisateur</h2>
        <button class="close-btn" @click="closeModal">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="user-detail-layout">
        <!-- Profile Header -->
        <div class="profile-banner">
          <div class="user-avatar-large">
            {{ (user.prenom || user.user?.prenom || 'U').charAt(0) }}
          </div>
          <div class="user-main-info">
            <h3 class="user-display-name">{{ user.prenom || user.user?.prenom }} {{ user.nom || user.user?.nom }}</h3>
            <div class="badges-row">
              <span class="badge role">{{ user.role || user.user?.role }}</span>
              <span class="badge status" :class="(user.is_actif || user.user?.is_actif) ? 'actif' : 'suspendu'">
                {{ (user.is_actif || user.user?.is_actif) ? 'Actif' : 'Suspendu' }}
              </span>
            </div>
          </div>
        </div>

        <div class="info-sections">
          <!-- Information Personnelle -->
          <div class="info-card">
            <h4 class="card-title">Informations Personnelles</h4>
            <div class="detail-list">
              <div class="detail-item">
                <span class="label">Email</span>
                <span class="value">{{ user.email || user.user?.email }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Téléphone</span>
                <span class="value">{{ user.telephone || user.user?.telephone || '+221 77 000 00 00' }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Date d'inscription</span>
                <span class="value">{{ user.date || 'Janvier 2026' }}</span>
              </div>
            </div>
          </div>

          <!-- Statistiques / Activité -->
          <div class="info-card">
            <h4 class="card-title">Résumé de l'Activité</h4>
            <div class="stats-mini-grid">
              <div class="stat-mini">
                <span class="stat-count">{{ (user.role || user.user?.role) === 'Agriculteur' ? '24' : '15' }}</span>
                <span class="stat-label">{{ (user.role || user.user?.role) === 'Agriculteur' ? 'Produits' : 'Commandes' }}</span>
              </div>
              <div class="stat-mini">
                <span class="stat-count">{{ (user.role || user.user?.role) === 'Agriculteur' ? '142' : '3.5M' }}</span>
                <span class="stat-label">{{ (user.role || user.user?.role) === 'Agriculteur' ? 'Ventes' : 'Dépenses' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="popup-footer">
        <div class="secondary-actions">
          <button class="btn-ghost">Contacter</button>
        </div>
        <div class="main-actions">
          <button class="btn-suspend" v-if="user.is_actif || user.user?.is_actif">Suspendre le compte</button>
          <button class="btn-activate" v-else>Réactiver le compte</button>
          <button class="btn-close" @click="closeModal">Fermer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  animation: fadeIn 0.3s ease;
}

.popup-modal {
  background: white;
  border-radius: 30px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.popup-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; }
.popup-title { font-size: 1.5rem; font-weight: 800; color: #111827; margin: 0; }
.close-btn { background: #f3f4f6; border: none; border-radius: 12px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #6b7280; }
.close-btn:hover { background: #fef2f2; color: #ef4444; }

.profile-banner {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: #f9fafb;
  padding: 2rem;
  border-radius: 24px;
  border: 1px solid #f3f4f6;
  margin-bottom: 2rem;
}

.user-avatar-large {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: #209216;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 2rem;
  box-shadow: 0 10px 15px -3px rgba(32, 146, 22, 0.2);
}

.user-display-name { font-size: 1.5rem; font-weight: 800; color: #111827; margin: 0 0 0.5rem 0; }
.badges-row { display: flex; gap: 0.75rem; }
.badge { padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.badge.role { background: #eff6ff; color: #3b82f6; }
.badge.status.actif { background: #ecfdf5; color: #059669; }
.badge.status.suspendu { background: #fef2f2; color: #dc2626; }

.info-sections { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.info-card { background: white; border: 1px solid #f3f4f6; border-radius: 20px; padding: 1.5rem; }
.card-title { font-size: 0.9rem; font-weight: 800; color: #4b5563; margin: 0 0 1.25rem 0; text-transform: uppercase; letter-spacing: 0.025em; }

.detail-list { display: flex; flex-direction: column; gap: 1rem; }
.detail-item { display: flex; flex-direction: column; gap: 0.25rem; }
.label { font-size: 0.75rem; font-weight: 600; color: #9ca3af; }
.value { font-size: 0.95rem; font-weight: 700; color: #111827; }

.stats-mini-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
.stat-mini { display: flex; flex-direction: column; align-items: center; padding: 1.25rem; background: #f9fafb; border-radius: 16px; border: 1px solid #f3f4f6; text-align: center; }
.stat-count { font-size: 1.5rem; font-weight: 800; color: #209216; }
.stat-label { font-size: 0.8rem; font-weight: 600; color: #6b7280; margin-top: 0.25rem; }

.popup-footer {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
}

.main-actions { display: flex; gap: 1rem; }
.btn-ghost { background: transparent; border: 1.5px solid #e5e7eb; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 700; color: #4b5563; cursor: pointer; }
.btn-close { background: #f3f4f6; border: none; padding: 0.75rem 2rem; border-radius: 12px; font-weight: 700; color: #4b5563; cursor: pointer; }
.btn-suspend { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 700; cursor: pointer; }
.btn-activate { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 700; cursor: pointer; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(40px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }

@media (max-width: 640px) {
  .info-sections { grid-template-columns: 1fr; }
  .profile-banner { flex-direction: column; text-align: center; }
}
</style>
