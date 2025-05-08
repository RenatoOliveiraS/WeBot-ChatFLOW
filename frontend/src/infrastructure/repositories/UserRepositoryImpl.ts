import { User, LoginCredentials } from '../../core/domain/entities/User';
import { UserRepository, LoginResponse } from '../../core/interfaces/repositories/UserRepository';
import { ApiClient } from '../api/ApiClient';

export class UserRepositoryImpl implements UserRepository {
  constructor(private api: ApiClient) {}

  async findByEmail(email: string): Promise<User | null> {
    try {
      const response = await this.api.get<User>(`/api/v1/users/${email}`);
      return response.data;
    } catch (error) {
      return null;
    }
  }

  async authenticate(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response = await this.api.post<LoginResponse>('/api/v1/auth/login', credentials);
      return response.data;
    } catch (error: any) {
      throw error;
    }
  }

  async save(user: User): Promise<void> {
    await this.api.post('/api/v1/users', user);
  }
} 