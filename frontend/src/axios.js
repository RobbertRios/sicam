/**
 * src/axios.js
 *
 * Instancia de axios configurada con:
 *  - baseURL apuntando al backend (relativo, funciona con el proxy de Vite)
 *  - Interceptor de request: agrega Authorization: Bearer <token> automáticamente
 *  - Interceptor de response: si llega 401, limpia sesión y fuerza re-login
 *
 * Uso en cualquier componente:
 *   import axios from '@/axios.js'
 *
 *   const res = await axios.get('/api/pacientes/')
 *   const res = await axios.post('/api/pacientes/', datos)
 */

import axios from "axios";

const instance = axios.create({
  baseURL: "/", // relativo → el proxy de Vite redirige /api/* al backend
  timeout: 30000, // 30 segundos
});

// ── Interceptor de REQUEST ──────────────────────────────────────────────────
// Agrega el token JWT a cada petición automáticamente
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// ── Interceptor de RESPONSE ─────────────────────────────────────────────────
// Si el servidor devuelve 401, el token expiró → limpiar sesión y recargar
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("doctor");
      window.location.reload();
    }

    return Promise.reject(error);
  },
);

export default instance;
