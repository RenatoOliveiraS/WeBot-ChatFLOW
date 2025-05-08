import { User, LoginCredentials } from '../../core/domain/entities/User';
import { AuthService } from '../../core/interfaces/services/AuthService';
import { UserRepository } from '../../core/interfaces/repositories/UserRepository';

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
        id: response.user_id,
        email: response.email,
        roles: response.roles,
        token: response.access_token
      };
      
      this.setCurrentUser(user);
      return user;
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Usuário ou senha inválidos');
      }
      throw new Error('Falha na autenticação. Tente novamente mais tarde.');
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