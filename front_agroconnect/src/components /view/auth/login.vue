<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/auth_store'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const mot_de_pass = ref('')
const isLoading = ref(false)

// Connexion
const handleLogin = async () => {
  isLoading.value = true
  try {
    const data = await authStore.login(email.value, mot_de_pass.value)
    
    // Redirection selon le rôle
    if (data.role === 'admin') {
      router.push('/admin/dashboard')
    } else if (data.role === 'agriculteur') {
      router.push('/agriculteur/dashboard')
    } else {
      router.push('/')
    }
  } catch (error: any) {
    // Les erreurs sont gérées directement par le store (fieldErrors)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <!-- Image Hero - Gauche -->
    <div class="login-hero">
      <img src="/images/client.png" alt="Paysage agricole" class="hero-image" />
      <div class="hero-overlay"></div>
      <div class="hero-text">
        <h2>Cultivons l'avenir ensemble</h2>
      </div>
    </div>

    <!-- Formulaire - Droite -->
    <div class="login-form-section">
      <div class="login-form-container">
        <!-- Logo -->
        <div class="login-header">
          <div class="logo-circle">
            <img src="/images/logo.jpeg" alt="Logo AgroConnect" class="logo-circle-img" />
          </div>
          <h1 class="login-title">Connectez-vous</h1>
        </div>

        <!-- Formulaire -->
        <form class="login-form" @submit.prevent="handleLogin">
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

          <!-- Mot de passe -->
          <div class="form-group">
            <label class="form-label">Mot de passe</label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.mot_de_pass }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input 
                type="password" 
                v-model="mot_de_pass" 
                placeholder="••••••••" 
                class="form-input" 
                :class="{ 'input-error': authStore.fieldErrors.mot_de_pass }"
              />
            </div>
            <span v-if="authStore.fieldErrors.mot_de_pass" class="error-msg">{{ authStore.fieldErrors.mot_de_pass }}</span>
          </div>

          <!-- Bouton -->
          <button type="submit" class="login-button" :disabled="isLoading">
            {{ isLoading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <!-- Footer -->
        <div class="login-footer">
          <p class="register-text">
            Pas encore de compte ? <a href="/user" class="register-link">Créer un compte</a>
          </p>
          <a href="/reset-password" class="forgot-password-link">Mot de passe oublié ?</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ============================================================
   PAGE LAYOUT
   ============================================================ */
.login-page {
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
.login-hero {
  display: none;
  position: relative;
  width: 50%;
  min-height: 100vh;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .login-hero {
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
.login-form-section {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

@media (min-width: 1024px) {
  .login-form-section {
    width: 50%;
  }
}

.login-form-container {
  width: 100%;
  max-width: 420px;
}

/* ============================================================
   HEADER (LOGO + TITLE)
   ============================================================ */
.login-header {
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

.login-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #209216;
  margin: 0;
}

/* ============================================================
   FORM
   ============================================================ */
.login-form {
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

/* ============================================================
   BUTTON
   ============================================================ */
.login-button {
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

.login-button:hover {
  background-color: #176c12;
  box-shadow: 0 4px 14px rgba(32, 146, 22, 0.35);
}

.login-button:active {
  transform: scale(0.98);
}

/* ============================================================
   LOGIN FOOTER
   ============================================================ */
.login-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1.5rem;
  font-size: 0.85rem;
  gap: 0.75rem;
}

.register-text {
  color: #1a1a1a;
  margin: 0;
}

.register-link {
  color: #209216;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s ease;
}

.register-link:hover {
  color: #176c12;
}

.forgot-password-link {
  color: #dc2626;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.forgot-password-link:hover {
  opacity: 0.8;
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

@media (max-width: 480px) {
  .login-footer {
    flex-direction: column;
    gap: 0.75rem;
    text-align: center;
  }
}
</style>