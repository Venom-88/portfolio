/**
 * Функции для регистрации, входа и выхода.
 *
 * login(...) отправляет form-data (`application/x-www-form-urlencoded`),  
 * как того требует энд-поинт FastAPI /users/login.
 *
 * register(...) — обычный JSON-POST на /users/register.
 */

import api from "./client";

/* ---------- Типы ответов бекенда ---------- */
interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function register(username: string, password: string): Promise<void> {
  await api.post("/users/register", { username, password });
}

/**
 * Авторизация пользователя.
 * Сохраняет токен в localStorage и возвращает его.
 */
export async function login(username: string, password: string): Promise<string> {
  /*   FastAPI ожидает x-www-form-urlencoded:
       username=<...>&password=<...>
  */
  const body = new URLSearchParams({ username, password });

  const { data } = await api.post<TokenResponse>(
    "/users/login",
    body,
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
  );

  localStorage.setItem("token", data.access_token);
  return data.access_token;
}

/**
 * Выход: достаточно удалить токен.
 */
export function logout(): void {
  localStorage.removeItem("token");
}
