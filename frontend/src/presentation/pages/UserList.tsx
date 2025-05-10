import React, { useEffect, useState } from 'react';
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
import { User as DomainUser, CreateUserDTO, UpdateUserDTO } from '../../core/domain/entities/User';

const UserList: React.FC = () => {
  const [users, setUsers] = useState<DomainUser[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState<DomainUser | null>(null);
  const [formData, setFormData] = useState<{
    name: string;
    email: string;
    password: string;
  }>({
    name: '',
    email: '',
    password: '',
  });
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');

  const apiClient = new ApiClient();
  const userRepository = new UserRepositoryImpl(apiClient);
  const listUsersUseCase = new ListUsers(userRepository);
  const createUserUseCase = new CreateUser(userRepository);
  const updateUserUseCase = new UpdateUser(userRepository);
  const deleteUserUseCase = new DeleteUser(userRepository);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const data = await listUsersUseCase.execute();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleOpenDialog = (user?: DomainUser) => {
    if (user) {
      setSelectedUser(user);
      setFormData({
        name: user.name,
        email: user.email,
        password: '',
      });
    } else {
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (selectedUser) {
        // Update
        const updateData: UpdateUserDTO = {
          name: formData.name,
          email: formData.email,
          ...(formData.password ? { password: formData.password } : {}),
        };
        await updateUserUseCase.execute(selectedUser.id, updateData);
      } else {
        // Create
        const createData: CreateUserDTO = {
          name: formData.name,
          email: formData.email,
          password: formData.password,
        };
        await createUserUseCase.execute(createData);
      }
      handleCloseDialog();
      fetchUsers();
    } catch (error) {
      console.error('Error saving user:', error);
    }
  };

  const handleDelete = async (userId: string) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await deleteUserUseCase.execute(userId);
        fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  const filteredUsers = users.filter((user) => {
    if (!user) return false;
    const name = user.name || '';
    const email = user.email || '';
    if (!name || !email) return false;
    const matchesSearch =
      name.toLowerCase().includes(search.toLowerCase()) ||
      email.toLowerCase().includes(search.toLowerCase());
    const matchesStatus =
      statusFilter === 'all' ||
      (statusFilter === 'active' && user.is_active) ||
      (statusFilter === 'inactive' && !user.is_active);
    return matchesSearch && matchesStatus;
  });

  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100dvh' }}>
        <Header />
        <Sidebar />
        <Box
          component="main"
          className="MainContent"
          sx={{
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
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Breadcrumbs
              size="sm"
              aria-label="breadcrumbs"
              separator={<ChevronRightRoundedIcon fontSize="small" />}
              sx={{ pl: 0 }}
            >
              <Link
                underline="none"
                color="neutral"
                href="#some-link"
                aria-label="Home"
              >
                <HomeRoundedIcon />
              </Link>
              <Link
                underline="hover"
                color="neutral"
                href="#some-link"
                sx={{ fontSize: 12, fontWeight: 500 }}
              >
                Dashboard
              </Link>
              <Typography color="primary" sx={{ fontWeight: 500, fontSize: 12 }}>
                Users
              </Typography>
            </Breadcrumbs>
          </Box>
          <Box
            sx={{
              display: 'flex',
              mb: 1,
              gap: 1,
              flexDirection: { xs: 'column', sm: 'row' },
              alignItems: { xs: 'start', sm: 'center' },
              flexWrap: 'wrap',
              justifyContent: 'space-between',
            }}
          >
            <Typography level="h2" component="h1">
              Users
            </Typography>
            <Button
              color="primary"
              startDecorator={<AddIcon />}
              size="sm"
              onClick={() => handleOpenDialog()}
            >
              Add User
            </Button>
          </Box>
          <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
            <FormControl sx={{ minWidth: 240 }}>
              <FormLabel>Search for user</FormLabel>
              <Input
                startDecorator={<SearchIcon />}
                placeholder="Search"
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </FormControl>
            <FormControl sx={{ minWidth: 180 }}>
              <FormLabel>Status</FormLabel>
              <Select
                value={statusFilter}
                onChange={(_, value) => setStatusFilter(value as any)}
              >
                <Option value="all">All</Option>
                <Option value="active">Active</Option>
                <Option value="inactive">Inactive</Option>
              </Select>
            </FormControl>
          </Box>
          <Sheet>
            <Table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Created At</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Avatar size="sm">
                          {user.name?.charAt(0).toUpperCase() || ''}
                        </Avatar>
                        <Box>
                          <Typography level="body-md">{user.name || ''}</Typography>
                          <Typography level="body-xs" color="neutral">{user.email || ''}</Typography>
                        </Box>
                      </Box>
                    </td>
                    <td>{user.email || ''}</td>
                    <td>
                      {user.is_active ? (
                        <Chip color="success" startDecorator={<CheckCircleIcon fontSize="small" />}>Active</Chip>
                      ) : (
                        <Chip color="danger" startDecorator={<BlockIcon fontSize="small" />}>Inactive</Chip>
                      )}
                    </td>
                    <td>{new Date(user.created_at).toLocaleDateString()}</td>
                    <td>
                      <IconButton
                        size="sm"
                        variant="plain"
                        color="primary"
                        onClick={() => handleOpenDialog(user)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        size="sm"
                        variant="plain"
                        color="danger"
                        onClick={() => handleDelete(user.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Sheet>

          <Modal open={openDialog} onClose={handleCloseDialog}>
            <ModalDialog>
              <ModalClose />
              <Typography level="h4">{selectedUser ? 'Edit User' : 'Add User'}</Typography>
              <form onSubmit={handleSubmit}>
                <Stack spacing={2}>
                  <FormControl>
                    <FormLabel>Username</FormLabel>
                    <Input
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Email</FormLabel>
                    <Input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      required
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Password</FormLabel>
                    <Input
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      required={!selectedUser}
                    />
                  </FormControl>
                  <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end', mt: 2 }}>
                    <Button
                      variant="plain"
                      color="neutral"
                      onClick={handleCloseDialog}
                    >
                      Cancel
                    </Button>
                    <Button type="submit">
                      {selectedUser ? 'Update' : 'Create'}
                    </Button>
                  </Box>
                </Stack>
              </form>
            </ModalDialog>
          </Modal>
        </Box>
      </Box>
    </CssVarsProvider>
  );
};

export default UserList; 