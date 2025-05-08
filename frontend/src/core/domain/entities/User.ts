export interface User {
  id: string;
  email: string;
  name: string;
  photo?: string;
  roles: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateUserDTO {
  email: string;
  name: string;
  password: string;
  photo?: string;
  roles?: string[];
}

export interface UpdateUserDTO {
  email?: string;
  name?: string;
  photo?: string;
  roles?: string[];
  is_active?: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
} 