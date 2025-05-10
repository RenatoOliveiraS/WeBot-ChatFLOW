export class UpdateUser {
    userRepository;
    constructor(userRepository) {
        this.userRepository = userRepository;
    }
    async execute(id, userData) {
        // Verificar se o usuário existe
        const existingUser = await this.userRepository.findById(id);
        if (!existingUser) {
            throw new Error('Usuário não encontrado');
        }
        // Se estiver atualizando o email, verificar se já existe
        if (userData.email && userData.email !== existingUser.email) {
            const userWithEmail = await this.userRepository.findByEmail(userData.email);
            if (userWithEmail) {
                throw new Error('Email já está em uso');
            }
        }
        // Atualizar o usuário
        return await this.userRepository.update(id, userData);
    }
}
