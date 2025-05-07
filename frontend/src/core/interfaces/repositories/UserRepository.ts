import { User, LoginCredentials } from '../../domain/entities/User';
 
export interface UserRepository {
  findByEmail(email: string): Promise<User | null>;
  authenticate(credentials: LoginCredentials): Promise<User>;
  save(user: User): Promise<void>;
} 