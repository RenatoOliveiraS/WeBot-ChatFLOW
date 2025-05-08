import React from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next';
import { Experimental_CssVarsProvider as CssVarsProvider } from '@mui/material/styles';
import i18n from '../i18n';
import AppTheme from '../shared-theme/AppTheme';
import { AuthProvider } from '../presentation/contexts/AuthContext';
import { AuthService } from '../core/interfaces/services/AuthService';
import { User } from '../core/domain/entities/User';

// Mock do serviço de autenticação
const mockAuthService: jest.Mocked<AuthService> = {
  login: jest.fn<Promise<User>, [any]>(),
  logout: jest.fn<Promise<void>, []>(),
  getCurrentUser: jest.fn<User | null, []>(() => null),
  isAuthenticated: jest.fn<boolean, []>(() => false),
};

interface WrapperProps {
  children: React.ReactNode;
}

export const AllTheProviders = ({ children }: WrapperProps) => {
  return (
    <BrowserRouter>
      <I18nextProvider i18n={i18n}>
        <CssVarsProvider>
          <AppTheme>
            <AuthProvider authService={mockAuthService}>
              {children}
            </AuthProvider>
          </AppTheme>
        </CssVarsProvider>
      </I18nextProvider>
    </BrowserRouter>
  );
};

const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllTheProviders, ...options });

// re-export everything
export * from '@testing-library/react';

// override render method
export { customRender as render, mockAuthService }; 