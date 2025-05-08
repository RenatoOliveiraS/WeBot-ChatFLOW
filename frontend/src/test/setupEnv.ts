import { config } from 'dotenv';

// Carrega as variáveis de ambiente do arquivo .env.test se existir
config({ path: '.env.test' });

// Define as variáveis de ambiente necessárias para os testes
process.env.VITE_API_URL = process.env.VITE_API_URL || 'http://localhost:8000'; 