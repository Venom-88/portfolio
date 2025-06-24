/**
 * CRUD-функции для работы с задачами.
 * Все запросы осуществляются через общий axios-клиент (`api`),
 * который уже вставляет JWT-токен в заголовки.
 */

import api from "./client";

/* ---------- Типы данных ---------- */
export interface Task {
  id: number;
  title: string;
  description?: string;
  is_done: boolean;
  created_at: string;          // ISO-дата от сервера
}

/* ---------- Запросы ---------- */

/**
 * Получить список задач.
 * @param status  "todo" | "done" | undefined (все)
 * @param order   пример: "created_at,-is_done"
 */
export async function getTasks(
  status?: "todo" | "done",
  order?: string,
): Promise<Task[]> {
  const params: Record<string, string> = {};
  if (status) params.status = status;
  if (order)  params.order  = order;

  const { data } = await api.get<Task[]>("/tasks", { params });
  return data;
}

/**
 * Создать задачу.
 */
export async function createTask(
  payload: Pick<Task, "title" | "description">,
): Promise<Task> {
  const { data } = await api.post<Task>("/tasks", payload);
  return data;
}

/**
 * Частично обновить задачу.
 */
export async function updateTask(
  id: number,
  payload: Partial<Pick<Task, "title" | "description" | "is_done">>,
): Promise<Task> {
  const { data } = await api.patch<Task>(`/tasks/${id}`, payload);
  return data;
}

/**
 * Удалить задачу.
 */
export async function deleteTask(id: number): Promise<void> {
  await api.delete(`/tasks/${id}`);
}
