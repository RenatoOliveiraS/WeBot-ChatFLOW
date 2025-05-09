import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from 'react';
import { useColorScheme } from '@mui/joy/styles';
import IconButton from '@mui/joy/IconButton';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeIcon from '@mui/icons-material/LightMode';
export default function ColorSchemeToggle(props) {
    const { onClick, sx, ...other } = props;
    const { mode, setMode } = useColorScheme();
    const [mounted, setMounted] = React.useState(false);
    React.useEffect(() => {
        setMounted(true);
    }, []);
    if (!mounted) {
        return (_jsx(IconButton, { size: "sm", variant: "outlined", color: "neutral", ...other, sx: sx, disabled: true }));
    }
    return (_jsxs(IconButton, { "data-screenshot": "toggle-mode", size: "sm", variant: "outlined", color: "neutral", ...other, onClick: (event) => {
            if (mode === 'light') {
                setMode('dark');
            }
            else {
                setMode('light');
            }
            onClick?.(event);
        }, sx: [
            mode === 'dark'
                ? { '& > *:first-child': { display: 'none' } }
                : { '& > *:first-child': { display: 'initial' } },
            mode === 'light'
                ? { '& > *:last-child': { display: 'none' } }
                : { '& > *:last-child': { display: 'initial' } },
            ...(Array.isArray(sx) ? sx : [sx]),
        ], children: [_jsx(DarkModeRoundedIcon, {}), _jsx(LightModeIcon, {})] }));
}
