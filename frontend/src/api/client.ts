/**
 * Общий экземпляр axios для обращения к бекенду.
 * Базовый URL берётся из переменной окружения VITE_API_URL
 * (см. vite.config) или по умолчанию http://localhost:8000.
 *
 * Токен из localStorage автоматически подставляется
 * в заголовок Authorization: Bearer <token>.
 */

import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

/* ─────────────── Интерцептор: добавляем JWT ─────────────── */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

export default api;
