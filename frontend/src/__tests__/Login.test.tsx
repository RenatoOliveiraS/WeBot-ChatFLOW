// src/__tests__/Login.test.tsx

import React from 'react'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import LoginPage from '../pages/Login'
import DashboardPage from '../pages/Dashboard'
import * as authService from '../services/authService'
import i18n from '../i18n'

// Mock do authService
jest.spyOn(authService, 'login').mockImplementation(({ password }) => {
  return password === '123456'
    ? Promise.resolve({ data: { token: 'mock-token' } })
    : Promise.reject({ response: { data: { message: 'Falha no login' } } })
})

describe('LoginPage', () => {
  beforeEach(async () => {
    // Reset do i18n para inglês antes de cada teste
    await act(async () => {
      await i18n.changeLanguage('en')
    })
  })

  test('mostra erro quando senha é inválida', async () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </MemoryRouter>
    )

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    fireEvent.change(emailInput, { target: { value: 'teste@ex.com' } })
    fireEvent.change(passwordInput, { target: { value: 'senhaErrada' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Falha no login')
    })
  })

  test('redireciona para /dashboard quando senha é válida', async () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </MemoryRouter>
    )

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    fireEvent.change(emailInput, { target: { value: 'teste@ex.com' } })
    fireEvent.change(passwordInput, { target: { value: '123456' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/Hello Dashboard/i)).toBeInTheDocument()
    })
  })

  test('valida formato de email inválido', async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    const emailInput = screen.getByLabelText(/email/i)
    fireEvent.change(emailInput, { target: { value: 'email-invalido' } })
    fireEvent.blur(emailInput)
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      const helperText = screen.getByText(/Please enter a valid email address/i)
      expect(helperText).toBeInTheDocument()
    })
  })

  test('valida senha muito curta', async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    const passwordInput = screen.getByLabelText(/password/i)
    fireEvent.change(passwordInput, { target: { value: '123' } })
    fireEvent.blur(passwordInput)
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      const helperText = screen.getByText(/Password must be at least 6 characters long/i)
      expect(helperText).toBeInTheDocument()
    })
  })

  test('muda idioma para português', async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    await act(async () => {
      await i18n.changeLanguage('pt')
    })

    await waitFor(() => {
      expect(screen.getByRole('heading')).toHaveTextContent('Entrar')
      expect(screen.getByLabelText('E-mail')).toBeInTheDocument()
      expect(screen.getByLabelText('Senha')).toBeInTheDocument()
    })
  })

  test('muda idioma para espanhol', async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    await act(async () => {
      await i18n.changeLanguage('es')
    })

    await waitFor(() => {
      expect(screen.getByRole('heading')).toHaveTextContent('Iniciar sesión')
      expect(screen.getByLabelText('Correo electrónico')).toBeInTheDocument()
      expect(screen.getByLabelText('Contraseña')).toBeInTheDocument()
    })
  })

  test('checkbox "Lembrar-me" funciona corretamente', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    const checkbox = screen.getByRole('checkbox', { name: /remember me/i })
    expect(checkbox).not.toBeChecked()

    fireEvent.click(checkbox)
    expect(checkbox).toBeChecked()
  })

  test('link "Esqueceu sua senha" está presente', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    const forgotPasswordLink = screen.getByRole('button', { name: /forgot your password/i })
    expect(forgotPasswordLink).toBeInTheDocument()
  })

  test('campos obrigatórios são marcados corretamente', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)

    expect(emailInput).toBeRequired()
    expect(passwordInput).toBeRequired()
  })

  test('mostra mensagens de erro quando o formulário é inválido', async () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    )

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitButton = screen.getByRole('button', { name: /sign in/i })

    fireEvent.change(emailInput, { target: { value: 'email-invalido' } })
    fireEvent.change(passwordInput, { target: { value: '123' } })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid email address/i)).toBeInTheDocument()
      expect(screen.getByText(/Password must be at least 6 characters long/i)).toBeInTheDocument()
    })
  })
})
