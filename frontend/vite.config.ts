import UnoCSS from "unocss/vite";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react(), UnoCSS()],
  server: {
    proxy: {
      "/congers/api": {
        target: "http://127.0.0.1:5000/",
        changeOrigin: true,
      },
    },
    cors: true,
  },
  build: {
    manifest: true,
    outDir: "../src/congers/static",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/main.tsx",
    },
  },
});
