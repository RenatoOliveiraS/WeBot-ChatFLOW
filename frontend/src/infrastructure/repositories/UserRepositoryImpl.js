export class UserRepositoryImpl {
    api;
    constructor(api) {
        this.api = api;
    }
    async authenticate(credentials) {
        const response = await this.api.post('/api/v1/auth/login', credentials);
        return response.data;
    }
    async create(userData) {
        const response = await this.api.post('/api/v1/users', userData);
        return response.data;
    }
    async findById(id) {
        try {
            const response = await this.api.get(`/api/v1/users/${id}`);
            return response.data;
        }
        catch (error) {
            return null;
        }
    }
    async findByEmail(email) {
        try {
            const response = await this.api.get(`/api/v1/users/email/${email}`);
            return response.data;
        }
        catch (error) {
            return null;
        }
    }
    async update(id, userData) {
        const response = await this.api.put(`/api/v1/users/${id}`, userData);
        return response.data;
    }
    async delete(id) {
        await this.api.delete(`/api/v1/users/${id}`);
    }
    async list() {
        const response = await this.api.get('/api/v1/users');
        return response.data;
    }
}
