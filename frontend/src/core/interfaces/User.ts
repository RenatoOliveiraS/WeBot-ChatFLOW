export interface User {
  id: string;
  email: string;
  name: string;
  photo?: string;
  roles: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
  token: string;
} 