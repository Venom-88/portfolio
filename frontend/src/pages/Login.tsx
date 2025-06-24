import { useState } from "react";
import {
  Button,
  Container,
  TextField,
  Typography,
  Alert,
  Box,
  Paper,
} from "@mui/material";
import { login as apiLogin } from "../api/auth";
import { useAuth } from "../context/AuthContext";

/**
 * Страница входа.
 * После успешной авторизации сохраняем токен через AuthContext.
 */
export default function Login() {
  const { login } = useAuth();

  /* ---------- Локальное состояние формы ---------- */
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  /* ---------- Сабмит ---------- */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const token = await apiLogin(username, password);
      login(token); // контекст сам переадресует на /
    } catch (err: any) {
      // AxiosError либо обычный Error
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Не удалось войти. Попробуйте ещё раз.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  /* ---------- UI ---------- */
  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Вход
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" noValidate onSubmit={handleSubmit}>
          <TextField
            label="Имя пользователя"
            fullWidth
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <TextField
            label="Пароль"
            type="password"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <Button
            type="submit"
            variant="contained"
            fullWidth
            disabled={loading}
            sx={{ mt: 2 }}
          >
            {loading ? "Входим..." : "Войти"}
          </Button>
        </Box>

        <Typography variant="body2" sx={{ mt: 2 }}>
          Нет аккаунта? <a href="/register">Регистрация</a>
        </Typography>
      </Paper>
    </Container>
  );
}
