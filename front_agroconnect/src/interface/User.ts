export interface User {
  id: string;
  nom: string;
  prenom: string;
  email: string;
  role: string;
  telephone?: string;
  photo?: string;
  agriculteur_id?: string;
  client_id?: string;
  is_actif?: boolean;
}

export interface RegisterData {
  nom: string;
  prenom: string;
  email: string;
  telephone: string;
  mot_de_pass: string;
  adresse: string;
  role: string;
  photo?: string;
}
