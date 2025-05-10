import * as React from 'react';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';

import Sidebar from './Sidebar';
import Header from '../../shared-theme/components/Header';
import AppTheme from '../../shared-theme/AppTheme';

export default function JoyOrderDashboardTemplate() {
  return (
    <AppTheme>
      <Box sx={{ display: 'flex', minHeight: '100dvh' }}>
        <Header />
        <Sidebar />
        <Box
          component="main"
          className="MainContent"
          sx={{
            px: { xs: 2, md: 6 },
            pt: {
              xs: 'calc(12px + var(--Header-height))',
              sm: 'calc(12px + var(--Header-height))',
              md: 3,
            },
            pb: { xs: 2, sm: 2, md: 3 },
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            minWidth: 0,
            height: '100dvh',
            gap: 1,
          }}
        >
          <Typography level="h1">Hello World</Typography>
        </Box>
      </Box>
    </AppTheme>
  );
}
