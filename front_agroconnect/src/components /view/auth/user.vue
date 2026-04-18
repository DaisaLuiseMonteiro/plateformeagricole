<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const selectRole = (role: string) => {
  sessionStorage.setItem('selectedRole', role)
  router.push('/register')
}
</script>

<template>
  <div class="selection-page">
    <!-- ======================== IMAGE HERO - GAUCHE ======================== -->
    <div class="selection-hero">
      <img src="/images/client.png" alt="Agriculture et technologie" class="hero-image" />
    </div>

    <!-- ======================== CONTENU - DROITE ======================== -->
    <div class="selection-content">
      <div class="selection-container">

        <!-- Logo & Branding -->
        <div class="welcome-section">
          <div class="logo-circle">
            <svg class="logo-icon" fill="none" stroke="white" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 3C8.5 3 6 5.5 6 9c0 2.5 1.5 4.5 3.5 5.5V21h5v-6.5c2-1 3.5-3 3.5-5.5 0-3.5-2.5-6-6-6z" />
            </svg>
          </div>
          <h1 class="welcome-title">AgroConnect</h1>
          <p class="welcome-slogan">Le pont entre la terre et votre table</p>
          <p class="welcome-subtitle">Pour commencer, dites-nous qui vous êtes.</p>
        </div>

        <!-- Cartes de sélection de rôle -->
        <div class="role-cards">

          <!-- Carte Agriculteur -->
          <div @click="selectRole('agriculteur')" class="role-card farmer-card">
            <div class="role-icon-wrapper role-icon-farmer">
              <svg class="role-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="role-title">Je suis un Agriculteur</h3>
            <p class="role-description">
              Vendez vos produits directement, gérez vos stocks et augmentez vos revenus sans intermédiaires.
            </p>
            <span class="role-cta">Commencer →</span>
          </div>

          <!-- Carte Client -->
          <div @click="selectRole('client')" class="role-card">
            <div class="role-icon-wrapper role-icon-client">
              <svg class="role-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
            </div>
            <h3 class="role-title">Je suis un Client</h3>
            <p class="role-description">
              Accédez à des produits frais, locaux et de saison au meilleur prix, livrés chez vous.
            </p>
            <span class="role-cta">Commencer →</span>
          </div>

        </div>

        <!-- Lien de connexion -->
        <p class="login-redirect">
          Vous avez déjà un compte ?
          <a href="/login" class="login-redirect-link">Connectez-vous ici</a>
        </p>

      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ============================================================
   PAGE LAYOUT
   ============================================================ */
.selection-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: rgb(238, 247, 241);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  color: #1a1a1a;
}

/* ============================================================
   HERO (LEFT PANEL)
   ============================================================ */
.selection-hero {
  display: none;
  position: relative;
  width: 50%;
  height: 100vh;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .selection-hero {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.hero-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ============================================================
   LOGO & BRANDING (RIGHT PANEL)
   ============================================================ */
.logo-circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #209216;
  box-shadow: 0 4px 14px rgba(32, 146, 22, 0.35);
  margin-bottom: 0.75rem;
}

.logo-icon {
  width: 28px;
  height: 28px;
}

/* ============================================================
   CONTENT (RIGHT PANEL)
   ============================================================ */
.selection-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

@media (min-width: 1024px) {
  .selection-content {
    width: 50%;
  }
}

.selection-container {
  width: 100%;
  max-width: 540px;
}

/* ============================================================
   WELCOME SECTION
   ============================================================ */
.welcome-section {
  text-align: center;
  margin-bottom: 2.5rem;
}

.welcome-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #209216;
  margin: 0 0 0.25rem 0;
}

.welcome-slogan {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0 0 1.25rem 0;
}

.welcome-subtitle {
  font-size: 1rem;
  color: #374151;
  font-weight: 500;
  margin: 0;
}

/* ============================================================
   ROLE CARDS
   ============================================================ */
.role-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 2rem;
}

@media (max-width: 600px) {
  .role-cards {
    grid-template-columns: 1fr;
  } 
}

.role-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.75rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  background-color: #ffffff;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.role-card:hover {
  border-color: #209216;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(32, 146, 22, 0.15);
}

.farmer-card:hover {
  border-color: #209216;
  box-shadow: 0 8px 24px rgba(166, 124, 82, 0.15);
}

.role-card:hover .role-cta {
  color: #209216;
}

.farmer-card:hover .role-cta {
  color: #209216;
}

/* ============================================================
   ROLE ICON
   ============================================================ */
.role-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 14px;
  margin-bottom: 1rem;
}

.role-icon-farmer {
  background-color: #ecfdf5;
  color: #209216;
}

.role-icon-client {
  background-color: #eff6ff;
  color: #209216;
}

.role-card:hover .role-icon-farmer {
  background-color: #A67C52;
  color: #ffffff;
}

.role-card:hover .role-icon-client {
  background-color: #209216;
  color: #ffffff;
}

.role-icon {
  width: 28px;
  height: 28px;
  transition: color 0.25s ease;
}

.role-icon-wrapper {
  transition: background-color 0.25s ease, color 0.25s ease;
}

/* ============================================================
   ROLE TEXT
   ============================================================ */
.role-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.role-description {
  font-size: 0.82rem;
  line-height: 1.5;
  color: #6b7280;
  margin: 0 0 1rem 0;
}

.role-cta {
  font-size: 0.85rem;
  font-weight: 600;
  color: #9ca3af;
  transition: color 0.25s ease;
}

/* ============================================================
   LOGIN REDIRECT
   ============================================================ */
.login-redirect {
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.login-redirect-link {
  color: #209216;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s ease;
}

.login-redirect-link:hover {
  color: #176c12;
}
</style>
