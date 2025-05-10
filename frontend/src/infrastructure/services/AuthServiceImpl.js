import i18n from '../../i18n';
export class AuthServiceImpl {
    userRepository;
    currentUser = null;
    constructor(userRepository) {
        this.userRepository = userRepository;
        // Recupera o usuário do localStorage se existir
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            this.currentUser = JSON.parse(storedUser);
        }
    }
    async login(credentials) {
        try {
            const response = await this.userRepository.authenticate(credentials);
            const user = {
                id: response.id,
                email: response.email,
                name: response.name,
                photo: response.photo,
                roles: response.roles,
                is_active: response.is_active,
                created_at: response.created_at,
                updated_at: response.updated_at,
                token: response.access_token
            };
            this.setCurrentUser(user);
            return user;
        }
        catch (error) {
            console.error('Erro no login:', error);
            if (error instanceof Error) {
                const axiosError = error;
                if (axiosError.response?.status === 401) {
                    throw new Error(i18n.t('login.authError.invalidCredentials'));
                }
                if (axiosError.response?.data?.detail) {
                    const errorMessage = axiosError.response.data.detail;
                    if (errorMessage.includes('inativo')) {
                        throw new Error(i18n.t('login.authError.inactiveUser'));
                    }
                    if (errorMessage.includes('não encontrado')) {
                        throw new Error(i18n.t('login.authError.userNotFound'));
                    }
                }
            }
            throw new Error(i18n.t('login.authError.serverError'));
        }
    }
    async logout() {
        this.currentUser = null;
        localStorage.removeItem('user');
        localStorage.removeItem('token');
    }
    getCurrentUser() {
        return this.currentUser;
    }
    isAuthenticated() {
        return !!this.currentUser && !!localStorage.getItem('token');
    }
    setCurrentUser(user) {
        this.currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));
        if (user.token) {
            localStorage.setItem('token', user.token);
        }
    }
}
