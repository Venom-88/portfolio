import {
  Box,
  Checkbox,
  IconButton,
  Paper,
  Tooltip,
  Typography,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

/* ---------- Типы ---------- */
export interface TaskItemProps {
  task: {
    id: number;
    title: string;
    description?: string;
    is_done: boolean;
    created_at: string;
  };
  onEdit: () => void;
  onDelete: () => void;
  onToggle: () => void;
}

/**
 * Одно «карточка-строка» задачи.
 *  • Checkbox помечает выполненной / невыполненной
 *  • Иконки редактирования и удаления
 */
export default function TaskItem({
  task,
  onEdit,
  onDelete,
  onToggle,
}: TaskItemProps) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2, display: "flex", alignItems: "flex-start" }}
    >
      {/* ───── Checkbox ───── */}
      <Checkbox
        checked={task.is_done}
        onChange={onToggle}
        sx={{ mr: 1, mt: 0.5 }}
      />

      {/* ───── Основной текст ───── */}
      <Box sx={{ flexGrow: 1 }}>
        <Typography
          variant="subtitle1"
          sx={{ textDecoration: task.is_done ? "line-through" : "none" }}
        >
          {task.title}
        </Typography>

        {task.description && (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ whiteSpace: "pre-wrap" }}
          >
            {task.description}
          </Typography>
        )}

        <Typography variant="caption" color="text.secondary">
          {new Date(task.created_at).toLocaleString()}
        </Typography>
      </Box>

      {/* ───── Действия ───── */}
      <Box sx={{ ml: 1, mt: -1 }}>
        <Tooltip title="Редактировать">
          <IconButton size="small" onClick={onEdit}>
            <EditIcon fontSize="small" />
          </IconButton>
        </Tooltip>

        <Tooltip title="Удалить">
          <IconButton size="small" onClick={onDelete}>
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
    </Paper>
  );
}
