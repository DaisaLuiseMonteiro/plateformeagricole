<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth/auth_store'
import { uploadToCloudinary } from '@/utils/cloudinary'

const router = useRouter()
const authStore = useAuthStore()

const selectedRole = ref('client')
const photoFile = ref<File | null>(null)
const photoPreview = ref('')
const isLoading = ref(false)
const successMessage = ref('')

const form = ref({
  nom: '',
  prenom: '',
  email: '',
  telephone: '',
  mot_de_pass: '',
  confirmPassword: '',
  adresse: ''
})

const errors = ref<Record<string, string>>({})

onMounted(() => {
  selectedRole.value = sessionStorage.getItem('selectedRole') || 'client'
})

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    photoFile.value = target.files[0]
    photoPreview.value = URL.createObjectURL(photoFile.value)
  }
}

const handleSubmit = async () => {
  isLoading.value = true
  try {
    let photoUrl = ''
    if (photoFile.value) {
      photoUrl = await uploadToCloudinary(photoFile.value)
    }

    await authStore.register({
      ...form.value,
      role: selectedRole.value,
      photo: photoUrl
    })

    successMessage.value = 'Inscription réussie ! Redirection en cours...';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error: any) {
    // Les erreurs sont gérées directement par le store (fieldErrors)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
<div class="register-page">
    <!-- Image Hero - Gauche -->
    <div class="register-hero">
      <img :src="selectedRole === 'agriculteur' ? '/images/agriculteur.jpeg' : '/images/client.png'" alt="Paysage agricole" class="hero-image" />
      <div class="hero-overlay"></div>
      <div class="hero-text">
        <h2>Rejoignez notre communauté</h2>
      </div>
    </div>

    <!-- Formulaire - Droite -->
    <div class="register-form-section">
      <div class="register-form-container">
        <!-- Header -->
        <div class="register-header">
          <div class="logo-circle">
            <img src="/images/logo.jpeg" alt="Logo AgroConnect" class="logo-circle-img" />
          </div>
          <h1 class="register-title">AgroConnect</h1>
          <p class="register-subtitle">Créez votre compte {{ selectedRole === 'agriculteur' ? 'agricole' : 'client' }}</p>
        </div>

        <div v-if="successMessage" class="success-banner">{{ successMessage }}</div>

        <!-- Formulaire -->
        <form class="register-form" @submit.prevent="handleSubmit">
          <input type="hidden" name="role" :value="selectedRole" />
          
          <!-- Photo de profil -->
          <div class="form-group photo-upload-container">
            <label class="form-label">Photo de profil</label>
            <div class="photo-preview-wrapper" @click="$refs.fileInput.click()">
              <img v-if="photoPreview" :src="photoPreview" class="photo-preview" />
              <div v-else class="photo-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                  <circle cx="12" cy="13" r="4"/>
                </svg>
              </div>
              <div class="upload-overlay">
                <span>Changer</span>
              </div>
            </div>
            <input 
              type="file" 
              ref="fileInput" 
              class="hidden-input" 
              accept="image/*" 
              @change="onFileChange"
              style="display: none;"
            />
          </div>

          <!-- Prénom & Nom -->
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Prénom</label>
              <div class="input-wrapper">
                <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.prenom }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <input type="text" v-model="form.prenom" placeholder="Prénom" class="form-input" :class="{ 'input-error': authStore.fieldErrors.prenom }" />
              </div>
              <span v-if="authStore.fieldErrors.prenom" class="error-msg">{{ authStore.fieldErrors.prenom }}</span>
            </div>
            <div class="form-group">
              <label class="form-label">Nom</label>
              <div class="input-wrapper">
                <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.nom }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <input type="text" v-model="form.nom" placeholder="Nom" class="form-input" :class="{ 'input-error': authStore.fieldErrors.nom }" />
              </div>
              <span v-if="authStore.fieldErrors.nom" class="error-msg">{{ authStore.fieldErrors.nom }}</span>
            </div>
          </div>

          <!-- Email -->
          <div class="form-group">
            <label class="form-label">Email</label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.email }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9" />
              </svg>
              <input type="email" v-model="form.email" placeholder="votre@email.com" class="form-input" :class="{ 'input-error': authStore.fieldErrors.email }" />
            </div>
            <span v-if="authStore.fieldErrors.email" class="error-msg">{{ authStore.fieldErrors.email }}</span>
          </div>

          <!-- Téléphone -->
          <div class="form-group">
            <label class="form-label">Téléphone</label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.telephone }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <input type="tel" v-model="form.telephone" placeholder="+212 6XX XXX XXX" class="form-input" :class="{ 'input-error': authStore.fieldErrors.telephone }" />
            </div>
            <span v-if="authStore.fieldErrors.telephone" class="error-msg">{{ authStore.fieldErrors.telephone }}</span>
          </div>

          <!-- Adresse / Localisation -->
          <div class="form-group">
            <label class="form-label">
              {{ selectedRole === 'agriculteur' ? 'Localisation' : 'Adresse' }}
            </label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.adresse }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <input 
                type="text" 
                v-model="form.adresse" 
                :placeholder="selectedRole === 'agriculteur' ? 'Où se trouve votre champ ?' : 'Adresse'" 
                class="form-input" 
                :class="{ 'input-error': authStore.fieldErrors.adresse }"
              />
            </div>
            <span v-if="authStore.fieldErrors.adresse" class="error-msg">{{ authStore.fieldErrors.adresse }}</span>
          </div>

          <!-- Mot de passe -->
          <div class="form-group">
            <label class="form-label">Mot de passe</label>
            <div class="input-wrapper">
              <svg class="input-icon" :class="{ 'error-icon': authStore.fieldErrors.mot_de_pass }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input type="password" v-model="form.mot_de_pass" placeholder="Mot de passe" class="form-input" :class="{ 'input-error': authStore.fieldErrors.mot_de_pass }" />
            </div>
            <span v-if="authStore.fieldErrors.mot_de_pass" class="error-msg">{{ authStore.fieldErrors.mot_de_pass }}</span>
          </div>

          <!-- Confirmer mot de passe -->
          <div class="form-group">
            <label class="form-label">Confirmer le mot de passe</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input type="password" v-model="form.confirmPassword" placeholder="Confirmer mot de passe" class="form-input" />
            </div>
          </div>

          <!-- Bouton -->
          <button type="submit" class="register-button" :disabled="isLoading">
            {{ isLoading ? 'Inscription en cours...' : "S'inscrire" }}
          </button>
        </form>

        <!-- Lien connexion -->
        <p class="login-link">
          Déjà un compte ? <a href="/login" class="login-link-anchor">Se connecter</a>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ============================================================
   PAGE LAYOUT
   ============================================================ */
