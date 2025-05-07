// frontend/src/services/authService.ts
//import axios from 'axios';

export interface LoginPayload {
  email: string;
  password: string;
}

// Mock que só “logins” com senha exata “123456” passam, os outros falham
export async function login(payload: LoginPayload) {
  console.log('Payload de login (mock):', payload);
  return new Promise<{ data: { token: string } }>((resolve, reject) => {
    setTimeout(() => {
      if (payload.password === '123456') {
        // sucesso!
        resolve({ data: { token: 'mock-token-123' } });
      } else {
        // simula erro de credenciais do servidor
        reject({
          response: { data: { message: 'Usuário ou senha inválidos' } },
        });
      }
    }, 500);
  });
}

// Quando o backend estiver pronto, volte a isto:
// export function login(payload: LoginPayload) {
//   return axios.post('/auth/login', payload);
// }
