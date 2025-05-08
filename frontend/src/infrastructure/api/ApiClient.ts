import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

export class ApiClient {
  private api: AxiosInstance;

  constructor() {
    const apiUrl = import.meta.env.VITE_API_URL;
    
    if (!apiUrl) {
      throw new Error('VITE_API_URL não está definida nas variáveis de ambiente');
    }

    console.log('Inicializando ApiClient com URL:', apiUrl);

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
        console.log('Enviando requisição:', {
          url: config.url,
          method: config.method,
          headers: config.headers,
          data: config.data,
          baseURL: config.baseURL,
          fullURL: `${config.baseURL}${config.url}`
        });
        return config;
      },
      (error) => {
        console.error('Erro na requisição:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        console.log('Resposta recebida:', {
          status: response.status,
          data: response.data,
          headers: response.headers,
          config: {
            url: response.config.url,
            baseURL: response.config.baseURL,
            fullURL: `${response.config.baseURL}${response.config.url}`
          }
        });
        return response;
      },
      (error) => {
        console.error('Erro na resposta:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message,
          config: error.config ? {
            url: error.config.url,
            baseURL: error.config.baseURL,
            fullURL: `${error.config.baseURL}${error.config.url}`
          } : 'No config'
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
      console.error(`Erro na requisição GET ${url}:`, error.response?.data || error.message);
      throw error;
    }
  }

  public async post<T>(url: string, data: any): Promise<AxiosResponse<T>> {
    try {
      console.log(`Enviando POST para ${url}:`, data);
      const response = await this.api.post<T>(url, data);
      console.log(`Resposta do POST ${url}:`, response.data);
      return response;
    } catch (error: any) {
      console.error(`Erro na requisição POST ${url}:`, error.response?.data || error.message);
      throw error;
    }
  }

  public async put<T>(url: string, data: any): Promise<AxiosResponse<T>> {
    try {
      return await this.api.put<T>(url, data);
    } catch (error: any) {
      console.error(`Erro na requisição PUT ${url}:`, error.response?.data || error.message);
      throw error;
    }
  }

  public async delete<T>(url: string): Promise<AxiosResponse<T>> {
    try {
      return await this.api.delete<T>(url);
    } catch (error: any) {
      console.error(`Erro na requisição DELETE ${url}:`, error.response?.data || error.message);
      throw error;
    }
  }
} 