.register-page {
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
.register-hero {
  display: none;
  position: relative;
  width: 50%;
  min-height: 100vh;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .register-hero {
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
.register-form-section {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

@media (min-width: 1024px) {
  .register-form-section {
    width: 50%;
  }
}

.register-form-container {
  width: 100%;
  max-width: 520px;
}

/* ============================================================
   HEADER
   ============================================================ */
.register-header {
  text-align: center;
  margin-bottom: 2rem;
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
  margin-bottom: 0.75rem;
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

.register-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #209216;
  margin: 0 0 0.25rem 0;
}

.register-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0;
}

/* ============================================================
   FORM
   ============================================================ */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
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

.form-select {
  appearance: none;
  cursor: pointer;
}

/* ============================================================
   BUTTON
   ============================================================ */
.register-button {
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

.register-button:hover {
  background-color: #176c12;
  box-shadow: 0 4px 14px rgba(32, 146, 22, 0.35);
}

.register-button:active {
  transform: scale(0.98);
}

/* ============================================================
   LOGIN LINK
   ============================================================ */
.login-link {
  text-align: center;
  margin-top: 1.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.login-link-anchor {
  color: #209216;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s ease;
}

.login-link-anchor:hover {
  color: #176c12;
}

/* ============================================================
   PHOTO UPLOAD
   ============================================================ */
.photo-upload-container {
  align-items: center;
  margin-bottom: 1.5rem;
}

.photo-preview-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px dashed #d1d5db;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.photo-preview-wrapper:hover {
  border-color: #209216;
}

.photo-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  width: 40px;
  height: 40px;
  color: #9ca3af;
}

.upload-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.photo-preview-wrapper:hover .upload-overlay {
  opacity: 1;
}

.upload-overlay span {
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
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
