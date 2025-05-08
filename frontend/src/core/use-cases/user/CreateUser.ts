import { User, CreateUserDTO } from '../../domain/entities/User';
import { UserRepository } from '../../interfaces/repositories/UserRepository';

export class CreateUser {
  constructor(private userRepository: UserRepository) {}

  async execute(userData: CreateUserDTO): Promise<User> {
    // Validar se o email já existe
    const existingUser = await this.userRepository.findByEmail(userData.email);
    if (existingUser) {
      throw new Error('Email já está em uso');
    }

    // Criar o usuário
    return await this.userRepository.create(userData);
  }
} 