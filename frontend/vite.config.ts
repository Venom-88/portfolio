// D:\todo-app\frontend\vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";   // ← ДОЛЖЕН быть!

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
