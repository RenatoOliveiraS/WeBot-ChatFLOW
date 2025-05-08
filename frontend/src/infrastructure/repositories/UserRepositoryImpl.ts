import { User, CreateUserDTO, UpdateUserDTO, LoginCredentials } from '../../core/domain/entities/User';
import { UserRepository, LoginResponse } from '../../core/interfaces/repositories/UserRepository';
import { ApiClient } from '../api/ApiClient';

export class UserRepositoryImpl implements UserRepository {
  constructor(private api: ApiClient) {}

  async authenticate(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response = await this.api.post<LoginResponse>('/api/v1/auth/login', credentials);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async create(userData: CreateUserDTO): Promise<User> {
    try {
      const response = await this.api.post<User>('/api/v1/users', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
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
    try {
      const response = await this.api.put<User>(`/api/v1/users/${id}`, userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async delete(id: string): Promise<void> {
    try {
      await this.api.delete(`/api/v1/users/${id}`);
    } catch (error) {
      throw error;
    }
  }

  async list(): Promise<User[]> {
    try {
      const response = await this.api.get<User[]>('/api/v1/users');
      return response.data;
    } catch (error) {
      throw error;
    }
  }
} 