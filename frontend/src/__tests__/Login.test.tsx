// src/__tests__/Login.test.tsx

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import LoginPage from '../pages/Login'
import DashboardPage from '../pages/Dashboard'
import * as authService from '../services/authService'

// mantemos o mock do authService
jest.spyOn(authService, 'login').mockImplementation(({ password }) => {
  return password === '123456'
    ? Promise.resolve({ data: { token: 'mock-token' } })
    : Promise.reject({ response: { data: { message: 'Usuário ou senha inválidos' } } })
})

describe('LoginPage', () => {
  test('mostra erro quando senha é inválida', async () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </MemoryRouter>
    )

    // CORREÇÃO: buscar pelo label "Email", não "E-mail Address"
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'teste@ex.com' },
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'senhaErrada' },
    })
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))

    const alert = await screen.findByText('Usuário ou senha inválidos')
    expect(alert).toBeVisible()
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

    // CORREÇÃO AQUI TAMBÉM
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'teste@ex.com' },
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: '123456' },
    })
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(screen.getByText(/Hello Dashboard/i)).toBeInTheDocument()
    })
  })
})
