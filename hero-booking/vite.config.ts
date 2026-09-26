import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { viteSingleFile } from "vite-plugin-singlefile";

// SINGLEFILE=1 genera un solo index.html con todo inline (para publicarlo como Artifact).
export default defineConfig({
  plugins: [react(), tailwindcss(), ...(process.env.SINGLEFILE ? [viteSingleFile()] : [])],
  build: { assetsInlineLimit: process.env.SINGLEFILE ? 100_000_000 : 4096 },
});
