import * as React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuthContext } from '../contexts/AuthContext';
import { Box, Typography, Button } from '@mui/material';

export default function Dashboard() {
  const { t } = useTranslation();
  const { logout, user } = useAuthContext();

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="body1" gutterBottom>
        Bem-vindo, {user?.name || 'Usuário'}!
      </Typography>
      <Button variant="contained" color="primary" onClick={logout}>
        Sair
      </Button>
    </Box>
  );
} 