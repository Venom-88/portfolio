import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { useNavigate } from "react-router-dom";

/* ---------- Тип интерфейса контекста ---------- */
interface AuthCtx {
  isAuth: boolean;
  login: (token: string) => void;
  logout: () => void;
}

/* ---------- Создаём сам контекст ---------- */
const AuthContext = createContext<AuthCtx>({
  isAuth: false,
  login: () => {},
  logout: () => {},
});

/* ---------- Удобный хук ---------- */
export const useAuth = () => useContext(AuthContext);

/* ------------------------------------------------------------------------ */
/*  Провайдер. Размещаем выше всех роутов (обычно в App.tsx).               */
/*  Сохраняем токен в localStorage, чтобы после перезагрузки оставаться     */
/*  авторизованным.                                                         */
/* ------------------------------------------------------------------------ */
export default function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuth, setIsAuth] = useState<boolean>(!!localStorage.getItem("token"));
  const navigate = useNavigate();

  /* ---------- Методы ---------- */
  const login = (token: string) => {
    localStorage.setItem("token", token);
    setIsAuth(true);
    navigate("/");        // после логина на главную страницу
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsAuth(false);
    navigate("/login");
  };

  /* ---------- Проверка токена при монтировании (опционально) ---------- */
  useEffect(() => {
    // Здесь можно проверять срок действия токена,
    // делать ping к /tasks, и если 401 — вызвать logout().
  }, []);

  /* ---------- Отдаём потомкам ---------- */
  return (
    <AuthContext.Provider value={{ isAuth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
