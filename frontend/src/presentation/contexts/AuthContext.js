import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext } from 'react';
import { useAuth } from '../hooks/useAuth';
const AuthContext = createContext(null);
export function AuthProvider({ children, authService }) {
    const auth = useAuth(authService);
    return (_jsx(AuthContext.Provider, { value: auth, children: children }));
}
export function useAuthContext() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuthContext must be used within an AuthProvider');
    }
    return context;
}
