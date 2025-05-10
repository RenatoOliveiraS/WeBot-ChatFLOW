import { jsx as _jsx } from "react/jsx-runtime";
// frontend/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './i18n';
import { ApiClient } from './infrastructure/api/ApiClient';
import { UserRepositoryImpl } from './infrastructure/repositories/UserRepositoryImpl';
import { AuthServiceImpl } from './infrastructure/services/AuthServiceImpl';
import { AuthProvider } from './presentation/contexts/AuthContext';
// Inicializa as dependências
const apiClient = new ApiClient();
const userRepository = new UserRepositoryImpl(apiClient);
const authService = new AuthServiceImpl(userRepository);
ReactDOM.createRoot(document.getElementById('root')).render(_jsx(React.StrictMode, { children: _jsx(BrowserRouter, { children: _jsx(AuthProvider, { authService: authService, children: _jsx(App, {}) }) }) }));
