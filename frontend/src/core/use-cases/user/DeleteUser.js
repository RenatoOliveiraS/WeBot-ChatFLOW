export class DeleteUser {
    userRepository;
    constructor(userRepository) {
        this.userRepository = userRepository;
    }
    async execute(id) {
        // Verificar se o usuário existe
        const existingUser = await this.userRepository.findById(id);
        if (!existingUser) {
            throw new Error('Usuário não encontrado');
        }
        // Deletar o usuário
        await this.userRepository.delete(id);
    }
}
