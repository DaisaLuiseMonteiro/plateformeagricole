import { createRouter, createWebHistory } from 'vue-router'


// import des composants 
import Index from '@/components /view/index.vue'
import Login from '@/components /view/auth/login.vue'
import Register from '@/components /view/auth/register.vue'
import resetPassword from '@/components /view/auth/resetPassword.vue'
import User from '@/components /view/auth/user.vue'
import AboutUs from '@/components /view/AboutUs.vue'

// Client Components
import Panier from '@/components /view/client/panier.vue'
import CommandeCl from '@/components /view/commandes/commande_cl.vue'

// Admin Components
import TableauAdmin from '@/components /view/admin/tableau.vue'
import ProduitsAdmin from '@/components /view/admin/produits_admin.vue'
import CommandesAdmin from '@/components /view/admin/commandes_admin.vue'
import UtilisateursAdmin from '@/components /view/admin/utilisateurs_admin.vue'
import AgriculteursAdmin from '@/components /view/admin/agriculteurs_admin.vue'
import PublicationsAdmin from '@/components /view/admin/publications_admin.vue'
import NotificationsAdmin from '@/components /view/admin/notifications_admin.vue'
import StatistiquesAdmin from '@/components /view/admin/statistiques_admin.vue'

// Agriculteur Components
import DashboardAgriculteur from '@/components /view/agriculteur/dashboardAgriculteur.vue'
import ProduitsAgriculteur from '@/components /view/agriculteur/produits_agriculteur.vue'
import CommandesAgriculteur from '@/components /view/agriculteur/commandes_agriculteur.vue'
import VentesAgriculteur from '@/components /view/agriculteur/ventes_agriculteur.vue'
import NotificationsAgriculteur from '@/components /view/agriculteur/notifications_agriculteur.vue'


const routes= [
    {path: '/', name:"interface accueil",component: Index},
    {path: '/login', name:"interface connexion",component: Login},
    {path: '/register', name:"interface inscription",component: Register},
    {path: '/reset-password', name:"interface réinitialisation mot de passe",component: resetPassword},
    {path: '/user', name:"interface utilisateur",component: User},
    {path: '/panier', name:"panier",component: Panier},
    {path: '/mes-commandes', name:"mes-commandes",component: CommandeCl},
    {path: '/a-propos', name:"a-propos",component: AboutUs},

    // Admin Routes
    { path: '/admin/dashboard', name: 'admin-dashboard', component: TableauAdmin },
    { path: '/admin/produits', name: 'admin-produits', component: ProduitsAdmin },
    { path: '/admin/commandes', name: 'admin-commandes', component: CommandesAdmin },
    { path: '/admin/utilisateurs', name: 'admin-utilisateurs', component: UtilisateursAdmin },
    { path: '/admin/agriculteurs', name: 'admin-agriculteurs', component: AgriculteursAdmin },
    { path: '/admin/publications', name: 'admin-publications', component: PublicationsAdmin },
    { path: '/admin/notifications', name: 'admin-notifications', component: NotificationsAdmin },
    { path: '/admin/statistiques', name: 'admin-statistiques', component: StatistiquesAdmin },

    // Agriculteur Routes
    { path: '/agriculteur/dashboard', name: 'agriculteur-dashboard', component: DashboardAgriculteur },
    { path: '/agriculteur/produits', name: 'agriculteur-produits', component: ProduitsAgriculteur },
    { path: '/agriculteur/commandes', name: 'agriculteur-commandes', component: CommandesAgriculteur },
    { path: '/agriculteur/ventes', name: 'agriculteur-ventes', component: VentesAgriculteur },
    { path: '/agriculteur/notifications', name: 'agriculteur-notifications', component: NotificationsAgriculteur },
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router


