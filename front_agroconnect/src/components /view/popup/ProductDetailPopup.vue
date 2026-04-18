<script setup lang="ts">
const props = defineProps({
  product: {
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
        <h2 class="popup-title">Détails du produit</h2>
        <button class="close-btn" @click="closeModal">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="product-detail-layout">
        <!-- Image Section -->
        <div class="detail-image-section">
          <div class="main-image-wrapper">
            <img :src="product.image || product.photo" :alt="product.name || product.description" class="detail-image" />
          </div>
          <div class="status-badge-container">
            <span class="status-badge" :class="product.statut_publication?.toLowerCase().replace('_', '-')">
              {{ product.statut_publication || 'PUBLIE' }}
            </span>
          </div>
        </div>

        <!-- Info Section -->
        <div class="detail-info-section">
          <div class="info-group">
            <span class="info-label">Description</span>
            <h3 class="info-value">{{ product.description }}</h3>
          </div>

          <div class="info-grid">
            <div class="info-group">
              <span class="info-label">Prix Unitaire</span>
              <div class="price-tag">{{ product.prix_unitaire }} FCFA</div>
            </div>
            <div class="info-group">
              <span class="info-label">Stock Disponible</span>
              <div class="stock-tag">{{ product.quantite_stock }} unités</div>
            </div>
            <div class="info-group">
              <span class="info-label">Catégorie</span>
              <div class="category-tag">{{ product.categorie }}</div>
            </div>
            <div class="info-group">
              <span class="info-label">Date d'ajout</span>
              <div class="date-tag">{{ product.date || '18 Avril 2026' }}</div>
            </div>
          </div>

          <div class="info-group full-width">
            <span class="info-label">Description détaillée</span>
            <p class="description-text">
              {{ product.fullDescription || product.description || 'Aucune description détaillée disponible.' }}
            </p>
          </div>
        </div>
      </div>

      <div class="popup-footer">
        <button class="btn-primary" @click="closeModal">Fermer</button>
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
  border-radius: 24px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  border-bottom: 1px solid #f3f4f6;
  padding-bottom: 1.5rem;
}

.popup-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.close-btn {
  background: #f3f4f6;
  border: none;
  border-radius: 12px;
  width: 44px;
  height: 44px;
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

.product-detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem;
}

.detail-image-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.main-image-wrapper {
  width: 100%;
  aspect-ratio: 1/1;
  border-radius: 20px;
  overflow: hidden;
  background: #f9fafb;
  border: 1px solid #f3f4f6;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.detail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.detail-image:hover {
  transform: scale(1.05);
}

.status-badge-container {
  display: flex;
  justify-content: center;
}

.status-badge {
  padding: 0.6rem 1.5rem;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.publié { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; }
.status-badge.en-attente { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.status-badge.rejeté { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }

.detail-info-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.info-value {
  font-size: 1.35rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.price-tag {
  font-size: 1.5rem;
  font-weight: 800;
  color: #209216;
}

.stock-tag, .category-tag, .date-tag {
  font-size: 1rem;
  font-weight: 600;
  color: #4b5563;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border-radius: 12px;
  display: inline-block;
  width: fit-content;
}

.description-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #4b5563;
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 16px;
  border: 1px solid #f3f4f6;
}

.popup-footer {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  padding: 0.85rem 2.5rem;
  border-radius: 14px;
  background: #209216;
  color: white;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(32, 146, 22, 0.2);
}

.btn-primary:hover {
  background: #1a7a12;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(32, 146, 22, 0.3);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@media (max-width: 768px) {
  .product-detail-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .popup-modal {
    padding: 1.5rem;
  }
}
</style>
