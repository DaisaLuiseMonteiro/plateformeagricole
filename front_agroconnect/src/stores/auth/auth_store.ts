import { defineStore } from 'pinia';

interface User {
  id: string;
  nom: string;
  prenom: string;
  email: string;
  role: string;
  telephone?: string;
  photo?: string;
  agriculteur_id?: string;
  client_id?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: string | null;
  fieldErrors: Record<string, string>;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim() || 'http://127.0.0.1:8000';

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    loading: false,
    error: null,
    fieldErrors: {},
  }),

  actions: {
    // ============================================================
    // SECTION : CONNEXION (LOGIN)
    // ============================================================
    async login(email: string, mot_de_pass: string) {
      this.fieldErrors = {};
      this.error = null;

      // Validation locale
      if (!email) {
        this.fieldErrors.email = "L'email est requis";
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        this.fieldErrors.email = "Format d'email invalide (ex: user@gmail.com)";
      }
      if (!mot_de_pass) {
        this.fieldErrors.mot_de_pass = "Le mot de passe est requis!";
      }

      if (Object.keys(this.fieldErrors).length > 0) return;

      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, mot_de_pass }),
        });

        const data = await response.json();

        if (!response.ok) {
          const detail = data.detail || 'Erreur de connexion';
          if (detail.includes('Email') || detail.includes('passe') || detail.includes('incorrect')) {
            this.fieldErrors.mot_de_pass = detail;
          }
          throw new Error(detail);
        }

        this.token = data.access_token;
        this.refreshToken = data.refresh_token;
        this.user = {
          id: data.user_id,
          role: data.role,
          nom: '', 
          prenom: '',
          email: email,
          photo: data.photo,
          agriculteur_id: data.agriculteur_id,
          client_id: data.client_id
        };

        localStorage.setItem('access_token', this.token as string);
        localStorage.setItem('refresh_token', this.refreshToken as string);
        localStorage.setItem('user', JSON.stringify(this.user));

        return data;
      } catch (err: any) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // ============================================================
    // SECTION : INSCRIPTION (REGISTER)
    // ============================================================
    // SECTION : INSCRIPTION (REGISTER)
    // ============================================================
    async register(userData: import('@/interface/User').RegisterData) {
      this.fieldErrors = {};
      this.error = null;

      // Validation locale
      if (!userData.prenom) this.fieldErrors.prenom = "Le prénom est requis";
      if (!userData.nom) this.fieldErrors.nom = "Le nom est requis";
      if (!userData.email) {
        this.fieldErrors.email = "L'email est requis";
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userData.email)) {
        this.fieldErrors.email = "Format d'email invalide (ex: user@gmail.com)";
      }
      if (!userData.telephone) this.fieldErrors.telephone = "Le téléphone est requis";
      if (!userData.adresse) this.fieldErrors.adresse = "L'adresse est requise";
      if (!userData.mot_de_pass) {
        this.fieldErrors.mot_de_pass = "Le mot de passe est requis";
      } else if (userData.mot_de_pass.length < 6) {
        this.fieldErrors.mot_de_pass = "Minimum 6 caractères";
      }

      if (Object.keys(this.fieldErrors).length > 0) return;

      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData),
        });

        const data = await response.json();

        if (!response.ok) {
          const detail = data.detail || "Erreur lors de l'inscription";
          if (detail.includes('email')) {
            this.fieldErrors.email = detail;
          }
          throw new Error(detail);
        }

        return data;
      } catch (err: any) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // ============================================================
    // SECTION : RÉINITIALISATION (RESET PASSWORD)
    // ============================================================
    async resetPassword(email: string, nouveau_mot_de_pass: string) {
      this.fieldErrors = {};
      this.error = null;

      if (!email) {
        this.fieldErrors.email = "L'email est requis";
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        this.fieldErrors.email = "Format d'email invalide (ex: user@gmail.com)";
      }
      if (!nouveau_mot_de_pass) {
        this.fieldErrors.nouveau_mot_de_pass = "Le nouveau mot de passe est requis";
      } else if (nouveau_mot_de_pass.length < 6) {
        this.fieldErrors.nouveau_mot_de_pass = "Minimum 6 caractères";
      }

      if (Object.keys(this.fieldErrors).length > 0) return;

      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/users/reset-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, nouveau_mot_de_pass }),
        });

        const data = await response.json();

        if (!response.ok) {
          const detail = data.detail || 'Erreur lors de la réinitialisation';
          if (detail.includes('email')) {
            this.fieldErrors.email = detail;
          }
          throw new Error(detail);
        }

        return data;
      } catch (err: any) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // ============================================================
    // SECTION : GESTION UTILISATEURS (ADMIN)
    // ============================================================
    async fetchAgriculteurs() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/users/agriculteurs`, {
          headers: { 'Authorization': `Bearer ${this.token}` }
        });
        if (!response.ok) throw new Error("Erreur de récupération");
        return await response.json();
      } catch (err: any) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async validerAgriculteur(agriculteurId: string) {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/users/agriculteurs/${agriculteurId}/activer`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) throw new Error("Erreur lors de l'activation");
        return await response.json();
      } catch (err: any) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async desactiverAgriculteur(agriculteurId: string) {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/users/agriculteurs/${agriculteurId}/desactiver`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) throw new Error("Erreur lors de la désactivation");
        return await response.json();
      } catch (err: any) {
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // ============================================================
    // SECTION : DÉCONNEXION (LOGOUT)
    // ============================================================
    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;
      this.fieldErrors = {};
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role,
    userPhoto: (state) => state.user?.photo || 'https://via.placeholder.com/150',
  },
});
