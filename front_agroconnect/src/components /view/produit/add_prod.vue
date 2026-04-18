<script setup lang="ts">
import { ref, computed } from 'vue'
import { useProduitStore } from '@/stores/produit/produit_store'
import { useAuthStore } from '@/stores/auth/auth_store'
import { uploadToCloudinary } from '@/utils/cloudinary'

const emit = defineEmits(['close', 'success'])
const produitStore = useProduitStore()
const authStore = useAuthStore()

const form = ref({
  prix_unitaire: '',
  description: '',
  quantite_stock: '',
  photo: '',
  categorie: '',
  agriculteur_id: authStore.user?.agriculteur_id || ''
})

const errors = ref<Record<string, string>>({})
const isUploading = ref(false)
const imageSelected = ref(false)

const categories = [
  { value: 'legume', label: 'Légume' },
  { value: 'cereale', label: 'Céréale' },
  { value: 'fruit', label: 'Fruit' }
]

const validate = (): boolean => {
  errors.value = {}

  // Validation du prix
  if (!form.value.prix_unitaire) {
    errors.value.prix_unitaire = 'Le prix est obligatoire pour vendre votre produit.'
  } else {
    const prix = Number(form.value.prix_unitaire)
    if (isNaN(prix)) {
      errors.value.prix_unitaire = 'Veuillez saisir un nombre (ex: 1500).'
    } else if (prix <= 0) {
      errors.value.prix_unitaire = 'Le prix doit être un nombre positif.'
    }
  }

  // Validation de la quantité
  if (!form.value.quantite_stock) {
    errors.value.quantite_stock = 'Indiquez la quantité que vous avez en stock.'
  } else {
    const stock = Number(form.value.quantite_stock)
    if (isNaN(stock) || !Number.isInteger(stock)) {
      errors.value.quantite_stock = 'La quantité doit être un nombre entier.'
    } else if (stock < 0) {
      errors.value.quantite_stock = 'Le stock ne peut pas être négatif.'
    }
  }

  // Validation de la catégorie
  if (!form.value.categorie) {
    errors.value.categorie = 'Veuillez choisir une catégorie pour classer le produit.'
  }

  // Validation de la description
  if (!form.value.description.trim()) {
    errors.value.description = 'Donnez quelques détails sur votre produit pour les clients.'
  } else if (form.value.description.trim().length < 10) {
    errors.value.description = 'La description doit faire au moins 10 caractères.'
  }

  // Validation de la photo
  if (!form.value.photo) {
    errors.value.photo = "Ajoutez une photo pour mettre en avant votre produit."
  } else if (isUploading.value) {
    errors.value.photo = "Attendez la fin de l'envoi de l'image avant de valider."
  }

  return Object.keys(errors.value).length === 0
}

const localPreview = ref('');

// Fonction utilitaire pour compresser l'image avant l'upload
const compressImage = (file: File): Promise<Blob> => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (event) => {
      const img = new Image();
      img.src = event.target?.result as string;
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const MAX_WIDTH = 1200; // Largeur max raisonnable pour le web
        const MAX_HEIGHT = 1200;
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }

        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx?.drawImage(img, 0, 0, width, height);
        
        canvas.toBlob((blob) => {
          if (blob) resolve(blob);
        }, 'image/jpeg', 0.7); // Compression JPEG avec qualité 70%
      };
    };
  });
};

const handleFileUpload = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  // Création d'une prévisualisation locale instantanée
  localPreview.value = URL.createObjectURL(file);
  form.value.photo = localPreview.value; 
  
  console.log('Traitement et compression de l\'image...');
  isUploading.value = true
  imageSelected.value = true
  errors.value.photo = ''

  try {
    const compressedBlob = await compressImage(file);
    // On doit transformer le blob en File pour Cloudinary si besoin, 
    // ou vérifier si uploadToCloudinary accepte un Blob (FormData accepte les deux)
    const compressedFile = new File([compressedBlob], file.name, { type: 'image/jpeg' });
    
    console.log('Début du téléchargement vers Cloudinary (taille réduite)...');
    const url = await uploadToCloudinary(compressedFile)
    form.value.photo = url
    console.log('Téléchargement réussi :', url);
  } catch (err: any) {
    console.error('Erreur de téléchargement :', err);
    errors.value.photo = "Erreur lors du téléchargement de l'image."
    imageSelected.value = false
    localPreview.value = '';
    form.value.photo = '';
  } finally {
    isUploading.value = false
  }
}

