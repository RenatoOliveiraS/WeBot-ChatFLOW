import { User } from '../../domain/entities/User';
import { UserRepository } from '../../interfaces/repositories/UserRepository';

export class ListUsers {
  constructor(private userRepository: UserRepository) {}

  async execute(): Promise<User[]> {
    return await this.userRepository.list();
  }
} 