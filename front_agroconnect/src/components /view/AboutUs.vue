<template>
  <div class="about-container">
    <Header />
    
    <main class="about-content">
      <section class="hero-section">
        <h1 class="title">À propos d'AgroConnect</h1>
        <p class="subtitle">La plateforme qui connecte directement producteurs et consommateurs pour une agriculture durable et équitable.</p>
      </section>

      <section class="info-grid">
        <div class="info-card fade-in">
          <h2>🌱 Notre Mission</h2>
          <p>
            AgroConnect est une initiative visant à dynamiser le secteur agricole sénégalais en supprimant les intermédiaires inutiles. 
            Nous permettons aux agriculteurs de fixer leurs propres prix et aux consommateurs d'accéder à des produits frais et locaux.
          </p>
        </div>

        <div class="info-card fade-in">
          <h2>🌟 Vos Privilèges</h2>
          <ul>
            <li><strong>Pour les Clients :</strong> Accès direct à la fraîcheur, prix justes, et traçabilité totale des produits.</li>
            <li><strong>Pour les Agriculteurs :</strong> Meilleure rentabilité, gestion simplifiée des stocks, et visibilité nationale.</li>
            <li><strong>Soutien Local :</strong> Chaque achat soutient directement une famille d'agriculteurs au Sénégal.</li>
          </ul>
        </div>
      </section>

      <section class="guide-section fade-in">
        <h2>🛍️ Comment commander ?</h2>
        <div class="steps-container">
          <div class="step">
            <span class="step-num">1</span>
            <h3>Explorez</h3>
            <p>Naviguez à travers nos catégories : Fruits, Légumes ou Céréales.</p>
          </div>
          <div class="step">
            <span class="step-num">2</span>
            <h3>Sélectionnez</h3>
            <p>Ajoutez vos produits préférés au panier après vous être connecté.</p>
          </div>
          <div class="step">
            <span class="step-num">3</span>
            <h3>Validez</h3>
            <p>Confirmez votre commande et l'un de nos agriculteurs préparera vos produits avec soin.</p>
          </div>
        </div>
      </section>

      <section class="cta-section fade-in">
        <h2>Rejoignez l'aventure !</h2>
        <p>Pas encore inscrit ? Rejoignez des milliers de Sénégalais qui transforment l'agriculture.</p>
        <router-link to="/login" class="cta-button">S'inscrire / Se connecter</router-link>
      </section>

      <section class="contact-section fade-in">
        <h2>📞 Service Client & Aide</h2>
        <p>Besoin d'assistance ? Nos experts sont là pour vous aider.</p>
        <div class="contact-card">
          <p><strong>Administrateur :</strong> Monteiro DLM</p>
          <p><strong>Téléphone :</strong> +221 77 000 00 00</p>
          <p><strong>Email :</strong> support@agroconnect.sn</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from '@/components /layout/header.vue';
</script>

<style scoped>
.about-container {
  min-height: 100vh;
  background-color: #f8fafc;
}

.about-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 100px 20px 60px;
}

.hero-section {
  text-align: center;
  margin-bottom: 60px;
}

.title {
  font-size: 3rem;
  color: #166534;
  margin-bottom: 15px;
  font-weight: 800;
}

.subtitle {
  font-size: 1.25rem;
  color: #475569;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.info-card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.info-card h2 {
  color: #166534;
  margin-bottom: 20px;
}

.info-card ul {
  list-style: none;
  padding: 0;
}

.info-card li {
  margin-bottom: 12px;
  padding-left: 20px;
  position: relative;
}

.info-card li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #22c55e;
  font-weight: bold;
}

.guide-section {
  background: #166534;
  color: white;
  padding: 60px 40px;
  border-radius: 30px;
  margin-bottom: 60px;
}

.guide-section h2 {
  text-align: center;
  margin-bottom: 40px;
}

.steps-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.step {
  text-align: center;
}

.step-num {
  width: 40px;
  height: 40px;
  background: #22c55e;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 0 auto 20px;
  font-weight: bold;
}

.cta-section {
  text-align: center;
  margin-bottom: 60px;
  padding: 40px;
  background: #f0fdf4;
  border: 2px dashed #22c55e;
  border-radius: 20px;
}

.cta-button {
  display: inline-block;
  margin-top: 20px;
  padding: 15px 35px;
  background: #166534;
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: bold;
  transition: transform 0.2s;
}

.cta-button:hover {
  transform: translateY(-2px);
  background: #15803d;
}

.contact-section {
  text-align: center;
}

.contact-card {
  margin-top: 20px;
  background: white;
  padding: 30px;
  border-radius: 15px;
  display: inline-block;
  text-align: left;
  border: 1px solid #e2e8f0;
}

.fade-in {
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