const isSubmitting = computed(() => produitStore.loading)

const submitForm = async () => {
  console.log('--- Tentative de soumission ---');
  
  if (isUploading.value) {
    console.warn('Action annulée : l\'image est encore en cours d\'envoi.');
    return;
  }
  
  const isValid = validate();
  console.log('Résultat validation :', isValid);
  
  if (!isValid) {
    console.warn('Erreurs de validation :', errors.value);
    return;
  }

  console.log('Préparation des données pour le store...');
  const payload = {
    prix_unitaire: Number(form.value.prix_unitaire),
    description: form.value.description,
    quantite_stock: Number(form.value.quantite_stock),
    photo: form.value.photo,
    categorie: form.value.categorie,
    agriculteur_id: form.value.agriculteur_id
  };
  console.log('Payload :', payload);

  produitStore.resetMessages()

  try {
    console.log('Appel de produitStore.ajouterProduit...');
    await produitStore.ajouterProduit(payload)
    console.log('Réponse du serveur reçue avec succès.');

    emit('success')
    emit('close')
  } catch (err: any) {
    console.error('ERREUR lors de l\'ajout du produit :', err);
  }
}

const closeModal = () => {
  produitStore.resetMessages()
  emit('close')
}
</script>

<template>
  <div class="popup-overlay" @click.self="closeModal">
    <div class="popup-modal">
      <!-- Header -->
      <div class="popup-header">
        <h2 class="popup-title">Ajouter un produit</h2>
        <button class="close-btn" @click="closeModal">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="22" height="22">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Error message global -->
      <div v-if="produitStore.error" class="alert alert-error">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ produitStore.error }}
      </div>

      <!-- Success message -->
      <div v-if="produitStore.successMessage" class="alert alert-success">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ produitStore.successMessage }}
      </div>

      <!-- Form -->
      <form @submit.prevent="submitForm" class="popup-form">
        <!-- Upload Section -->
        <div class="form-group full-width">
          <label class="form-label">Photo du produit <span class="required">*</span></label>
          <div class="upload-container" :class="{ 'has-image': form.photo, 'is-uploading': isUploading, 'error': errors.photo }">
            <input
              type="file"
              accept="image/*"
              class="file-input"
              @change="handleFileUpload"
              id="product-image"
            />
            <label for="product-image" class="upload-label">
              <div v-if="!form.photo && !isUploading" class="upload-placeholder">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="40" height="40">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Cliquez ou glissez une image ici</span>
                <p>Format JPG, PNG (Max 5MB)</p>
              </div>
              
              <div v-if="form.photo" class="image-preview-wrapper">
                <img :src="form.photo" class="image-preview" alt="Prévisualisation" />
                <div class="change-overlay">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Changer l'image</span>
                </div>
              </div>
            </label>
            <span v-if="errors.photo" class="field-error center-error">{{ errors.photo }}</span>
          </div>
        </div>

        <div class="form-grid">
          <!-- Prix unitaire -->
          <div class="form-group">
            <label class="form-label">Prix unitaire (FCFA) <span class="required">*</span></label>
            <input
              v-model="form.prix_unitaire"
              type="text"
              class="form-input"
              :class="{ 'input-error': errors.prix_unitaire }"
              placeholder="Ex: 1500"
            />
            <span v-if="errors.prix_unitaire" class="field-error">{{ errors.prix_unitaire }}</span>
          </div>

          <!-- Quantité en stock -->
          <div class="form-group">
            <label class="form-label">Quantité en stock <span class="required">*</span></label>
            <input
              v-model="form.quantite_stock"
              type="text"
              class="form-input"
              :class="{ 'input-error': errors.quantite_stock }"
              placeholder="Ex: 500"
            />
            <span v-if="errors.quantite_stock" class="field-error">{{ errors.quantite_stock }}</span>
          </div>

          <div class="form-group full-width">
            <label class="form-label">Description du produit <span class="required">*</span></label>
            <textarea
              v-model="form.description"
              class="form-input form-textarea"
              :class="{ 'input-error': errors.description }"
              placeholder="Décrivez votre produit (ex: Tomates fraîches du jardin...)"
            ></textarea>
            <span v-if="errors.description" class="field-error">{{ errors.description }}</span>
          </div>

          <!-- Catégorie -->
          <div class="form-group full-width">
            <label class="form-label">Catégorie <span class="required">*</span></label>
            <select
              v-model="form.categorie"
              class="form-input"
              :class="{ 'input-error': errors.categorie }"
            >
              <option value="" disabled>Choisir une catégorie</option>
              <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
            </select>
            <span v-if="errors.categorie" class="field-error">{{ errors.categorie }}</span>
          </div>
        </div>

        <!-- Buttons -->
        <div class="form-actions">
          <button type="button" class="btn-cancel" @click="closeModal">Annuler</button>
          <button type="submit" class="btn-submit" :disabled="isSubmitting || isUploading">
            <svg v-if="isSubmitting || isUploading" class="spinner" viewBox="0 0 24 24" width="18" height="18">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4" stroke-dashoffset="10" />
            </svg>
            <span v-if="isUploading">Téléchargement...</span>
            <span v-else-if="isSubmitting">Ajout en cours...</span>
            <span v-else>Ajouter le produit</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.popup-modal {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 750px;
  max-height: 95vh;
  overflow-y: auto;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideUp 0.3s ease;
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.popup-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.close-btn {
  background: #f3f4f6;
  border: none;
  border-radius: 12px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #fef2f2;
  color: #ef4444;
  transform: rotate(90deg);
}

/* Upload Zone Styles */
.upload-container {
  position: relative;
  border: 2px dashed #e5e7eb;
  border-radius: 16px;
  background: #f9fafb;
  height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  margin-bottom: 1rem;
}

.upload-container:hover {
  border-color: #209216;
  background: #f0fdf4;
}

.upload-container.has-image {
  border-style: solid;
  border-color: #e5e7eb;
}

.upload-container.is-uploading {
  border-color: #209216;
  pointer-events: none;
}

.upload-container.error {
  border-color: #ef4444;
  background: #fff5f5;
}

.file-input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  text-align: center;
}

