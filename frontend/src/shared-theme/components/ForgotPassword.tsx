import * as React from 'react';
import Button from '@mui/joy/Button';
import Modal from '@mui/joy/Modal';
import ModalDialog from '@mui/joy/ModalDialog';
import ModalClose from '@mui/joy/ModalClose';
import Typography from '@mui/joy/Typography';
import Input from '@mui/joy/Input';
import Stack from '@mui/joy/Stack';

interface ForgotPasswordProps {
  open: boolean;
  handleClose: () => void;
}

export default function ForgotPassword({ open, handleClose }: ForgotPasswordProps) {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    handleClose();
  };

  return (
    <Modal open={open} onClose={handleClose}>
      <ModalDialog
        component="form"
        onSubmit={handleSubmit}
        sx={{
          maxWidth: 500,
          width: '100%',
          p: 3,
        }}
      >
        <ModalClose />
        <Typography level="h4" component="h2" mb={2}>
          Reset password
        </Typography>
        <Stack spacing={2}>
          <Typography level="body-md">
            Enter your account&apos;s email address, and we&apos;ll send you a link to
            reset your password.
          </Typography>
          <Input
            required
            id="email"
            name="email"
            placeholder="Email address"
            type="email"
            fullWidth
          />
          <Stack direction="row" spacing={1} justifyContent="flex-end" mt={2}>
            <Button variant="plain" color="neutral" onClick={handleClose}>
              Cancel
            </Button>
            <Button type="submit">
              Continue
            </Button>
          </Stack>
        </Stack>
      </ModalDialog>
    </Modal>
  );
}
