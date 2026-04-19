<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/auth_store'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const nouveau_mot_de_pass = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const successMessage = ref('')

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// Réinitialisation
const handleReset = async () => {
  isLoading.value = true
  try {
    await authStore.resetPassword(email.value, nouveau_mot_de_pass.value)
    successMessage.value = 'Mot de passe réinitialisé avec succès'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error: any) {
    // Les erreurs sont gérées directement par le store (fieldErrors)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="reset-page">
    <!-- Image Hero - Gauche -->
    <div class="reset-hero">
      <img src="/images/client.png" alt="Paysage agricole" class="hero-image" />
      <div class="hero-overlay"></div>
      <div class="hero-text">
        <h2>Réinitialisez votre mot de passe</h2>
      </div>
    </div>

    <!-- Formulaire - Droite -->
    <div class="reset-form-section">
      <div class="reset-form-container">
        <!-- Header -->
        <div class="reset-header">
          <div class="logo-circle">
            <img src="/images/logo.jpeg" alt="Logo AgroConnect" class="logo-circle-img" />
          </div>
          <h1 class="reset-title">Réinitialisation du mot de passe</h1>
        </div>

        <div v-if="successMessage" class="success-banner">{{ successMessage }}</div>

        <!-- Formulaire -->
        <form class="reset-form" @submit.prevent="handleReset">
          <!-- Email -->
          <div class="form-group">
            <label class="form-label">Email</label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.email }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9" />
              </svg>
              <input 
                type="email" 
                v-model="email" 
                placeholder="votre@email.com" 
                class="form-input" 
                :class="{ 'input-error': authStore.fieldErrors.email }"
              />
            </div>
            <span v-if="authStore.fieldErrors.email" class="error-msg">{{ authStore.fieldErrors.email }}</span>
          </div>

          <!-- Nouveau mot de passe -->
          <div class="form-group">
            <label class="form-label">Nouveau mot de passe</label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.nouveau_mot_de_pass }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input 
                :type="showPassword ? 'text' : 'password'" 
                v-model="nouveau_mot_de_pass" 
                placeholder="••••••••" 
                class="form-input password-input" 
                :class="{ 'input-error': authStore.fieldErrors.nouveau_mot_de_pass }"
              />
              <button 
                type="button" 
                class="toggle-password" 
                @click="togglePassword"
                attr-label="Toggle password visibility"
              >
                <svg v-if="!showPassword" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                </svg>
              </button>
            </div>
            <span v-if="authStore.fieldErrors.nouveau_mot_de_pass" class="error-msg">{{ authStore.fieldErrors.nouveau_mot_de_pass }}</span>
          </div>

          <!-- Bouton -->
          <button type="submit" class="reset-button" :disabled="isLoading">
            {{ isLoading ? 'Réinitialisation...' : 'Réinitialiser' }}
          </button>
        </form>

        <!-- Lien retour -->
        <p class="back-link">
          <a href="/login" class="back-link-anchor">Retour à la connexion</a>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ============================================================
   PAGE LAYOUT
   ============================================================ */
.reset-page {
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
.reset-hero {
  display: none;
  position: relative;
  width: 50%;
  min-height: 100vh;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .reset-hero {
    display: flex;
  }
}

.hero-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(32, 146, 22, 0.15) 0%,
    rgba(0, 0, 0, 0.05) 100%
  );
}

.hero-text {
  position: absolute;
  bottom: 2.5rem;
  left: 2.5rem;
  right: 2.5rem;
  color: #ffffff;
}

.hero-text h2 {
  font-size: 1.85rem;
  font-weight: 700;
  line-height: 1.3;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
  margin: 0;
}

/* ============================================================
   FORM SECTION (RIGHT PANEL)
   ============================================================ */
.reset-form-section {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

@media (min-width: 1024px) {
  .reset-form-section {
    width: 50%;
  }
}

.reset-form-container {
  width: 100%;
  max-width: 420px;
}

/* ============================================================
   HEADER
   ============================================================ */
.reset-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #209216;
  box-shadow: 0 4px 14px rgba(32, 146, 22, 0.35);
  margin-bottom: 1rem;
}

.logo-icon {
  width: 28px;
  height: 28px;
}

.logo-circle-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.reset-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #209216;
  margin: 0;
}

/* ============================================================
   FORM
   ============================================================ */
.reset-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #9ca3af;
  pointer-events: none;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 0.75rem 0 2.5rem;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #1a1a1a;
  background-color: #ffffff;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-input:focus {
  border-color: #209216;
  box-shadow: 0 0 0 3px rgba(32, 146, 22, 0.15);
}

.password-input {
  padding-right: 2.75rem;
}

.toggle-password {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: #209216;
}

.toggle-password svg {
  width: 20px;
  height: 20px;
}

/* ============================================================
   BUTTON
   ============================================================ */
.reset-button {
  width: 100%;
  height: 44px;
  margin-top: 0.5rem;
  border: none;
  border-radius: 8px;
  background-color: #209216;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 8px rgba(32, 146, 22, 0.25);
}

.reset-button:hover {
  background-color: #176c12;
  box-shadow: 0 4px 14px rgba(32, 146, 22, 0.35);
}

.reset-button:active {
  transform: scale(0.98);
}

/* ============================================================
   BACK LINK
   ============================================================ */
.back-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
}

.back-link-anchor {
  color: #209216;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s ease;
}

.back-link-anchor:hover {
  color: #176c12;
}

/* ============================================================
   ERROR HANDLING
   ============================================================ */
.error-msg {
  color: #dc2626;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 0.25rem;
  animation: slideIn 0.2s ease;
}

.input-error {
  border-color: #dc2626 !important;
  background-color: #fffafb !important;
}

.error-icon {
  color: #dc2626 !important;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.success-banner {
  background-color: #d1fae5;
  color: #065f46;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
  animation: slideIn 0.3s ease;
}
</style>