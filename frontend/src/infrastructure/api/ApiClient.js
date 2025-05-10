import axios from 'axios';
import { environment } from '../../config/environment';
export class ApiClient {
    api;
    constructor() {
        const apiUrl = environment.apiUrl;
        if (!apiUrl) {
            throw new Error('VITE_API_URL não está definida nas variáveis de ambiente');
        }
        this.api = axios.create({
            baseURL: apiUrl,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        this.setupInterceptors();
    }
    setupInterceptors() {
        // Request interceptor
        this.api.interceptors.request.use((config) => {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        }, (error) => {
            return Promise.reject(error);
        });
        // Response interceptor
        this.api.interceptors.response.use((response) => {
            return response;
        }, (error) => {
            if (error.response?.status === 401) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/login';
            }
            return Promise.reject(error);
        });
    }
    async get(url) {
        return await this.api.get(url);
    }
    async post(url, data) {
        return await this.api.post(url, data);
    }
    async put(url, data) {
        return await this.api.put(url, data);
    }
    async delete(url) {
        return await this.api.delete(url);
    }
}
