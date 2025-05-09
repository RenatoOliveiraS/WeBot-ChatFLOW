import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from 'react';
import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Chip from '@mui/joy/Chip';
import Divider from '@mui/joy/Divider';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Link from '@mui/joy/Link';
import Input from '@mui/joy/Input';
import Modal from '@mui/joy/Modal';
import ModalDialog from '@mui/joy/ModalDialog';
import ModalClose from '@mui/joy/ModalClose';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';
import Checkbox from '@mui/joy/Checkbox';
import IconButton, { iconButtonClasses } from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import Menu from '@mui/joy/Menu';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import Dropdown from '@mui/joy/Dropdown';
import FilterAltIcon from '@mui/icons-material/FilterAlt';
import SearchIcon from '@mui/icons-material/Search';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import BlockIcon from '@mui/icons-material/Block';
import AutorenewRoundedIcon from '@mui/icons-material/AutorenewRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import MoreHorizRoundedIcon from '@mui/icons-material/MoreHorizRounded';
const rows = [
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
    {
        id: 'INV-1228',
        date: 'Feb 3, 2023',
        status: 'Refunded',
        customer: {
            initial: 'K',
            name: 'Krystal Stevens',
            email: 'k.stevens@email.com',
        },
    },
    {
        id: 'INV-1227',
        date: 'Feb 3, 2023',
        status: 'Paid',
        customer: {
            initial: 'S',
            name: 'Sachin Flynn',
            email: 's.flyn@email.com',
        },
    },
    {
        id: 'INV-1226',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'B',
            name: 'Bradley Rosales',
            email: 'brad123@email.com',
        },
    },
    {
        id: 'INV-1225',
        date: 'Feb 3, 2023',
        status: 'Paid',
        customer: {
            initial: 'O',
            name: 'Olivia Ryhe',
            email: 'olivia@email.com',
        },
    },
    {
        id: 'INV-1224',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'S',
            name: 'Steve Hampton',
            email: 'steve.hamp@email.com',
        },
    },
    {
        id: 'INV-1223',
        date: 'Feb 3, 2023',
        status: 'Paid',
        customer: {
            initial: 'C',
            name: 'Ciaran Murray',
            email: 'ciaran.murray@email.com',
        },
    },
    {
        id: 'INV-1221',
        date: 'Feb 3, 2023',
        status: 'Refunded',
        customer: {
            initial: 'M',
            name: 'Maria Macdonald',
            email: 'maria.mc@email.com',
        },
    },
    {
        id: 'INV-1220',
        date: 'Feb 3, 2023',
        status: 'Paid',
        customer: {
            initial: 'C',
            name: 'Charles Fulton',
            email: 'fulton@email.com',
        },
    },
    {
        id: 'INV-1219',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'J',
            name: 'Jay Hooper',
            email: 'hooper@email.com',
        },
    },
    {
        id: 'INV-1218',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'K',
            name: 'Krystal Stevens',
            email: 'k.stevens@email.com',
        },
    },
    {
        id: 'INV-1217',
        date: 'Feb 3, 2023',
        status: 'Paid',
        customer: {
            initial: 'S',
            name: 'Sachin Flynn',
            email: 's.flyn@email.com',
        },
    },
    {
        id: 'INV-1216',
        date: 'Feb 3, 2023',
        status: 'Cancelled',
        customer: {
            initial: 'B',
            name: 'Bradley Rosales',
            email: 'brad123@email.com',
        },
    },
];
function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    return 0;
}
function getComparator(order, orderBy) {
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
}
function RowMenu() {
    return (_jsxs(Dropdown, { children: [_jsx(MenuButton, { slots: { root: IconButton }, slotProps: { root: { variant: 'plain', color: 'neutral', size: 'sm' } }, children: _jsx(MoreHorizRoundedIcon, {}) }), _jsxs(Menu, { size: "sm", sx: { minWidth: 140 }, children: [_jsx(MenuItem, { children: "Edit" }), _jsx(MenuItem, { children: "Rename" }), _jsx(MenuItem, { children: "Move" }), _jsx(Divider, {}), _jsx(MenuItem, { color: "danger", children: "Delete" })] })] }));
}
export default function OrderTable() {
    const [order, setOrder] = React.useState('desc');
    const [selected, setSelected] = React.useState([]);
    const [open, setOpen] = React.useState(false);
    const renderFilters = () => (_jsxs(React.Fragment, { children: [_jsxs(FormControl, { size: "sm", children: [_jsx(FormLabel, { children: "Status" }), _jsxs(Select, { size: "sm", placeholder: "Filter by status", slotProps: { button: { sx: { whiteSpace: 'nowrap' } } }, children: [_jsx(Option, { value: "paid", children: "Paid" }), _jsx(Option, { value: "pending", children: "Pending" }), _jsx(Option, { value: "refunded", children: "Refunded" }), _jsx(Option, { value: "cancelled", children: "Cancelled" })] })] }), _jsxs(FormControl, { size: "sm", children: [_jsx(FormLabel, { children: "Category" }), _jsxs(Select, { size: "sm", placeholder: "All", children: [_jsx(Option, { value: "all", children: "All" }), _jsx(Option, { value: "refund", children: "Refund" }), _jsx(Option, { value: "purchase", children: "Purchase" }), _jsx(Option, { value: "debit", children: "Debit" })] })] }), _jsxs(FormControl, { size: "sm", children: [_jsx(FormLabel, { children: "Customer" }), _jsxs(Select, { size: "sm", placeholder: "All", children: [_jsx(Option, { value: "all", children: "All" }), _jsx(Option, { value: "olivia", children: "Olivia Rhye" }), _jsx(Option, { value: "steve", children: "Steve Hampton" }), _jsx(Option, { value: "ciaran", children: "Ciaran Murray" }), _jsx(Option, { value: "marina", children: "Marina Macdonald" }), _jsx(Option, { value: "charles", children: "Charles Fulton" }), _jsx(Option, { value: "jay", children: "Jay Hoper" })] })] })] }));
    return (_jsxs(React.Fragment, { children: [_jsxs(Sheet, { className: "SearchAndFilters-mobile", sx: { display: { xs: 'flex', sm: 'none' }, my: 1, gap: 1 }, children: [_jsx(Input, { size: "sm", placeholder: "Search", startDecorator: _jsx(SearchIcon, {}), sx: { flexGrow: 1 } }), _jsx(IconButton, { size: "sm", variant: "outlined", color: "neutral", onClick: () => setOpen(true), children: _jsx(FilterAltIcon, {}) }), _jsx(Modal, { open: open, onClose: () => setOpen(false), children: _jsxs(ModalDialog, { "aria-labelledby": "filter-modal", layout: "fullscreen", children: [_jsx(ModalClose, {}), _jsx(Typography, { id: "filter-modal", level: "h2", children: "Filters" }), _jsx(Divider, { sx: { my: 2 } }), _jsxs(Sheet, { sx: { display: 'flex', flexDirection: 'column', gap: 2 }, children: [renderFilters(), _jsx(Button, { color: "primary", onClick: () => setOpen(false), children: "Submit" })] })] }) })] }), _jsxs(Box, { className: "SearchAndFilters-tabletUp", sx: {
                    borderRadius: 'sm',
                    py: 2,
                    display: { xs: 'none', sm: 'flex' },
                    flexWrap: 'wrap',
                    gap: 1.5,
                    '& > *': {
                        minWidth: { xs: '120px', md: '160px' },
                    },
                }, children: [_jsxs(FormControl, { sx: { flex: 1 }, size: "sm", children: [_jsx(FormLabel, { children: "Search for order" }), _jsx(Input, { size: "sm", placeholder: "Search", startDecorator: _jsx(SearchIcon, {}) })] }), renderFilters()] }), _jsx(Sheet, { className: "OrderTableContainer", variant: "outlined", sx: {
                    display: { xs: 'none', sm: 'initial' },
                    width: '100%',
                    borderRadius: 'sm',
                    flexShrink: 1,
                    overflow: 'auto',
                    minHeight: 0,
                }, children: _jsxs(Table, { "aria-labelledby": "tableTitle", stickyHeader: true, hoverRow: true, sx: {
                        '--TableCell-headBackground': 'var(--joy-palette-background-level1)',
                        '--Table-headerUnderlineThickness': '1px',
                        '--TableRow-hoverBackground': 'var(--joy-palette-background-level1)',
                        '--TableCell-paddingY': '4px',
                        '--TableCell-paddingX': '8px',
                    }, children: [_jsx("thead", { children: _jsxs("tr", { children: [_jsx("th", { style: { width: 48, textAlign: 'center', padding: '12px 6px' }, children: _jsx(Checkbox, { size: "sm", indeterminate: selected.length > 0 && selected.length !== rows.length, checked: selected.length === rows.length, onChange: (event) => {
                                                setSelected(event.target.checked ? rows.map((row) => row.id) : []);
                                            }, color: selected.length > 0 || selected.length === rows.length
                                                ? 'primary'
                                                : undefined, sx: { verticalAlign: 'text-bottom' } }) }), _jsx("th", { style: { width: 120, padding: '12px 6px' }, children: _jsx(Link, { underline: "none", color: "primary", component: "button", onClick: () => setOrder(order === 'asc' ? 'desc' : 'asc'), endDecorator: _jsx(ArrowDropDownIcon, {}), sx: [
                                                {
                                                    fontWeight: 'lg',
                                                    '& svg': {
                                                        transition: '0.2s',
                                                        transform: order === 'desc' ? 'rotate(0deg)' : 'rotate(180deg)',
                                                    },
                                                },
                                                order === 'desc'
                                                    ? { '& svg': { transform: 'rotate(0deg)' } }
                                                    : { '& svg': { transform: 'rotate(180deg)' } },
                                            ], children: "Invoice" }) }), _jsx("th", { style: { width: 140, padding: '12px 6px' }, children: "Date" }), _jsx("th", { style: { width: 140, padding: '12px 6px' }, children: "Status" }), _jsx("th", { style: { width: 240, padding: '12px 6px' }, children: "Customer" }), _jsx("th", { style: { width: 140, padding: '12px 6px' }, children: " " })] }) }), _jsx("tbody", { children: [...rows].sort(getComparator(order, 'id')).map((row) => (_jsxs("tr", { children: [_jsx("td", { style: { textAlign: 'center', width: 120 }, children: _jsx(Checkbox, { size: "sm", checked: selected.includes(row.id), color: selected.includes(row.id) ? 'primary' : undefined, onChange: (event) => {
                                                setSelected((ids) => event.target.checked
                                                    ? ids.concat(row.id)
                                                    : ids.filter((itemId) => itemId !== row.id));
                                            }, slotProps: { checkbox: { sx: { textAlign: 'left' } } }, sx: { verticalAlign: 'text-bottom' } }) }), _jsx("td", { children: _jsx(Typography, { level: "body-xs", children: row.id }) }), _jsx("td", { children: _jsx(Typography, { level: "body-xs", children: row.date }) }), _jsx("td", { children: _jsx(Chip, { variant: "soft", size: "sm", startDecorator: {
                                                Paid: _jsx(CheckRoundedIcon, {}),
                                                Refunded: _jsx(AutorenewRoundedIcon, {}),
                                                Cancelled: _jsx(BlockIcon, {}),
                                            }[row.status], color: {
                                                Paid: 'success',
                                                Refunded: 'neutral',
                                                Cancelled: 'danger',
                                            }[row.status], children: row.status }) }), _jsx("td", { children: _jsxs(Box, { sx: { display: 'flex', gap: 2, alignItems: 'center' }, children: [_jsx(Avatar, { size: "sm", children: row.customer.initial }), _jsxs("div", { children: [_jsx(Typography, { level: "body-xs", children: row.customer.name }), _jsx(Typography, { level: "body-xs", children: row.customer.email })] })] }) }), _jsx("td", { children: _jsxs(Box, { sx: { display: 'flex', gap: 2, alignItems: 'center' }, children: [_jsx(Link, { level: "body-xs", component: "button", children: "Download" }), _jsx(RowMenu, {})] }) })] }, row.id))) })] }) }), _jsxs(Box, { className: "Pagination-laptopUp", sx: {
                    pt: 2,
                    gap: 1,
                    [`& .${iconButtonClasses.root}`]: { borderRadius: '50%' },
                    display: {
                        xs: 'none',
                        md: 'flex',
                    },
                }, children: [_jsx(Button, { size: "sm", variant: "outlined", color: "neutral", startDecorator: _jsx(KeyboardArrowLeftIcon, {}), children: "Previous" }), _jsx(Box, { sx: { flex: 1 } }), ['1', '2', '3', '…', '8', '9', '10'].map((page) => (_jsx(IconButton, { size: "sm", variant: Number(page) ? 'outlined' : 'plain', color: "neutral", children: page }, page))), _jsx(Box, { sx: { flex: 1 } }), _jsx(Button, { size: "sm", variant: "outlined", color: "neutral", endDecorator: _jsx(KeyboardArrowRightIcon, {}), children: "Next" })] })] }));
}
