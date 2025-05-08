import { User, LoginCredentials } from '../../domain/entities/User';

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  id: string;
  email: string;
  roles: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserRepository {
  findByEmail(email: string): Promise<User | null>;
  authenticate(credentials: LoginCredentials): Promise<LoginResponse>;
  save(user: User): Promise<void>;
} 