.has-image .upload-label {
  padding: 0;
}

.upload-placeholder {
  padding: 1.5rem;
  color: #9ca3af;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.upload-placeholder span {
  font-weight: 700;
  color: #4b5563;
  font-size: 1rem;
}

.upload-placeholder p {
  font-size: 0.8rem;
  color: #9ca3af;
}

.upload-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #209216;
  font-weight: 700;
}

.dynamic-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(32, 146, 22, 0.1);
  border-top-color: #209216;
  border-radius: 50%;
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  to { transform: rotate(360deg); }
}

.image-preview-wrapper {
  position: relative;
  width: 100%;
  height: 320px;
  border-radius: 12px;
  overflow: hidden;
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #f7faf8; /* Dark background for professional look with contain */
  transition: transform 0.3s ease;
  display: block;
}

.change-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: white;
  font-weight: 700;
  opacity: 0;
  transition: opacity 0.2s;
  backdrop-filter: blur(2px);
}

.upload-container:hover .change-overlay {
  opacity: 1;
}

/* Alerts */
.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: 14px;
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.alert-error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.alert-success {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

/* Form */
.popup-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: #c3d5f1;
}

.required {
  color: #ef4444;
}

.form-input {
  padding: 0.85rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  font-size: 0.95rem;
  color: #111827;
  background: #f9fafb;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
  outline: none;
}

.form-input:focus {
  border-color: #209216;
  background: white;
  box-shadow: 0 0 0 4px rgba(32, 146, 22, 0.1);
}

.input-error {
  border-color: #ef4444 !important;
  background: #fff5f5 !important;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

select.form-input {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1.25rem center;
  padding-right: 3rem;
}

.field-error {
  font-size: 0.8rem;
  color: #ef4444;
  font-weight: 600;
  margin-top: 0.25rem;
}

.center-error {
  text-align: center;
  width: 100%;
}

/* Buttons */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
}

.btn-cancel {
  padding: 0.85rem 1.75rem;
  border-radius: 14px;
  border: 1.5px solid #e5e7eb;
  background: white;
  color: #4b5563;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.btn-submit {
  padding: 0.85rem 2rem;
  border-radius: 14px;
  border: none;
  background: #209216;
  color: white;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-submit:hover:not(:disabled) {
  background: #1a7a12;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(32, 146, 22, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .popup-modal {
    width: 95%;
    padding: 1.5rem;
  }
  .form-grid {
    grid-template-columns: 1fr;
  }
  .image-preview-wrapper {
    height: 200px;
  }
}
</style>
