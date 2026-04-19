export interface OrderDetail {
  id: string;
  produit_id: string;
  quantite: number;
  montant: number;
  agriculteur_nom?: string;
}

export interface Order {
  id: string;
  date_commande: string;
  statut: string;
  montant_commande: number;
  client_id: string;
  details: OrderDetail[];
}

export interface CommandeData {
  client_id: string;
  montant_total: number;
  items: {
    produit_id: string;
    quantite: number;
    montant: number;
  }[];
}
