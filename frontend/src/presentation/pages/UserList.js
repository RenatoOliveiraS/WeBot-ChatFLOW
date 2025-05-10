import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState, useCallback, useMemo } from 'react';
import { CssVarsProvider } from '@mui/joy/styles';
import CssBaseline from '@mui/joy/CssBaseline';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Breadcrumbs from '@mui/joy/Breadcrumbs';
import Link from '@mui/joy/Link';
import Typography from '@mui/joy/Typography';
import Sheet from '@mui/joy/Sheet';
import Table from '@mui/joy/Table';
import IconButton from '@mui/joy/IconButton';
import Modal from '@mui/joy/Modal';
import ModalDialog from '@mui/joy/ModalDialog';
import ModalClose from '@mui/joy/ModalClose';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Stack from '@mui/joy/Stack';
import Avatar from '@mui/joy/Avatar';
import Chip from '@mui/joy/Chip';
import SearchIcon from '@mui/icons-material/Search';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import BlockIcon from '@mui/icons-material/Block';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import ChevronRightRoundedIcon from '@mui/icons-material/ChevronRightRounded';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Header from '../../shared-theme/components/Header';
import Sidebar from './Sidebar';
import { ApiClient } from '../../infrastructure/api/ApiClient';
import { UserRepositoryImpl } from '../../infrastructure/repositories/UserRepositoryImpl';
import { ListUsers } from '../../core/use-cases/user/ListUsers';
import { CreateUser } from '../../core/use-cases/user/CreateUser';
import { UpdateUser } from '../../core/use-cases/user/UpdateUser';
import { DeleteUser } from '../../core/use-cases/user/DeleteUser';
const UserList = () => {
    const [users, setUsers] = useState([]);
    const [search, setSearch] = useState('');
    const [statusFilter, setStatusFilter] = useState('all');
    const [openDialog, setOpenDialog] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
    });
    const apiClient = useMemo(() => new ApiClient(), []);
    const userRepository = useMemo(() => new UserRepositoryImpl(apiClient), [apiClient]);
    const listUsersUseCase = useMemo(() => new ListUsers(userRepository), [userRepository]);
    const createUserUseCase = useMemo(() => new CreateUser(userRepository), [userRepository]);
    const updateUserUseCase = useMemo(() => new UpdateUser(userRepository), [userRepository]);
    const deleteUserUseCase = useMemo(() => new DeleteUser(userRepository), [userRepository]);
    const fetchUsers = useCallback(async () => {
        try {
            const data = await listUsersUseCase.execute();
            setUsers(data);
        }
        catch (error) {
            console.error('Error fetching users:', error);
        }
    }, [listUsersUseCase]);
    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);
    const handleOpenDialog = (user) => {
        if (user) {
            setSelectedUser(user);
            setFormData({
                name: user.name,
                email: user.email,
                password: '',
            });
        }
        else {
            setSelectedUser(null);
            setFormData({
                name: '',
                email: '',
                password: '',
            });
        }
        setOpenDialog(true);
    };
    const handleCloseDialog = () => {
        setOpenDialog(false);
        setSelectedUser(null);
        setFormData({
            name: '',
            email: '',
            password: '',
        });
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (selectedUser) {
                // Update
                const updateData = {
                    name: formData.name,
                    email: formData.email,
                    ...(formData.password ? { password: formData.password } : {}),
                };
                await updateUserUseCase.execute(selectedUser.id, updateData);
            }
            else {
                // Create
                const createData = {
                    name: formData.name,
                    email: formData.email,
                    password: formData.password,
                };
                await createUserUseCase.execute(createData);
            }
            handleCloseDialog();
            fetchUsers();
        }
        catch (error) {
            console.error('Error saving user:', error);
        }
    };
    const handleDelete = async (userId) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            try {
                await deleteUserUseCase.execute(userId);
                fetchUsers();
            }
            catch (error) {
                console.error('Error deleting user:', error);
            }
        }
    };
    const filteredUsers = users.filter((user) => {
        if (!user)
            return false;
        const name = user.name || '';
        const email = user.email || '';
        if (!name || !email)
            return false;
        const matchesSearch = name.toLowerCase().includes(search.toLowerCase()) ||
            email.toLowerCase().includes(search.toLowerCase());
        const matchesStatus = statusFilter === 'all' ||
            (statusFilter === 'active' && user.is_active) ||
            (statusFilter === 'inactive' && !user.is_active);
        return matchesSearch && matchesStatus;
    });
    return (_jsxs(CssVarsProvider, { disableTransitionOnChange: true, children: [_jsx(CssBaseline, {}), _jsxs(Box, { sx: { display: 'flex', minHeight: '100dvh' }, children: [_jsx(Header, {}), _jsx(Sidebar, {}), _jsxs(Box, { component: "main", className: "MainContent", sx: {
                            px: { xs: 2, md: 6 },
                            pt: {
                                xs: 'calc(12px + var(--Header-height))',
                                sm: 'calc(12px + var(--Header-height))',
                                md: 3,
                            },
                            pb: { xs: 2, sm: 2, md: 3 },
                            flex: 1,
                            display: 'flex',
                            flexDirection: 'column',
                            minWidth: 0,
                            height: '100dvh',
                            gap: 1,
                        }, children: [_jsx(Box, { sx: { display: 'flex', alignItems: 'center' }, children: _jsxs(Breadcrumbs, { size: "sm", "aria-label": "breadcrumbs", separator: _jsx(ChevronRightRoundedIcon, { fontSize: "small" }), sx: { pl: 0 }, children: [_jsx(Link, { underline: "none", color: "neutral", href: "#some-link", "aria-label": "Home", children: _jsx(HomeRoundedIcon, {}) }), _jsx(Link, { underline: "hover", color: "neutral", href: "#some-link", sx: { fontSize: 12, fontWeight: 500 }, children: "Dashboard" }), _jsx(Typography, { color: "primary", sx: { fontWeight: 500, fontSize: 12 }, children: "Users" })] }) }), _jsxs(Box, { sx: {
                                    display: 'flex',
                                    mb: 1,
                                    gap: 1,
                                    flexDirection: { xs: 'column', sm: 'row' },
                                    alignItems: { xs: 'start', sm: 'center' },
                                    flexWrap: 'wrap',
                                    justifyContent: 'space-between',
                                }, children: [_jsx(Typography, { level: "h2", component: "h1", children: "Users" }), _jsx(Button, { color: "primary", startDecorator: _jsx(AddIcon, {}), size: "sm", onClick: () => handleOpenDialog(), children: "Add User" })] }), _jsxs(Box, { sx: { display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }, children: [_jsxs(FormControl, { sx: { minWidth: 240 }, children: [_jsx(FormLabel, { children: "Search for user" }), _jsx(Input, { startDecorator: _jsx(SearchIcon, {}), placeholder: "Search", value: search, onChange: e => setSearch(e.target.value) })] }), _jsxs(FormControl, { sx: { minWidth: 180 }, children: [_jsx(FormLabel, { children: "Status" }), _jsxs(Select, { value: statusFilter, onChange: (_, value) => setStatusFilter(value), children: [_jsx(Option, { value: "all", children: "All" }), _jsx(Option, { value: "active", children: "Active" }), _jsx(Option, { value: "inactive", children: "Inactive" })] })] })] }), _jsx(Sheet, { children: _jsxs(Table, { children: [_jsx("thead", { children: _jsxs("tr", { children: [_jsx("th", { children: "ID" }), _jsx("th", { children: "Username" }), _jsx("th", { children: "Email" }), _jsx("th", { children: "Status" }), _jsx("th", { children: "Created At" }), _jsx("th", { children: "Actions" })] }) }), _jsx("tbody", { children: filteredUsers.map((user) => (_jsxs("tr", { children: [_jsx("td", { children: user.id }), _jsx("td", { children: _jsxs(Box, { sx: { display: 'flex', alignItems: 'center', gap: 1 }, children: [_jsx(Avatar, { size: "sm", children: user.name?.charAt(0).toUpperCase() || '' }), _jsxs(Box, { children: [_jsx(Typography, { level: "body-md", children: user.name || '' }), _jsx(Typography, { level: "body-xs", color: "neutral", children: user.email || '' })] })] }) }), _jsx("td", { children: user.email || '' }), _jsx("td", { children: user.is_active ? (_jsx(Chip, { color: "success", startDecorator: _jsx(CheckCircleIcon, { fontSize: "small" }), children: "Active" })) : (_jsx(Chip, { color: "danger", startDecorator: _jsx(BlockIcon, { fontSize: "small" }), children: "Inactive" })) }), _jsx("td", { children: new Date(user.created_at).toLocaleDateString() }), _jsxs("td", { children: [_jsx(IconButton, { size: "sm", variant: "plain", color: "primary", onClick: () => handleOpenDialog(user), children: _jsx(EditIcon, {}) }), _jsx(IconButton, { size: "sm", variant: "plain", color: "danger", onClick: () => handleDelete(user.id), children: _jsx(DeleteIcon, {}) })] })] }, user.id))) })] }) }), _jsx(Modal, { open: openDialog, onClose: handleCloseDialog, children: _jsxs(ModalDialog, { children: [_jsx(ModalClose, {}), _jsx(Typography, { level: "h4", children: selectedUser ? 'Edit User' : 'Add User' }), _jsx("form", { onSubmit: handleSubmit, children: _jsxs(Stack, { spacing: 2, children: [_jsxs(FormControl, { children: [_jsx(FormLabel, { children: "Username" }), _jsx(Input, { value: formData.name, onChange: (e) => setFormData({ ...formData, name: e.target.value }), required: true })] }), _jsxs(FormControl, { children: [_jsx(FormLabel, { children: "Email" }), _jsx(Input, { type: "email", value: formData.email, onChange: (e) => setFormData({ ...formData, email: e.target.value }), required: true })] }), _jsxs(FormControl, { children: [_jsx(FormLabel, { children: "Password" }), _jsx(Input, { type: "password", value: formData.password, onChange: (e) => setFormData({ ...formData, password: e.target.value }), required: !selectedUser })] }), _jsxs(Box, { sx: { display: 'flex', gap: 1, justifyContent: 'flex-end', mt: 2 }, children: [_jsx(Button, { variant: "plain", color: "neutral", onClick: handleCloseDialog, children: "Cancel" }), _jsx(Button, { type: "submit", children: selectedUser ? 'Update' : 'Create' })] })] }) })] }) })] })] })] }));
};
export default UserList;
