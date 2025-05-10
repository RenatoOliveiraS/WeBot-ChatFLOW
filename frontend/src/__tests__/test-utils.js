import { jsx as _jsx } from "react/jsx-runtime";
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next';
import { Experimental_CssVarsProvider as CssVarsProvider } from '@mui/material/styles';
import i18n from '../i18n';
import AppTheme from '../shared-theme/AppTheme';
import { AuthProvider } from '../presentation/contexts/AuthContext';
// Mock do serviço de autenticação
const mockAuthService = {
    login: jest.fn(),
    logout: jest.fn(),
    getCurrentUser: jest.fn(() => null),
    isAuthenticated: jest.fn(() => false),
};
export const AllTheProviders = ({ children }) => {
    return (_jsx(BrowserRouter, { children: _jsx(I18nextProvider, { i18n: i18n, children: _jsx(CssVarsProvider, { children: _jsx(AppTheme, { children: _jsx(AuthProvider, { authService: mockAuthService, children: children }) }) }) }) }));
};
const customRender = (ui, options) => render(ui, { wrapper: AllTheProviders, ...options });
// re-export everything
export * from '@testing-library/react';
// override render method
export { customRender as render, mockAuthService };
