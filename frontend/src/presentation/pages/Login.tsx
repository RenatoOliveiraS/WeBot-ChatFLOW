import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuthContext } from '../contexts/AuthContext';
import { LoginCredentials } from '../../core/domain/entities/User';
import Alert from '@mui/joy/Alert';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Checkbox from '@mui/joy/Checkbox';
import CssBaseline from '@mui/joy/CssBaseline';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Link from '@mui/joy/Link';
import Typography from '@mui/joy/Typography';
import Stack from '@mui/joy/Stack';
import Card from '@mui/joy/Card';
import { styled } from '@mui/joy/styles';
import ForgotPassword from '../../shared-theme/components/ForgotPassword';
import AppTheme from '../../shared-theme/AppTheme';
import ColorSchemeToggle from '../../shared-theme/components/ColorSchemeToggle';
import LanguageSelect from '../../shared-theme/LanguageSelect';
import { LogoIcon } from '../../shared-theme/components/CustomIcons';

const SignInContainer = styled(Stack)(({ theme }) => ({
  height: 'calc((1 - var(--template-frame-height, 0)) * 100dvh)',
  minHeight: '100%',
  padding: theme.spacing(2),
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(4),
  },
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  '&::before': {
    content: '""',
    display: 'block',
    position: 'absolute',
    zIndex: -1,
    inset: 0,
    backgroundImage:
      'radial-gradient(ellipse at 50% 50%, hsl(210, 100%, 97%), hsl(0, 0%, 100%))',
    backgroundRepeat: 'no-repeat',
    ...theme.applyStyles('dark', {
      backgroundImage:
        'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
    }),
  },
}));

export default function SignIn(props: { disableCustomTheme?: boolean }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { login, error: loginError, loading } = useAuthContext();
  const [emailError, setEmailError] = React.useState(false);
  const [emailErrorMessage, setEmailErrorMessage] = React.useState('');
  const [passwordError, setPasswordError] = React.useState(false);
  const [passwordErrorMessage, setPasswordErrorMessage] = React.useState('');
  const [open, setOpen] = React.useState(false);
  const [rememberMe, setRememberMe] = React.useState(() => {
    const saved = localStorage.getItem('rememberMe');
    return saved ? JSON.parse(saved) : false;
  });
  const [email, setEmail] = React.useState(() => {
    return rememberMe ? localStorage.getItem('savedEmail') || '' : '';
  });
  const [password, setPassword] = React.useState('');

  const handleRememberMeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const isChecked = event.target.checked;
    setRememberMe(isChecked);
    localStorage.setItem('rememberMe', JSON.stringify(isChecked));
    
    if (!isChecked) {
      localStorage.removeItem('savedEmail');
    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    const credentials: LoginCredentials = {
      email,
      password,
    };

    if (rememberMe) {
      localStorage.setItem('savedEmail', email);
    }

    try {
      await login(credentials);
      navigate('/dashboard');
    } catch (err) {
      // O erro já é tratado pelo hook useAuth
    }
  };

  const validateInputs = () => {
    let isValid = true;

    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      setEmailError(true);
      setEmailErrorMessage(t('login.emailError'));
      isValid = false;
    } else {
      setEmailError(false);
      setEmailErrorMessage('');
    }

    if (!password || password.length < 6) {
      setPasswordError(true);
      setPasswordErrorMessage(t('login.passwordError'));
      isValid = false;
    } else {
      setPasswordError(false);
      setPasswordErrorMessage('');
    }

    return isValid;
  };

  return (
    <AppTheme {...props}>
      <CssBaseline />
      <SignInContainer>
        <Box sx={{ position: 'fixed', top: '1rem', right: '1rem', display: 'flex', alignItems: 'center', gap: 2 }}>
          <ColorSchemeToggle />
          <LanguageSelect />
        </Box>
        <Card 
          variant="outlined" 
          sx={{ 
            width: '100%', 
            maxWidth: '450px',
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', width: '100%' }}>
            <LogoIcon />
          </Box>
          <Typography
            level="h1"
            sx={{ width: '100%', fontSize: 'clamp(2rem, 10vw, 2.15rem)' }}
          >
            {t('login.title')}
          </Typography>
          {loginError && (
            <Alert color="danger" sx={{ width: '100%', mt: 2 }}>
              {loginError}
            </Alert>
          )}
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              gap: 2,
            }}
          >
            <FormControl>
              <FormLabel htmlFor="email">{t('login.email')}</FormLabel>
              <Input
                error={emailError}
                id="email"
                type="email"
                name="email"
                placeholder={t('login.emailPlaceholder')}
                autoComplete="email"
                required
                fullWidth
                color={emailError ? 'danger' : 'neutral'}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {emailErrorMessage && (
                <Typography level="body-sm" color="danger">
                  {emailErrorMessage}
                </Typography>
              )}
            </FormControl>
            <FormControl>
              <FormLabel htmlFor="password">{t('login.password')}</FormLabel>
              <Input
                error={passwordError}
                name="password"
                placeholder={t('login.passwordPlaceholder')}
                type="password"
                id="password"
                autoComplete="current-password"
                required
                fullWidth
                color={passwordError ? 'danger' : 'neutral'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              {passwordErrorMessage && (
                <Typography level="body-sm" color="danger">
                  {passwordErrorMessage}
                </Typography>
              )}
            </FormControl>
            <Checkbox
              label={t('login.rememberMe')}
              size="sm"
              checked={rememberMe}
              onChange={handleRememberMeChange}
            />
            <ForgotPassword open={open} handleClose={handleClose} />
            <Button
              type="submit"
              fullWidth
              variant="solid"
              onClick={validateInputs}
              loading={loading}
            >
              {loading ? t('login.loading') : t('login.signIn')}
            </Button>
            <Link
              component="button"
              type="button"
              onClick={handleClickOpen}
              level="body-sm"
              sx={{ alignSelf: 'center' }}
            >
              {t('login.forgotPassword')}
            </Link>
          </Box>
        </Card>
      </SignInContainer>
    </AppTheme>
  );
}