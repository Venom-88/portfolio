import { useEffect, useState } from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
} from "@mui/material";

/* ---------- Типы пропсов ---------- */
interface TaskFormProps {
  open: boolean;
  mode: "create" | "edit";
  task?: {
    title: string;
    description?: string;
  };
  onClose: () => void;
  onSubmit: (payload: { title: string; description?: string }) => void;
}

/**
 * Диалоговое окно для создания или редактирования задачи.
 */
export default function TaskForm({
  open,
  mode,
  task,
  onClose,
  onSubmit,
}: TaskFormProps) {
  /* ---------- Локальное состояние формы ---------- */
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  /* ---------- Заполнить поля при открытии в режиме edit ---------- */
  useEffect(() => {
    if (mode === "edit" && task) {
      setTitle(task.title);
      setDescription(task.description ?? "");
    } else {
      setTitle("");
      setDescription("");
    }
  }, [mode, task]);

  /* ---------- Сабмит ---------- */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return; // простая валидация
    onSubmit({ title: title.trim(), description: description.trim() || undefined });
  };

  /* ---------- UI ---------- */
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{mode === "create" ? "Новая задача" : "Редактировать задачу"}</DialogTitle>

      <form onSubmit={handleSubmit}>
        <DialogContent dividers>
          <TextField
            label="Заголовок"
            fullWidth
            required
            margin="normal"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <TextField
            label="Описание"
            fullWidth
            multiline
            minRows={3}
            margin="normal"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>Отмена</Button>
          <Button type="submit" variant="contained">
            {mode === "create" ? "Добавить" : "Сохранить"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
