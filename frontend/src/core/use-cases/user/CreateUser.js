export class CreateUser {
    userRepository;
    constructor(userRepository) {
        this.userRepository = userRepository;
    }
    async execute(userData) {
        // Validar se o email já existe
        const existingUser = await this.userRepository.findByEmail(userData.email);
        if (existingUser) {
            throw new Error('Email já está em uso');
        }
        // Criar o usuário
        return await this.userRepository.create(userData);
    }
}
