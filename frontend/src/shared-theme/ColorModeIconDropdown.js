import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from 'react';
import DarkModeIcon from '@mui/icons-material/DarkModeRounded';
import LightModeIcon from '@mui/icons-material/LightModeRounded';
import Box from '@mui/joy/Box';
import IconButton from '@mui/joy/IconButton';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import { useColorScheme } from '@mui/joy/styles';
export default function ColorModeIconDropdown(props) {
    const { mode, systemMode, setMode } = useColorScheme();
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
    const handleMode = (targetMode) => () => {
        setMode(targetMode);
        handleClose();
    };
    if (!mode) {
        return (_jsx(Box, { "data-screenshot": "toggle-mode", sx: (theme) => ({
                verticalAlign: 'bottom',
                display: 'inline-flex',
                width: '2.25rem',
                height: '2.25rem',
                borderRadius: theme.radius.sm,
                border: '1px solid',
                borderColor: theme.palette.divider,
            }) }));
    }
    const resolvedMode = (systemMode || mode);
    const icon = {
        light: _jsx(LightModeIcon, {}),
        dark: _jsx(DarkModeIcon, {}),
    }[resolvedMode];
    return (_jsxs(React.Fragment, { children: [_jsx(IconButton, { "data-screenshot": "toggle-mode", onClick: handleClick, size: "sm", variant: "plain", color: "neutral", "aria-controls": open ? 'color-scheme-menu' : undefined, "aria-haspopup": "true", "aria-expanded": open ? 'true' : undefined, ...props, children: icon }), _jsxs(Menu, { anchorEl: anchorEl, id: "account-menu", open: open, onClose: handleClose, onClick: handleClose, variant: "outlined", sx: {
                    my: '4px',
                }, placement: "bottom-end", children: [_jsx(MenuItem, { selected: mode === 'system', onClick: handleMode('system'), children: "System" }), _jsx(MenuItem, { selected: mode === 'light', onClick: handleMode('light'), children: "Light" }), _jsx(MenuItem, { selected: mode === 'dark', onClick: handleMode('dark'), children: "Dark" })] })] }));
}
