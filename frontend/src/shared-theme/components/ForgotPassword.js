import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Button from '@mui/joy/Button';
import Modal from '@mui/joy/Modal';
import ModalDialog from '@mui/joy/ModalDialog';
import ModalClose from '@mui/joy/ModalClose';
import Typography from '@mui/joy/Typography';
import Input from '@mui/joy/Input';
import Stack from '@mui/joy/Stack';
export default function ForgotPassword({ open, handleClose }) {
    const handleSubmit = (event) => {
        event.preventDefault();
        handleClose();
    };
    return (_jsx(Modal, { open: open, onClose: handleClose, children: _jsxs(ModalDialog, { component: "form", onSubmit: handleSubmit, sx: {
                maxWidth: 500,
                width: '100%',
                p: 3,
            }, children: [_jsx(ModalClose, {}), _jsx(Typography, { level: "h4", component: "h2", mb: 2, children: "Reset password" }), _jsxs(Stack, { spacing: 2, children: [_jsx(Typography, { level: "body-md", children: "Enter your account's email address, and we'll send you a link to reset your password." }), _jsx(Input, { required: true, id: "email", name: "email", placeholder: "Email address", type: "email", fullWidth: true }), _jsxs(Stack, { direction: "row", spacing: 1, justifyContent: "flex-end", mt: 2, children: [_jsx(Button, { variant: "plain", color: "neutral", onClick: handleClose, children: "Cancel" }), _jsx(Button, { type: "submit", children: "Continue" })] })] })] }) }));
}
