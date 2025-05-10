import { Theme, Components } from '@mui/joy/styles';
import { gray } from '../themePrimitives';

export const surfacesCustomizations: Components<Theme> = {
  JoyAccordion: {
    styleOverrides: {
      root: ({ theme }: { theme: Theme }) => ({
        padding: 4,
        overflow: 'clip',
        backgroundColor: theme.palette.background.surface,
        border: '1px solid',
        borderColor: theme.palette.divider,
        ':before': {
          backgroundColor: 'transparent',
        },
        '&:not(:last-of-type)': {
          borderBottom: 'none',
        },
        '&:first-of-type': {
          borderTopLeftRadius: theme.radius.sm,
          borderTopRightRadius: theme.radius.sm,
        },
        '&:last-of-type': {
          borderBottomLeftRadius: theme.radius.sm,
          borderBottomRightRadius: theme.radius.sm,
        },
      }),
    },
  },
  JoyAccordionSummary: {
    styleOverrides: {
      root: ({ theme }: { theme: Theme }) => ({
        border: 'none',
        borderRadius: 8,
        '&:hover': { backgroundColor: gray[50] },
        '&:focus-visible': { backgroundColor: 'transparent' },
        ...theme.applyStyles('dark', {
          '&:hover': { backgroundColor: gray[800] },
        }),
      }),
    },
  },
  JoyAccordionDetails: {
    styleOverrides: {
      root: { mb: 20, border: 'none' },
    },
  },
  JoyCard: {
    styleOverrides: {
      root: ({ theme }: { theme: Theme }) => {
        return {
          padding: 16,
          gap: 16,
          transition: 'all 100ms ease',
          backgroundColor: gray[50],
          borderRadius: theme.radius.sm,
          border: `1px solid ${theme.palette.divider}`,
          boxShadow: 'none',
          ...theme.applyStyles('dark', {
            backgroundColor: gray[800],
          }),
          variants: [
            {
              props: {
                variant: 'outlined',
              },
              style: {
                border: `1px solid ${theme.palette.divider}`,
                boxShadow: 'none',
                background: 'hsl(0, 0%, 100%)',
                ...theme.applyStyles('dark', {
                  background: gray[900],
                }),
              },
            },
          ],
        };
      },
    },
  },
  JoyCardContent: {
    styleOverrides: {
      root: {
        padding: 0,
        '&:last-child': { paddingBottom: 0 },
      },
    },
  },
  JoyCardHeader: {
    styleOverrides: {
      root: {
        padding: 0,
      },
    },
  },
  JoyCardActions: {
    styleOverrides: {
      root: {
        padding: 0,
      },
    },
  },
  JoySheet: {
    styleOverrides: {
      root: ({ theme }: { theme: Theme }) => ({
        padding: 4,
        overflow: 'clip',
        backgroundColor: theme.palette.background.surface,
        border: '1px solid',
        borderColor: theme.palette.divider,
        borderRadius: theme.radius.sm,
      }),
    },
  },
};
