import { jsx as _jsx } from "react/jsx-runtime";
// src/__tests__/Login.test.tsx
import { screen, fireEvent, waitFor, act } from '@testing-library/react';
import i18n from '../i18n';
import Login from '../presentation/pages/Login';
import { render as customRender, mockAuthService } from './test-utils';
// Mock do módulo de ambiente
jest.mock('../config/environment', () => ({
    environment: {
        apiUrl: 'http://localhost:8000'
    }
}));
// Mock do módulo de navegação
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockNavigate,
}));
const renderLogin = () => {
    return customRender(_jsx(Login, {}));
};
describe('Login Page', () => {
    beforeEach(() => {
        mockNavigate.mockClear();
        jest.clearAllMocks();
        act(() => {
            i18n.changeLanguage('en');
        });
    });
    it('should display error message for invalid password', async () => {
        mockAuthService.login.mockRejectedValueOnce(new Error('Usuário ou senha inválidos'));
        renderLogin();
        const emailInput = screen.getByPlaceholderText(/your@email.com/i);
        const passwordInput = screen.getByPlaceholderText(/••••••/i);
        const submitButton = screen.getByRole('button', { name: /sign in/i });
        await act(async () => {
            fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
            fireEvent.change(passwordInput, { target: { value: 'wrong' } });
            fireEvent.click(submitButton);
        });
        await waitFor(() => {
            expect(screen.getByText(/usuário ou senha inválidos/i)).toBeInTheDocument();
        });
    });
    it('should redirect to dashboard on successful login', async () => {
        const mockUser = {
            id: '1',
            email: 'test@example.com',
            name: 'Test User',
            roles: ['user'],
            is_active: true,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            token: 'mock-token-123'
        };
        mockAuthService.login.mockResolvedValueOnce(mockUser);
        renderLogin();
        const emailInput = screen.getByPlaceholderText(/your@email.com/i);
        const passwordInput = screen.getByPlaceholderText(/••••••/i);
        const submitButton = screen.getByRole('button', { name: /sign in/i });
        await act(async () => {
            fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
            fireEvent.change(passwordInput, { target: { value: '123456' } });
            fireEvent.click(submitButton);
        });
        await waitFor(() => {
            expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
        });
    });
    it('should validate email format', () => {
        renderLogin();
        const emailInput = screen.getByPlaceholderText(/your@email.com/i);
        const submitButton = screen.getByRole('button', { name: /sign in/i });
        fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
        fireEvent.click(submitButton);
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
    });
    it('should validate password length', () => {
        renderLogin();
        const passwordInput = screen.getByPlaceholderText(/••••••/i);
        const submitButton = screen.getByRole('button', { name: /sign in/i });
        fireEvent.change(passwordInput, { target: { value: '123' } });
        fireEvent.click(submitButton);
        expect(screen.getByText(/password must be at least 6 characters long/i)).toBeInTheDocument();
    });
    it('should change language to Portuguese', async () => {
        renderLogin();
        await act(async () => {
            await i18n.changeLanguage('pt');
        });
        await waitFor(() => {
            expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
            expect(screen.getByPlaceholderText(/seu@email.com/i)).toBeInTheDocument();
        });
    });
    it('should change language to Spanish', async () => {
        renderLogin();
        await act(async () => {
            await i18n.changeLanguage('es');
        });
        await waitFor(() => {
            expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument();
            expect(screen.getByPlaceholderText(/tu@email.com/i)).toBeInTheDocument();
        });
    });
    it('should toggle remember me checkbox', () => {
        renderLogin();
        const rememberMeCheckbox = screen.getByRole('checkbox', { name: /remember me/i });
        expect(rememberMeCheckbox).not.toBeChecked();
        fireEvent.click(rememberMeCheckbox);
        expect(rememberMeCheckbox).toBeChecked();
    });
    it('should show forgot password link', () => {
        renderLogin();
        expect(screen.getByRole('button', { name: /forgot your password/i })).toBeInTheDocument();
    });
    it('should show required field errors', () => {
        renderLogin();
        const submitButton = screen.getByRole('button', { name: /sign in/i });
        fireEvent.click(submitButton);
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
        expect(screen.getByText(/password must be at least 6 characters long/i)).toBeInTheDocument();
    });
});
