import * as React from 'react';
import { useTranslation } from 'react-i18next';
import IconButton from '@mui/joy/IconButton';
import Menu from '@mui/joy/Menu';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import Dropdown from '@mui/joy/Dropdown';
import Tooltip from '@mui/joy/Tooltip';
import LanguageIcon from '@mui/icons-material/Language';
import { SxProps } from '@mui/system';

interface LanguageSelectProps {
  sx?: SxProps;
}

export default function LanguageSelect({ sx }: LanguageSelectProps) {
  const { i18n } = useTranslation();

  const handleLanguageChange = (language: string) => {
    i18n.changeLanguage(language);
  };

  return (
    <Dropdown>
      <Tooltip title="Mudar idioma">
        <MenuButton
          slots={{ root: IconButton }}
          slotProps={{ root: { variant: 'plain', color: 'neutral', size: 'sm', sx } }}
        >
          <LanguageIcon />
        </MenuButton>
      </Tooltip>
      <Menu>
        <MenuItem onClick={() => handleLanguageChange('pt')}>Português</MenuItem>
        <MenuItem onClick={() => handleLanguageChange('en')}>English</MenuItem>
        <MenuItem onClick={() => handleLanguageChange('es')}>Español</MenuItem>
      </Menu>
    </Dropdown>
  );
} 