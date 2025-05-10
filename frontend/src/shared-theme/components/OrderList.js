import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Box from '@mui/joy/Box';
import Avatar from '@mui/joy/Avatar';
import Chip from '@mui/joy/Chip';
import Link from '@mui/joy/Link';
import Divider from '@mui/joy/Divider';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import ListItemContent from '@mui/joy/ListItemContent';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import ListDivider from '@mui/joy/ListDivider';
import Menu from '@mui/joy/Menu';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import Dropdown from '@mui/joy/Dropdown';
import MoreHorizRoundedIcon from '@mui/icons-material/MoreHorizRounded';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import BlockIcon from '@mui/icons-material/Block';
import AutorenewRoundedIcon from '@mui/icons-material/AutorenewRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
const listItems = [
    {
        id: 'INV-1234',
        date: 'Feb 3, 2023',
        status: 'Refunded',
        customer: {
            initial: 'O',
            name: 'Olivia Ryhe',
            email: 'olivia@email.com',
        },
    },
    {
        id: 'INV-1233',
        date: 'Feb 3, 2023',
        status: 'Paid',
        customer: {
            initial: 'S',
            name: 'Steve Hampton',
            email: 'steve.hamp@email.com',
        },
    },
    {
        id: 'INV-1232',
        date: 'Feb 3, 2023',
        status: 'Refunded',
        customer: {
            initial: 'C',
            name: 'Ciaran Murray',
            email: 'ciaran.murray@email.com',
        },
    },
    {
        id: 'INV-1231',
        date: 'Feb 3, 2023',
        status: 'Refunded',
        customer: {
            initial: 'M',
            name: 'Maria Macdonald',
            email: 'maria.mc@email.com',
        },
    },
    {
        id: 'INV-1230',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'C',
            name: 'Charles Fulton',
            email: 'fulton@email.com',
        },
    },
    {
        id: 'INV-1229',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'J',
            name: 'Jay Hooper',
            email: 'hooper@email.com',
        },
    },
];
function RowMenu() {
    return (_jsxs(Dropdown, { children: [_jsx(MenuButton, { slots: { root: IconButton }, slotProps: { root: { variant: 'plain', color: 'neutral', size: 'sm' } }, children: _jsx(MoreHorizRoundedIcon, {}) }), _jsxs(Menu, { size: "sm", sx: { minWidth: 140 }, children: [_jsx(MenuItem, { children: "Edit" }), _jsx(MenuItem, { children: "Rename" }), _jsx(MenuItem, { children: "Move" }), _jsx(Divider, {}), _jsx(MenuItem, { color: "danger", children: "Delete" })] })] }));
}
export default function OrderList() {
    return (_jsxs(Box, { sx: { display: { xs: 'block', sm: 'none' } }, children: [listItems.map((listItem) => (_jsxs(List, { size: "sm", sx: { '--ListItem-paddingX': 0 }, children: [_jsxs(ListItem, { sx: {
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'start',
                        }, children: [_jsxs(ListItemContent, { sx: { display: 'flex', gap: 2, alignItems: 'start' }, children: [_jsx(ListItemDecorator, { children: _jsx(Avatar, { size: "sm", children: listItem.customer.initial }) }), _jsxs("div", { children: [_jsx(Typography, { gutterBottom: true, sx: { fontWeight: 600 }, children: listItem.customer.name }), _jsx(Typography, { level: "body-xs", gutterBottom: true, children: listItem.customer.email }), _jsxs(Box, { sx: {
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'space-between',
                                                    gap: 0.5,
                                                    mb: 1,
                                                }, children: [_jsx(Typography, { level: "body-xs", children: listItem.date }), _jsx(Typography, { level: "body-xs", children: "\u2022" }), _jsx(Typography, { level: "body-xs", children: listItem.id })] }), _jsxs(Box, { sx: { display: 'flex', alignItems: 'center', gap: 1, mb: 1 }, children: [_jsx(Link, { level: "body-sm", component: "button", children: "Download" }), _jsx(RowMenu, {})] })] })] }), _jsx(Chip, { variant: "soft", size: "sm", startDecorator: {
                                    Paid: _jsx(CheckRoundedIcon, {}),
                                    Refunded: _jsx(AutorenewRoundedIcon, {}),
                                    Cancelled: _jsx(BlockIcon, {}),
                                }[listItem.status], color: {
                                    Paid: 'success',
                                    Refunded: 'neutral',
                                    Cancelled: 'danger',
                                }[listItem.status], children: listItem.status })] }), _jsx(ListDivider, {})] }, listItem.id))), _jsxs(Box, { className: "Pagination-mobile", sx: { display: { xs: 'flex', md: 'none' }, alignItems: 'center', py: 2 }, children: [_jsx(IconButton, { "aria-label": "previous page", variant: "outlined", color: "neutral", size: "sm", children: _jsx(KeyboardArrowLeftIcon, {}) }), _jsx(Typography, { level: "body-sm", sx: { mx: 'auto' }, children: "Page 1 of 10" }), _jsx(IconButton, { "aria-label": "next page", variant: "outlined", color: "neutral", size: "sm", children: _jsx(KeyboardArrowRightIcon, {}) })] })] }));
}
