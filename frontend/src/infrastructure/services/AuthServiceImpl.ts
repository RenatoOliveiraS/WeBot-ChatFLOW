import { LoginCredentials } from '../../core/domain/entities/User';
import { User } from '../../core/interfaces/User';
import { AuthService } from '../../core/interfaces/services/AuthService';
import { UserRepository } from '../../core/interfaces/repositories/UserRepository';
import i18n from '../../i18n';

export class AuthServiceImpl implements AuthService {
  private currentUser: User | null = null;

  constructor(private userRepository: UserRepository) {
    // Recupera o usuário do localStorage se existir
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      this.currentUser = JSON.parse(storedUser);
    }
  }

  async login(credentials: LoginCredentials): Promise<User> {
    try {
      const response = await this.userRepository.authenticate(credentials);
      const user: User = {
        id: response.id,
        email: response.email,
        name: response.name,
        photo: response.photo,
        roles: response.roles,
        is_active: response.is_active,
        created_at: response.created_at,
        updated_at: response.updated_at,
        token: response.access_token
      };
      
      this.setCurrentUser(user);
      return user;
    } catch (error: unknown) {
      console.error('Erro no login:', error);
      if (error instanceof Error) {
        const axiosError = error as { response?: { status?: number; data?: { detail?: string } } };
        if (axiosError.response?.status === 401) {
          throw new Error(i18n.t('login.authError.invalidCredentials'));
        }
        if (axiosError.response?.data?.detail) {
          const errorMessage = axiosError.response.data.detail;
          if (errorMessage.includes('inativo')) {
            throw new Error(i18n.t('login.authError.inactiveUser'));
          }
          if (errorMessage.includes('não encontrado')) {
            throw new Error(i18n.t('login.authError.userNotFound'));
          }
        }
      }
      throw new Error(i18n.t('login.authError.serverError'));
    }
  }

  async logout(): Promise<void> {
    this.currentUser = null;
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return !!this.currentUser && !!localStorage.getItem('token');
  }

  private setCurrentUser(user: User): void {
    this.currentUser = user;
    localStorage.setItem('user', JSON.stringify(user));
    if (user.token) {
      localStorage.setItem('token', user.token);
    }
  }
} 