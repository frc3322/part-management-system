import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";
import handlebars from "vite-plugin-handlebars";

export default defineConfig({
    server: {
        port: 3000,
        open: false,
    },
    plugins: [
        tailwindcss(),
        handlebars({
            partialDirectory: [path.resolve(__dirname, "./src/html")],
        }),
    ],
});
