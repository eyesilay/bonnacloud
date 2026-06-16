/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Design Tokens (Admin Panelden değişecek dinamik renkler)
        theme: {
          primary: "var(--color-primary, #1E3A8A)",     // Varsayılan: Bonna Laciverti
          secondary: "var(--color-secondary, #F8FAFC)", // Varsayılan: Açık Gri
          accent: "var(--color-accent, #F59E0B)",       // Varsayılan: Vurgu Sarısı
        }
      }
    },
  },
  plugins: [],
}