import { User, CreateUserDTO, UpdateUserDTO, LoginCredentials } from '../../domain/entities/User';

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  id: string;
  email: string;
  name: string;
  photo?: string;
  roles: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserRepository {
  // Auth
  authenticate(credentials: LoginCredentials): Promise<LoginResponse>;
  
  // CRUD
  create(user: CreateUserDTO): Promise<User>;
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  update(id: string, user: UpdateUserDTO): Promise<User>;
  delete(id: string): Promise<void>;
  list(): Promise<User[]>;
} 