// src/__tests__/Login.test.tsx

import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { I18nextProvider } from 'react-i18next'
import i18n from '../i18n'
import Login from '../presentation/pages/Login'
import { AuthProvider } from '../presentation/contexts/AuthContext'
import { AuthServiceImpl } from '../infrastructure/services/AuthServiceImpl'
import { UserRepositoryImpl } from '../infrastructure/repositories/UserRepositoryImpl'
import { ApiClient } from '../infrastructure/api/ApiClient'

// Mock do módulo de navegação
const mockNavigate = jest.fn()
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}))

// Configuração dos mocks
const apiClient = new ApiClient()
const userRepository = new UserRepositoryImpl(apiClient)
const authService = new AuthServiceImpl(userRepository)

// Mock do serviço de autenticação
jest.spyOn(authService, 'login').mockImplementation(async (credentials) => {
  if (credentials.password === '123456') {
    return {
      id: '1',
      email: credentials.email,
      name: 'Usuário Teste',
      token: 'mock-token-123'
    }
  }
  throw new Error('Usuário ou senha inválidos')
})

const renderLogin = () => {
  return render(
    <BrowserRouter>
      <I18nextProvider i18n={i18n}>
        <AuthProvider authService={authService}>
          <Login />
        </AuthProvider>
      </I18nextProvider>
    </BrowserRouter>
  )
}

describe('Login Page', () => {
  beforeEach(() => {
    mockNavigate.mockClear()
    act(() => {
      i18n.changeLanguage('en')
    })
  })

  it('should display error message for invalid password', async () => {
    renderLogin()

    const emailInput = screen.getByPlaceholderText(/your@email.com/i)
    const passwordInput = screen.getByPlaceholderText(/••••••/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    await act(async () => {
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
      fireEvent.change(passwordInput, { target: { value: 'wrong' } })
      fireEvent.click(submitButton)
    })

    await waitFor(() => {
      expect(screen.getByText(/usuário ou senha inválidos/i)).toBeInTheDocument()
    })
  })

  it('should redirect to dashboard on successful login', async () => {
    renderLogin()

    const emailInput = screen.getByPlaceholderText(/your@email.com/i)
    const passwordInput = screen.getByPlaceholderText(/••••••/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    await act(async () => {
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
      fireEvent.change(passwordInput, { target: { value: '123456' } })
      fireEvent.click(submitButton)
    })

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard')
    })
  })

  it('should validate email format', () => {
    renderLogin()

    const emailInput = screen.getByPlaceholderText(/your@email.com/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    fireEvent.change(emailInput, { target: { value: 'invalid-email' } })
    fireEvent.click(submitButton)

    expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument()
  })

  it('should validate password length', () => {
    renderLogin()

    const passwordInput = screen.getByPlaceholderText(/••••••/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    fireEvent.change(passwordInput, { target: { value: '123' } })
    fireEvent.click(submitButton)

    expect(screen.getByText(/password must be at least 6 characters long/i)).toBeInTheDocument()
  })

  it('should change language to Portuguese', async () => {
    renderLogin()
    
    await act(async () => {
      await i18n.changeLanguage('pt')
    })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/seu@email.com/i)).toBeInTheDocument()
    })
  })

  it('should change language to Spanish', async () => {
    renderLogin()
    
    await act(async () => {
      await i18n.changeLanguage('es')
    })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument()
      expect(screen.getByPlaceholderText(/tu@email.com/i)).toBeInTheDocument()
    })
  })

  it('should toggle remember me checkbox', () => {
    renderLogin()

    const rememberMeCheckbox = screen.getByRole('checkbox', { name: /remember me/i })
    expect(rememberMeCheckbox).not.toBeChecked()

    fireEvent.click(rememberMeCheckbox)
    expect(rememberMeCheckbox).toBeChecked()
  })

  it('should show forgot password link', () => {
    renderLogin()

    expect(screen.getByRole('button', { name: /forgot your password/i })).toBeInTheDocument()
  })

  it('should show required field errors', () => {
    renderLogin()

    const submitButton = screen.getByRole('button', { name: /sign in/i })
    fireEvent.click(submitButton)

    expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument()
    expect(screen.getByText(/password must be at least 6 characters long/i)).toBeInTheDocument()
  })
})
