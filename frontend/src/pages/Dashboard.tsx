// frontend/src/pages/Dashboard.tsx

import React from 'react';
import { Container, Box, Typography } from '@mui/material';

const DashboardPage: React.FC = () => {
  return (
    <Container maxWidth="md">
      <Box
        mt={8}
        display="flex"
        flexDirection="column"
        alignItems="center"
      >
        <Typography component="h1" variant="h4">
          Hello Dashboard
        </Typography>
      </Box>
    </Container>
  );
};

export default DashboardPage;
