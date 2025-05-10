import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useTranslation } from 'react-i18next';
import IconButton from '@mui/joy/IconButton';
import Menu from '@mui/joy/Menu';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import Dropdown from '@mui/joy/Dropdown';
import Tooltip from '@mui/joy/Tooltip';
import LanguageIcon from '@mui/icons-material/Language';
export default function LanguageSelect({ sx }) {
    const { i18n } = useTranslation();
    const handleLanguageChange = (language) => {
        i18n.changeLanguage(language);
    };
    return (_jsxs(Dropdown, { children: [_jsx(Tooltip, { title: "Mudar idioma", children: _jsx(MenuButton, { slots: { root: IconButton }, slotProps: { root: { variant: 'plain', color: 'neutral', size: 'sm', sx } }, children: _jsx(LanguageIcon, {}) }) }), _jsxs(Menu, { children: [_jsx(MenuItem, { onClick: () => handleLanguageChange('pt'), children: "Portugu\u00EAs" }), _jsx(MenuItem, { onClick: () => handleLanguageChange('en'), children: "English" }), _jsx(MenuItem, { onClick: () => handleLanguageChange('es'), children: "Espa\u00F1ol" })] })] }));
}
