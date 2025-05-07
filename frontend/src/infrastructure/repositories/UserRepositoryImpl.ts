import { User, LoginCredentials } from '../../core/domain/entities/User';
import { UserRepository } from '../../core/interfaces/repositories/UserRepository';
import { ApiClient } from '../api/ApiClient';

export class UserRepositoryImpl implements UserRepository {
  constructor(private api: ApiClient) {}

  async findByEmail(email: string): Promise<User | null> {
    try {
      const response = await this.api.get<User>(`/users/${email}`);
      return response.data;
    } catch (error) {
      return null;
    }
  }

  async authenticate(credentials: LoginCredentials): Promise<User> {
    const response = await this.api.post<User>('/auth/login', credentials);
    return response.data;
  }

  async save(user: User): Promise<void> {
    await this.api.post('/users', user);
  }
} 