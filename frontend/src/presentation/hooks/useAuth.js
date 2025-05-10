import { useState, useCallback } from 'react';
export function useAuth(authService) {
    const [user, setUser] = useState(authService.getCurrentUser());
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const login = useCallback(async (credentials) => {
        try {
            setLoading(true);
            setError(null);
            const user = await authService.login(credentials);
            setUser(user);
            return user;
        }
        catch (err) {
            setError(err instanceof Error ? err.message : 'Falha na autenticação');
            throw err;
        }
        finally {
            setLoading(false);
        }
    }, [authService]);
    const logout = useCallback(async () => {
        try {
            setLoading(true);
            await authService.logout();
            setUser(null);
        }
        catch (err) {
            setError(err instanceof Error ? err.message : 'Falha ao fazer logout');
        }
        finally {
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
