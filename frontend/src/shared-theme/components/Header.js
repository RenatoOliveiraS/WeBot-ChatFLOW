import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import GlobalStyles from '@mui/joy/GlobalStyles';
import Sheet from '@mui/joy/Sheet';
import IconButton from '@mui/joy/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { toggleSidebar } from '../../shared-theme/components/utils';
export default function Header() {
    return (_jsxs(Sheet, { sx: {
            display: { xs: 'flex', md: 'none' },
            alignItems: 'center',
            justifyContent: 'space-between',
            position: 'fixed',
            top: 0,
            width: '100vw',
            height: 'var(--Header-height)',
            zIndex: 9995,
            p: 2,
            gap: 1,
            borderBottom: '1px solid',
            borderColor: 'background.level1',
            boxShadow: 'sm',
        }, children: [_jsx(GlobalStyles, { styles: (theme) => ({
                    ':root': {
                        '--Header-height': '52px',
                        [theme.breakpoints.up('md')]: {
                            '--Header-height': '0px',
                        },
                    },
                }) }), _jsx(IconButton, { onClick: () => toggleSidebar(), variant: "outlined", color: "neutral", size: "sm", children: _jsx(MenuIcon, {}) })] }));
}
