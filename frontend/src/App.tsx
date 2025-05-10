// frontend/src/App.tsx

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthContext } from './presentation/contexts/AuthContext';
import Login from './presentation/pages/Login';
import Dashboard from './presentation/pages/Dashboard';
import UserList from './presentation/pages/UserList';

function App() {
  const { isAuthenticated } = useAuthContext();

  return (
    <Routes>
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />}
      />
      <Route
        path="/dashboard"
        element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
      />
      <Route
        path="/users"
        element={isAuthenticated ? <UserList /> : <Navigate to="/login" />}
      />
      <Route path="/" element={<Navigate to="/login" />} />
    </Routes>
  );
}

export default App;
