import type { User } from './User';

export interface Agriculteur {
  id: string;
  name?: string;
  email?: string;
  status?: string;
  registrationDate?: string;
  productsCount?: number;
  is_actif: boolean;
  user?: User;
}
