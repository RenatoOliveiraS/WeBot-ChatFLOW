import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import Sidebar from './Sidebar';
import Header from '../../shared-theme/components/Header';
import AppTheme from '../../shared-theme/AppTheme';
export default function JoyOrderDashboardTemplate() {
    return (_jsx(AppTheme, { children: _jsxs(Box, { sx: { display: 'flex', minHeight: '100dvh' }, children: [_jsx(Header, {}), _jsx(Sidebar, {}), _jsx(Box, { component: "main", className: "MainContent", sx: {
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
                    }, children: _jsx(Typography, { level: "h1", children: "Hello World" }) })] }) }));
}
