import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from 'react';
import GlobalStyles from '@mui/joy/GlobalStyles';
import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Divider from '@mui/joy/Divider';
import IconButton from '@mui/joy/IconButton';
import Input from '@mui/joy/Input';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import ListItemButton, { listItemButtonClasses } from '@mui/joy/ListItemButton';
import ListItemContent from '@mui/joy/ListItemContent';
import Typography from '@mui/joy/Typography';
import Sheet from '@mui/joy/Sheet';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';
import SupportRoundedIcon from '@mui/icons-material/SupportRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import ListAltRoundedIcon from '@mui/icons-material/ListAltRounded';
import { useNavigate } from 'react-router-dom';
import ColorSchemeToggle from '../../shared-theme/components/ColorSchemeToggle';
import { closeSidebar } from '../../shared-theme/components/utils';
import { LogoIcon } from '../../shared-theme/components/CustomIcons';
function Toggler({ defaultExpanded = false, renderToggle, children, }) {
    const [open, setOpen] = React.useState(defaultExpanded);
    return (_jsxs(React.Fragment, { children: [renderToggle({ open, setOpen }), _jsx(Box, { sx: [
                    {
                        display: 'grid',
                        transition: '0.2s ease',
                        '& > *': {
                            overflow: 'hidden',
                        },
                    },
                    open ? { gridTemplateRows: '1fr' } : { gridTemplateRows: '0fr' },
                ], children: children })] }));
}
const DEFAULT_AVATAR = '/default-avatar.png'; // Coloque a imagem padrão em public/default-avatar.png
function getCurrentUser() {
    try {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
    catch {
        return null;
    }
}
export default function Sidebar() {
    const user = getCurrentUser();
    const navigate = useNavigate();
    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    };
    const handleNavigation = (path) => {
        navigate(path);
    };
    return (_jsxs(Sheet, { className: "Sidebar", sx: {
            position: { xs: 'fixed', md: 'sticky' },
            transform: {
                xs: 'translateX(calc(100% * (var(--SideNavigation-slideIn, 0) - 1)))',
                md: 'none',
            },
            transition: 'transform 0.4s, width 0.4s',
            zIndex: 10000,
            height: '100dvh',
            width: 'var(--Sidebar-width)',
            top: 0,
            p: 2,
            flexShrink: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            borderRight: '1px solid',
            borderColor: 'divider',
        }, children: [_jsx(GlobalStyles, { styles: (theme) => ({
                    ':root': {
                        '--Sidebar-width': '220px',
                        [theme.breakpoints.up('lg')]: {
                            '--Sidebar-width': '240px',
                        },
                    },
                }) }), _jsx(Box, { className: "Sidebar-overlay", sx: {
                    position: 'fixed',
                    zIndex: 9998,
                    top: 0,
                    left: 0,
                    width: '100vw',
                    height: '100vh',
                    opacity: 'var(--SideNavigation-slideIn)',
                    backgroundColor: 'var(--joy-palette-background-backdrop)',
                    transition: 'opacity 0.4s',
                    transform: {
                        xs: 'translateX(calc(100% * (var(--SideNavigation-slideIn, 0) - 1) + var(--SideNavigation-slideIn, 0) * var(--Sidebar-width, 0px)))',
                        lg: 'translateX(-100%)',
                    },
                }, onClick: () => closeSidebar() }), _jsxs(Box, { sx: { display: 'flex', gap: 1, alignItems: 'center' }, children: [_jsx(LogoIcon, {}), _jsx(ColorSchemeToggle, { sx: { ml: 'auto' } })] }), _jsx(Input, { size: "sm", startDecorator: _jsx(SearchRoundedIcon, {}), placeholder: "Search" }), _jsxs(Box, { sx: {
                    minHeight: 0,
                    overflow: 'hidden auto',
                    flexGrow: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    [`& .${listItemButtonClasses.root}`]: {
                        gap: 1.5,
                    },
                }, children: [_jsxs(List, { size: "sm", sx: {
                            gap: 1,
                            '--List-nestedInsetStart': '30px',
                            '--ListItem-radius': (theme) => theme.vars.radius.sm,
                        }, children: [_jsx(ListItem, { children: _jsxs(ListItemButton, { children: [_jsx(HomeRoundedIcon, {}), _jsx(ListItemContent, { children: _jsx(Typography, { level: "title-sm", children: "Home" }) })] }) }), _jsx(ListItem, { children: _jsxs(ListItemButton, { onClick: () => handleNavigation('/dashboard'), children: [_jsx(DashboardRoundedIcon, {}), _jsx(ListItemContent, { children: _jsx(Typography, { level: "title-sm", children: "Dashboard" }) })] }) }), _jsx(ListItem, { nested: true, children: _jsx(Toggler, { renderToggle: ({ open, setOpen }) => (_jsxs(ListItemButton, { onClick: () => setOpen(!open), children: [_jsx(GroupRoundedIcon, {}), _jsx(ListItemContent, { children: _jsx(Typography, { level: "title-sm", children: "Users" }) }), _jsx(KeyboardArrowDownIcon, { sx: [
                                                    open
                                                        ? {
                                                            transform: 'rotate(180deg)',
                                                        }
                                                        : {
                                                            transform: 'rotate(0deg)',
                                                        },
                                                ] })] })), children: _jsx(List, { sx: { gap: 0.5 }, children: _jsx(ListItem, { children: _jsxs(ListItemButton, { onClick: () => handleNavigation('/users'), children: [_jsx(ListAltRoundedIcon, {}), _jsx(ListItemContent, { children: _jsx(Typography, { level: "title-sm", children: "List Users" }) })] }) }) }) }) })] }), _jsxs(List, { size: "sm", sx: {
                            mt: 'auto',
                            flexGrow: 0,
                            '--ListItem-radius': (theme) => theme.vars.radius.sm,
                            '--List-gap': '8px',
                            mb: 2,
                        }, children: [_jsx(ListItem, { children: _jsxs(ListItemButton, { children: [_jsx(SupportRoundedIcon, {}), "Support"] }) }), _jsx(ListItem, { children: _jsxs(ListItemButton, { children: [_jsx(SettingsRoundedIcon, {}), "Settings"] }) })] })] }), _jsx(Divider, {}), _jsxs(Box, { sx: { display: 'flex', gap: 1, alignItems: 'center' }, children: [_jsx(Avatar, { variant: "outlined", size: "sm", src: user?.photo || DEFAULT_AVATAR }), _jsxs(Box, { sx: { minWidth: 0, flex: 1 }, children: [_jsx(Typography, { level: "title-sm", children: user?.name || '' }), _jsx(Typography, { level: "body-xs", children: user?.email || '' })] }), _jsx(IconButton, { size: "sm", variant: "plain", color: "neutral", onClick: handleLogout, children: _jsx(LogoutRoundedIcon, {}) })] })] }));
}
