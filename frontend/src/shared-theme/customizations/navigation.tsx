import { Theme, Components } from '@mui/material/styles';
import { alpha } from '@mui/system';
import { gray, brand } from '../themePrimitives';

interface CustomTheme extends Theme {
  applyStyles: (mode: string, styles: Record<string, unknown>) => Record<string, unknown>;
}

export const navigationCustomizations: Components<CustomTheme> = {
  MuiAppBar: {
    styleOverrides: {
      root: ({ theme }) => ({
        backgroundColor: theme.palette.background.default,
        color: theme.palette.text.primary,
        boxShadow: 'none',
        borderBottom: `1px solid ${theme.palette.divider}`,
        ...(theme.applyStyles('dark', {
          backgroundColor: theme.palette.background.default,
        })),
      }),
    },
  },
  MuiToolbar: {
    styleOverrides: {
      root: ({ theme }) => ({
        minHeight: '64px !important',
        padding: '0 24px',
        ...(theme.applyStyles('dark', {
          backgroundColor: theme.palette.background.default,
        })),
      }),
    },
  },
  MuiDrawer: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          backgroundColor: theme.palette.background.default,
          borderRight: `1px solid ${theme.palette.divider}`,
          ...(theme.applyStyles('dark', {
            backgroundColor: theme.palette.background.default,
          })),
        },
      }),
    },
  },
  MuiList: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        padding: '8px',
        ...(theme.applyStyles('dark', {
          backgroundColor: theme.palette.background.default,
        })),
      }),
    },
  },
  MuiListItem: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        borderRadius: theme.shape.borderRadius,
        marginBottom: '4px',
        '&:last-child': {
          marginBottom: 0,
        },
        ...(theme.applyStyles('dark', {
          backgroundColor: theme.palette.background.default,
        })),
      }),
    },
  },
  MuiListItemButton: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        minWidth: '40px',
        color: theme.palette.text.secondary,
        ...(theme.applyStyles('dark', {
          color: theme.palette.text.secondary,
        })),
      }),
    },
  },
  MuiListItemIcon: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        minWidth: '40px',
        color: theme.palette.text.secondary,
        ...(theme.applyStyles('dark', {
          color: theme.palette.text.secondary,
        })),
      }),
    },
  },
  MuiListItemText: {
    styleOverrides: {
      root: () => ({
        margin: 0,
        '& .MuiTypography-root': {
          fontSize: '0.875rem',
          fontWeight: 500,
        },
      }),
    },
  },
  MuiBottomNavigation: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        backgroundColor: theme.palette.background.default,
        borderTop: `1px solid ${theme.palette.divider}`,
        height: 56,
        ...(theme.applyStyles('dark', {
          backgroundColor: theme.palette.grey[900],
          '& .MuiBottomNavigationAction-root': {
            color: theme.palette.grey[400],
            '&.Mui-selected': {
              color: theme.palette.grey[50],
            },
          },
        })),
      }),
    },
  },
  MuiBottomNavigationAction: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        color: theme.palette.grey[800],
        '&.Mui-selected': {
          color: theme.palette.grey[200],
        },
      }),
    },
  },
  MuiBreadcrumbs: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        color: theme.palette.text.secondary,
        fontSize: '0.875rem',
        '& .MuiBreadcrumbs-separator': {
          margin: '0 8px',
        },
        '& .MuiBreadcrumbs-li': {
          '&:last-child': {
            color: theme.palette.text.primary,
          },
          '& .MuiLink-root': {
            color: 'inherit',
            textDecoration: 'none',
            '&:hover': {
              textDecoration: 'underline',
            },
          },
        },
      }),
    },
  },
  MuiPagination: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        '& .MuiPaginationItem-root': {
          borderColor: theme.palette.divider,
          '&.Mui-selected': {
            backgroundColor: theme.palette.primary.main,
            color: theme.palette.primary.contrastText,
            '&:hover': {
              backgroundColor: theme.palette.primary.dark,
            },
          },
          '&.MuiPaginationItem-ellipsis': {
            border: 'none',
          },
        },
      }),
    },
  },
  MuiPaginationItem: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        '&.Mui-selected': {
          backgroundColor: theme.palette.primary.main,
          color: theme.palette.primary.contrastText,
          '&:hover': {
            backgroundColor: theme.palette.primary.light,
          },
        },
        '&.MuiPaginationItem-ellipsis': {
          border: 'none',
        },
      }),
    },
  },
  MuiMenuItem: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        borderRadius: theme.shape.borderRadius,
        margin: '4px 8px',
        padding: '8px 16px',
        '&:hover': {
          backgroundColor: theme.palette.action.hover,
        },
        '&.Mui-selected': {
          backgroundColor: theme.palette.action.selected,
          '&:hover': {
            backgroundColor: theme.palette.action.selected,
          },
        },
        ...(theme.applyStyles('dark', {
          '&:hover': {
            backgroundColor: theme.palette.action.hover,
          },
          '&.Mui-selected': {
            backgroundColor: theme.palette.action.selected,
            '&:hover': {
              backgroundColor: theme.palette.action.selected,
            },
          },
        })),
      }),
    },
  },
  MuiMenu: {
    styleOverrides: {
      list: {
        gap: '0px',
        [`& .MuiDivider-root`]: {
          margin: '0 -8px',
        },
      },
      paper: ({ theme }: { theme: CustomTheme }) => ({
        marginTop: '4px',
        borderRadius: theme.shape.borderRadius,
        border: `1px solid ${theme.palette.divider}`,
        backgroundImage: 'none',
        background: 'hsl(0, 0%, 100%)',
        boxShadow:
          'hsla(220, 30%, 5%, 0.07) 0px 4px 16px 0px, hsla(220, 25%, 10%, 0.07) 0px 8px 16px -5px',
        [`& .MuiButtonBase-root`]: {
          '&.Mui-selected': {
            backgroundColor: alpha(theme.palette.action.selected, 0.3),
          },
        },
        ...(theme.applyStyles('dark', {
          background: gray[900],
          boxShadow:
            'hsla(220, 30%, 5%, 0.7) 0px 4px 16px 0px, hsla(220, 25%, 10%, 0.8) 0px 8px 16px -5px',
        })),
      }),
    },
  },
  MuiSelect: {
    styleOverrides: {
      root: ({ theme }) => ({
        '& .MuiSelect-select': {
          borderRadius: theme.shape.borderRadius,
          border: `1px solid ${theme.palette.divider}`,
          padding: '8px 16px',
          '&:focus': {
            backgroundColor: theme.palette.background.paper,
          },
        },
        '& .MuiOutlinedInput-notchedOutline': {
          display: 'none',
        },
        '&:hover': {
          '& .MuiSelect-select': {
            backgroundColor: theme.palette.background.paper,
          },
        },
        '&.Mui-focused': {
          '& .MuiSelect-select': {
            backgroundColor: theme.palette.background.paper,
          },
        },
      }),
    },
  },
  MuiLink: {
    defaultProps: {
      underline: 'none',
    },
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        color: theme.palette.text.primary,
        fontWeight: 500,
        position: 'relative',
        textDecoration: 'none',
        width: 'fit-content',
        '&::before': {
          content: '""',
          position: 'absolute',
          width: '100%',
          height: '1px',
          bottom: 0,
          left: 0,
          backgroundColor: theme.palette.text.secondary,
          opacity: 0.3,
          transition: 'width 0.3s ease, opacity 0.3s ease',
        },
        '&:hover::before': {
          width: 0,
        },
        '&:focus-visible': {
          outline: `3px solid ${alpha(brand[500], 0.5)}`,
          outlineOffset: '4px',
          borderRadius: '2px',
        },
      }),
    },
  },
  MuiTabs: {
    styleOverrides: {
      root: () => ({
        minHeight: 48,
        '& .MuiTabs-indicator': {
          height: 3,
          borderRadius: '3px 3px 0 0',
        },
      }),
    },
  },
  MuiTab: {
    styleOverrides: {
      root: () => ({
        textTransform: 'none',
        minHeight: 48,
        padding: '12px 16px',
        '&.Mui-selected': {
          fontWeight: 600,
        },
      }),
    },
  },
  MuiStepConnector: {
    styleOverrides: {
      line: ({ theme }: { theme: CustomTheme }) => ({
        borderTop: '1px solid',
        borderColor: theme.palette.divider,
        flex: 1,
        borderRadius: '99px',
      }),
    },
  },
  MuiStepIcon: {
    styleOverrides: {
      root: ({ theme }: { theme: CustomTheme }) => ({
        color: 'transparent',
        border: `1px solid ${gray[400]}`,
        width: 12,
        height: 12,
        borderRadius: '50%',
        '& text': {
          display: 'none',
        },
        '&.Mui-active': {
          border: 'none',
          color: theme.palette.primary.main,
        },
        '&.Mui-completed': {
          border: 'none',
          color: theme.palette.success.main,
        },
        ...(theme.applyStyles('dark', {
          border: `1px solid ${gray[700]}`,
          '&.Mui-active': {
            border: 'none',
            color: theme.palette.primary.light,
          },
          '&.Mui-completed': {
            border: 'none',
            color: theme.palette.success.light,
          },
        })),
        variants: [
          {
            props: { completed: true },
            style: {
              width: 12,
              height: 12,
            },
          },
        ],
      }),
    },
  },
  MuiStepLabel: {
    styleOverrides: {
      label: ({ theme }: { theme: CustomTheme }) => ({
        '&.Mui-completed': {
          opacity: 0.6,
          ...(theme.applyStyles('dark', { opacity: 0.5 })),
        },
      }),
    },
  },
};
