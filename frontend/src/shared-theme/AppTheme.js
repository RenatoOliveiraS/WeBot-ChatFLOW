import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { CssVarsProvider } from '@mui/joy/styles';
import CssBaseline from '@mui/joy/CssBaseline';
export default function AppTheme({ children, disableCustomTheme: _disableCustomTheme = false }) {
    return (_jsxs(CssVarsProvider, { defaultMode: "light", colorSchemeStorageKey: "template-color-scheme", modeStorageKey: "template-mode", disableTransitionOnChange: true, children: [_jsx(CssBaseline, {}), children] }));
}
