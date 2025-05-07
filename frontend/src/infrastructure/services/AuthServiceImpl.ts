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
      // Mock temporário - remover quando o backend estiver pronto
      if (credentials.password === '123456') {
        const mockUser: User = {
          id: '1',
          email: credentials.email,
          name: 'Usuário Mock',
          token: 'mock-token-123'
        };
        this.setCurrentUser(mockUser);
        return mockUser;
      }
      throw new Error('Usuário ou senha inválidos');

      // Implementação real - descomentar quando o backend estiver pronto
      // const user = await this.userRepository.authenticate(credentials);
      // this.setCurrentUser(user);
      // return user;
    } catch (error) {
      throw new Error('Falha na autenticação');
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
    return !!this.currentUser;
  }

  private setCurrentUser(user: User): void {
    this.currentUser = user;
    localStorage.setItem('user', JSON.stringify(user));
    if (user.token) {
      localStorage.setItem('token', user.token);
    }
  }
} 