<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth/auth_store';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submitted'): void;
}>();

const authStore = useAuthStore();
const nom_produit = ref<string>('');
const quantite = ref<number>(1);
const description = ref<string>('');
const isSubmitting = ref<boolean>(false);
const showSuccess = ref<boolean>(false);

const submitForm = async () => {
  if (!authStore.isAuthenticated) {
    alert('Veuillez vous connecter pour envoyer une demande.');
    return;
  }
  if (!nom_produit.value || quantite.value <= 0) {
    alert('Veuillez remplir tous les champs obligatoires.');
    return;
  }

  isSubmitting.value = true;
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
    const response = await fetch(`${API_BASE_URL}/production/demande`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        nom_produit: nom_produit.value,
        quantite: quantite.value,
        description: description.value,
        client_id: authStore.user?.id
      }),
    });

    if (response.ok) {
      showSuccess.value = true;
      nom_produit.value = '';
      quantite.value = 1;
      description.value = '';
      emit('submitted');
      setTimeout(() => {
        closeModal();
      }, 3000);
    } else {
      const errorData = await response.json();
      alert(`Erreur : ${errorData.detail || 'Une erreur est survenue.'}`);
    }
  } catch (error) {
    console.error('Erreur lors de la soumission :', error);
    alert('Erreur de connexion au serveur.');
  } finally {
    isSubmitting.value = false;
  }
};

const closeModal = () => {
  showSuccess.value = false;
  emit('close');
};
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        
        <div v-if="!showSuccess">
          <h2 class="modal-title">Production sur commande</h2>
          <p class="modal-subtitle">
            Vous ne trouvez pas ce que vous cherchez ? Demandez une production personnalisée à nos agriculteurs.
          </p>

          <form @submit.prevent="submitForm" class="production-form">
            <div class="form-group">
              <label class="form-label">Nom du produit souhaité <span class="required">*</span></label>
              <input 
                v-model="nom_produit" 
                type="text" 
                placeholder="Ex: Tomates Cerises" 
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Quantité souhaitée (en kg/unité) <span class="required">*</span></label>
              <input 
                v-model.number="quantite" 
                type="number" 
                min="1" 
                class="form-input"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Détails supplémentaires</label>
              <textarea 
                v-model="description" 
                placeholder="Couleur, variété, urgence..." 
                class="form-textarea"
              ></textarea>
            </div>

            <button type="submit" class="submit-btn" :disabled="isSubmitting">
              {{ isSubmitting ? 'Envoi en cours...' : 'Envoyer la demande' }}
            </button>
          </form>
        </div>

        <div v-else class="success-message">
          <div class="success-icon">✓</div>
          <h3>Demande envoyée !</h3>
          <p>L'administration a reçu votre demande. Nous allons contacter des agriculteurs capables de produire cela pour vous.</p>
          <p class="notif-hint">Vous recevrez une notification dès qu'un agriculteur accepte votre commande.</p>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalAppear 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalAppear {
  from { opacity: 0; transform: scale(0.9) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.close-btn {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: #f3f4f6;
  border: none;
  font-size: 1.5rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
  color: #111827;
  transform: rotate(90deg);
}

.modal-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 0.5rem;
  text-align: center;
}

.modal-subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.95rem;
  line-height: 1.5;
}

.production-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: #374151;
}

.required {
  color: #ef4444;
}

.form-input, .form-textarea {
  padding: 0.8rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f9fafb;
}

.form-input:focus, .form-textarea:focus {
  border-color: #209216;
  background: white;
  outline: none;
  box-shadow: 0 0 0 4px rgba(32, 146, 22, 0.1);
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.submit-btn {
  background: #209216;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  background: #1a7a12;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(32, 146, 22, 0.3);
}

.submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.success-message {
  text-align: center;
  padding: 1rem 0;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: #ecfdf5;
  color: #10b981;
  font-size: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.success-message h3 {
  font-size: 1.5rem;
  color: #065f46;
  margin-bottom: 1rem;
}

.success-message p {
  color: #374151;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.notif-hint {
  font-size: 0.85rem;
  background: #fef3c7;
  color: #92400e;
  padding: 0.75rem;
  border-radius: 8px;
  font-style: italic;
}
</style>
