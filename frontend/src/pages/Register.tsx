import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Container,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import { register as apiRegister, login as apiLogin } from "../api/auth";
import { useAuth } from "../context/AuthContext";

/**
 * Страница регистрации.
 * После успешного создания пользователя сразу логинимся,
 * чтобы не заставлять пользователя вводить пароль повторно.
 */
export default function Register() {
  const { login } = useAuth();

  /* ---------- Состояние формы ---------- */
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  /* ---------- Сабмит ---------- */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== password2) {
      setError("Пароли не совпадают");
      return;
    }

    setLoading(true);
    try {
      // 1. Регистрируем
      await apiRegister(username, password);
      // 2. Автоматически входим
      const token = await apiLogin(username, password);
      login(token);
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Не удалось зарегистрироваться. Попробуйте ещё раз.";
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
          Регистрация
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

          <TextField
            label="Повторите пароль"
            type="password"
            fullWidth
            margin="normal"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            required
          />

          <Button
            type="submit"
            variant="contained"
            fullWidth
            disabled={loading}
            sx={{ mt: 2 }}
          >
            {loading ? "Создаём..." : "Зарегистрироваться"}
          </Button>
        </Box>

        <Typography variant="body2" sx={{ mt: 2 }}>
          Уже есть аккаунт? <a href="/login">Войти</a>
        </Typography>
      </Paper>
    </Container>
  );
}
