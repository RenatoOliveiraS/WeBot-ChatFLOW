import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthContext } from './presentation/contexts/AuthContext';
import Login from './presentation/pages/Login';
import Dashboard from './presentation/pages/Dashboard';
import UserList from './presentation/pages/UserList';
function App() {
    const { isAuthenticated } = useAuthContext();
    return (_jsxs(Routes, { children: [_jsx(Route, { path: "/login", element: isAuthenticated ? _jsx(Navigate, { to: "/dashboard" }) : _jsx(Login, {}) }), _jsx(Route, { path: "/dashboard", element: isAuthenticated ? _jsx(Dashboard, {}) : _jsx(Navigate, { to: "/login" }) }), _jsx(Route, { path: "/users", element: isAuthenticated ? _jsx(UserList, {}) : _jsx(Navigate, { to: "/login" }) }), _jsx(Route, { path: "/", element: _jsx(Navigate, { to: "/login" }) })] }));
}
export default App;
