import { useState, useCallback } from 'react';
import { User, LoginCredentials } from '../../core/domain/entities/User';
import { AuthService } from '../../core/interfaces/services/AuthService';

export function useAuth(authService: AuthService) {
  const [user, setUser] = useState<User | null>(authService.getCurrentUser());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (credentials: LoginCredentials) => {
    try {
      setLoading(true);
      setError(null);
      const user = await authService.login(credentials);
      setUser(user);
      return user;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Falha na autenticação');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [authService]);

  const logout = useCallback(async () => {
    try {
      setLoading(true);
      await authService.logout();
      setUser(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Falha ao fazer logout');
    } finally {
      setLoading(false);
    }
  }, [authService]);

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: authService.isAuthenticated(),
  };
} 