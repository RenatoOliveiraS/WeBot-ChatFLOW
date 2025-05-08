import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { environment } from '../../config/environment';

export class ApiClient {
  private api: AxiosInstance;

  constructor(baseUrl?: string) {
    const apiUrl = baseUrl || environment.apiUrl;
    
    if (!apiUrl) {
      throw new Error('VITE_API_URL não está definida nas variáveis de ambiente');
    }
    
    console.log('Inicializando ApiClient');

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
        // Log seguro da requisição
        console.log('Enviando requisição:', {
          url: config.url,
          method: config.method,
          headers: {
            ...config.headers,
            Authorization: config.headers.Authorization ? 'Bearer [REDACTED]' : undefined
          }
        });
        return config;
      },
      (error) => {
        console.error('Erro na requisição:', error.message);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        // Log seguro da resposta
        console.log('Resposta recebida:', {
          status: response.status,
          url: response.config.url
        });
        return response;
      },
      (error) => {
        console.error('Erro na resposta:', {
          status: error.response?.status,
          message: error.message,
          url: error.config?.url
        });
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  public async get<T>(url: string): Promise<AxiosResponse<T>> {
    try {
      return await this.api.get<T>(url);
    } catch (error: any) {
      console.error(`Erro na requisição GET ${url}:`, error.message);
      throw error;
    }
  }

  public async post<T>(url: string, data: any): Promise<AxiosResponse<T>> {
    try {
      // Log seguro do POST
      console.log(`Enviando POST para ${url}`);
      const response = await this.api.post<T>(url, data);
      return response;
    } catch (error: any) {
      console.error(`Erro na requisição POST ${url}:`, error.message);
      throw error;
    }
  }

  public async put<T>(url: string, data: any): Promise<AxiosResponse<T>> {
    try {
      return await this.api.put<T>(url, data);
    } catch (error: any) {
      console.error(`Erro na requisição PUT ${url}:`, error.message);
      throw error;
    }
  }

  public async delete<T>(url: string): Promise<AxiosResponse<T>> {
    try {
      return await this.api.delete<T>(url);
    } catch (error: any) {
      console.error(`Erro na requisição DELETE ${url}:`, error.message);
      throw error;
    }
  }
} 