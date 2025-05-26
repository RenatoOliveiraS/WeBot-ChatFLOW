import { User, CreateUserDTO, UpdateUserDTO, LoginCredentials } from '../../core/domain/entities/User';
import { UserRepository, LoginResponse } from '../../core/interfaces/repositories/UserRepository';
import { ApiClient } from '../api/ApiClient';

export class UserRepositoryImpl implements UserRepository {
  constructor(private api: ApiClient) {}

  async authenticate(credentials: LoginCredentials): Promise<LoginResponse> {
    const params = new URLSearchParams();
    params.append('username', credentials.email);
    params.append('password', credentials.password);
    const response = await this.api.post<LoginResponse>(
      '/auth/login',
      params,
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    );
    return response.data;
  }

  async create(userData: CreateUserDTO): Promise<User> {
    const response = await this.api.post<User>('/api/v1/users', userData);
    return response.data;
  }

  async findById(id: string): Promise<User | null> {
    try {
      const response = await this.api.get<User>(`/api/v1/users/${id}`);
      return response.data;
    } catch (error) {
      return null;
    }
  }

  async findByEmail(email: string): Promise<User | null> {
    try {
      const response = await this.api.get<User>(`/api/v1/users/email/${email}`);
      return response.data;
    } catch (error) {
      return null;
    }
  }

  async update(id: string, userData: UpdateUserDTO): Promise<User> {
    const response = await this.api.put<User>(`/api/v1/users/${id}`, userData);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await this.api.delete(`/api/v1/users/${id}`);
  }

  async list(): Promise<User[]> {
    const response = await this.api.get<User[]>('/api/v1/users');
    return response.data;
  }
} 