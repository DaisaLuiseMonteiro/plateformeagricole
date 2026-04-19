export interface Product {
  id: string;
  name: string;
  prix_unitaire: number;
  description: string | null;
  quantite_stock: number;
  photo: string | null;
  categorie: string;
  agriculteur_id: string;
}
