<script setup lang="ts">
import { useRouter } from 'vue-router';

const props = defineProps({
  message: {
    type: String,
    default: 'pour pouvoir commander'
  },
  verb: {
    type: String,
    default: 'commander'
  }
});

const emit = defineEmits(['close']);
const router = useRouter();

const closeModal = () => {
  emit('close');
};

const goToLogin = () => {
  router.push('/login');
  closeModal();
};
</script>

<template>
  <div class="popup-overlay" @click.self="closeModal">
    <div class="popup-modal">
      <div class="popup-icon">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="60" height="60">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      </div>
      
      <h2 class="popup-title">Connexion requise</h2>
      <p class="popup-message">
        <strong>Connectez-vous</strong> {{ message }}.
      </p>

      <div class="popup-actions">
        <button class="btn-login" @click="goToLogin">
          Connectez-vous pour {{ verb }}
        </button>
        
        <div class="register-hint">
          <p>Nouveau ici ?</p>
          <button class="btn-register" @click="router.push('/register'); closeModal()">
            Créez votre compte maintenant
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.popup-modal {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 32px;
  width: 90%;
  max-width: 420px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.popup-icon {
  width: 80px;
  height: 80px;
  background: #209216;
  color: white;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 16px rgba(32, 146, 22, 0.3);
}

.popup-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.75rem;
  letter-spacing: -0.5px;
}

.popup-message {
  font-size: 1.1rem;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.popup-message strong {
  color: #209216;
  font-weight: 700;
}

.popup-actions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.register-hint {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.register-hint p {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0;
}

.btn-login {
  background: #209216;
  color: white;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(32, 146, 22, 0.2);
}

.btn-login:hover {
  background: #1a7a12;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(32, 146, 22, 0.3);
}

.btn-register {
  background: transparent;
  color: #209216;
  border: 1px solid #209216;
  padding: 0.8rem 1.5rem;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-register:hover {
  background: #f0fdf4;
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
