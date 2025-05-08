import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { environment } from '../../config/environment';

export class ApiClient {
  private api: AxiosInstance;

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

  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string): Promise<AxiosResponse<T>> {
    try {
      return await this.api.get<T>(url);
    } catch (error) {
      throw error;
    }
  }

  async post<T>(url: string, data: any): Promise<AxiosResponse<T>> {
    try {
      return await this.api.post<T>(url, data);
    } catch (error) {
      throw error;
    }
  }

  async put<T>(url: string, data: any): Promise<AxiosResponse<T>> {
    try {
      return await this.api.put<T>(url, data);
    } catch (error) {
      throw error;
    }
  }

  async delete<T>(url: string): Promise<AxiosResponse<T>> {
    try {
      return await this.api.delete<T>(url);
    } catch (error) {
      throw error;
    }
  }
} 