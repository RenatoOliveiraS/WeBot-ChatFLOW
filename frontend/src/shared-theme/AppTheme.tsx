import * as React from 'react';
import { CssVarsProvider } from '@mui/joy/styles';
import CssBaseline from '@mui/joy/CssBaseline';

interface AppThemeProps {
  children: React.ReactNode;
  /**
   * This is for the docs site. You can ignore it or remove it.
   */
  disableCustomTheme?: boolean;
}

export default function AppTheme({ children, disableCustomTheme: _disableCustomTheme = false }: AppThemeProps) {
  return (
    <CssVarsProvider
      defaultMode="light"
      colorSchemeStorageKey="template-color-scheme"
      modeStorageKey="template-mode"
      disableTransitionOnChange
    >
      <CssBaseline />
      {children}
    </CssVarsProvider>
  );
}