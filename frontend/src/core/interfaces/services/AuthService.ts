import { User, LoginCredentials } from '../../domain/entities/User';

export interface AuthService {
  login(credentials: LoginCredentials): Promise<User>;
  logout(): Promise<void>;
  getCurrentUser(): User | null;
  isAuthenticated(): boolean;
} 