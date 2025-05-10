import { gray } from '../themePrimitives';
export const surfacesCustomizations = {
    JoyCard: {
        styleOverrides: {
            root: ({ theme }) => ({
                padding: '16px',
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
            }),
        },
    },
    JoySheet: {
        styleOverrides: {
            root: ({ theme }) => ({
                padding: '4px',
                overflow: 'clip',
                backgroundColor: theme.palette.background.surface,
                border: '1px solid',
                borderColor: theme.palette.divider,
                borderRadius: theme.radius.sm,
            }),
        },
    },
};
