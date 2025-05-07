export interface User {
  id: string;
  email: string;
  name: string;
  token?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
} 