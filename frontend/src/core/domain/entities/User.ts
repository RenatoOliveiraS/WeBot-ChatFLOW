export interface User {
  id: string;
  email: string;
  roles: string[];
  token: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
} 