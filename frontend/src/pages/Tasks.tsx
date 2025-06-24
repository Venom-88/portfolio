import { useEffect, useState } from "react";
import {
  AppBar,
  Box,
  Button,
  Container,
  IconButton,
  MenuItem,
  Select,
  Toolbar,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import LogoutIcon from "@mui/icons-material/Logout";
import { AnimatePresence, motion } from "framer-motion";

import {
  createTask,
  deleteTask,
  getTasks,
  Task,
  updateTask,
} from "../api/tasks";
import { useAuth } from "../context/AuthContext";
import TaskItem from "../components/TaskItem";
import TaskForm from "../components/TaskForm";

/**
 * Главная страница со списком задач.
 * Поддерживает:
 *   • Фильтр todo / done / all
 *   • Сортировку (created_at ASC/DESC, is_done)
 *   • CRUD через TaskForm (диалог)
 */
export default function TasksPage() {
  const { logout } = useAuth();

  /* ---------- Локальный state ---------- */
  const [tasks, setTasks] = useState<Task[]>([]);
  const [statusFilter, setStatusFilter] = useState<"" | "todo" | "done">("");
  const [order, setOrder] = useState<string>("-created_at"); // по умолчанию новые вверх
  const [openForm, setOpenForm] = useState<{
    mode: "create" | "edit";
    task?: Task;
  } | null>(null);

  /* ---------- Загрузить задачи ---------- */
  const loadTasks = async () => {
    const data = await getTasks(statusFilter || undefined, order);
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, order]);

  /* ---------- CRUD handlers ---------- */
  const handleCreate = async (payload: { title: string; description?: string }) => {
    await createTask(payload);
    setOpenForm(null);
    await loadTasks();
  };

  const handleUpdate = async (
    id: number,
    payload: Partial<Pick<Task, "title" | "description" | "is_done">>,
  ) => {
    await updateTask(id, payload);
    setOpenForm(null);
    await loadTasks();
  };

  const handleDelete = async (id: number) => {
    await deleteTask(id);
    await loadTasks();
  };

  /* ---------- UI ---------- */
  return (
    <>
      {/* ─────── Верхняя панель ─────── */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Список задач
          </Typography>

          {/* Фильтр */}
          <Select
            variant="outlined"
            size="small"
            sx={{ bgcolor: "background.paper", mr: 2 }}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as any)}
          >
            <MenuItem value="">Все</MenuItem>
            <MenuItem value="todo">Не выполненные</MenuItem>
            <MenuItem value="done">Выполненные</MenuItem>
          </Select>

          {/* Сортировка */}
          <Select
            variant="outlined"
            size="small"
            sx={{ bgcolor: "background.paper", mr: 2 }}
            value={order}
            onChange={(e) => setOrder(e.target.value)}
          >
            <MenuItem value="-created_at">Новые ⬆</MenuItem>
            <MenuItem value="created_at">Старые ⬆</MenuItem>
            <MenuItem value="is_done,-created_at">Статус, новые</MenuItem>
          </Select>

          {/* Добавить задачу */}
          <IconButton color="inherit" onClick={() => setOpenForm({ mode: "create" })}>
            <AddIcon />
          </IconButton>

          {/* Выход */}
          <IconButton color="inherit" onClick={logout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* ─────── Контент ─────── */}
      <Container maxWidth="md" sx={{ mt: 4 }}>
        {tasks.length === 0 ? (
          <Typography color="text.secondary" align="center" sx={{ mt: 8 }}>
            Задач пока нет
          </Typography>
        ) : (
          <Box>
            <AnimatePresence>
              {tasks.map((t) => (
                <motion.div
                  key={t.id}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.2 }}
                  style={{ marginBottom: "12px" }}
                >
                  <TaskItem
                    task={t}
                    onEdit={() => setOpenForm({ mode: "edit", task: t })}
                    onDelete={() => handleDelete(t.id)}
                    onToggle={() => handleUpdate(t.id, { is_done: !t.is_done })}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </Box>
        )}
      </Container>

      {/* ─────── Диалог создания/редактирования ─────── */}
      {openForm && (
        <TaskForm
          open
          mode={openForm.mode}
          task={openForm.task}
          onClose={() => setOpenForm(null)}
          onSubmit={
            openForm.mode === "create"
              ? handleCreate
              : (payload) => handleUpdate(openForm.task!.id, payload)
          }
        />
      )}
    </>
  );
}
