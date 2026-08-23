<template>
  <div class="login-root">
    <!-- Panel izquierdo: visual con imágenes microscópicas -->
    <div class="login-left">
      <!-- Slides de imágenes microscópicas -->
      <div class="micro-slides">
        <!-- Slide 0: gradiente puro (estado base del original) -->
        <div class="slide slide-gradient" :class="{ active: currentSlide === 0 }"></div>
        <!-- Slide 1: muestra de saliva -->
        <div
          class="slide slide-saliva"
          :class="{ active: currentSlide === 1 }"
          :style="{ backgroundImage: `url(${imgSaliva})` }"
        ></div>
        <!-- Slide 2: muestra de sangre  -->
        <div
          class="slide slide-sangre"
          :class="{ active: currentSlide === 2 }"
          :style="{ backgroundImage: `url(${imgSangre})` }"
        ></div>
      </div>

      <!-- Overlay adaptable: más ligero en sangre para que sea visible -->
      <div class="color-overlay" :class="'overlay-slide-' + currentSlide"></div>

      <!-- Etiqueta de tipo de muestra (aparece en slides 1 y 2) -->
      <transition name="label-fade">
        <div v-if="currentSlide > 0" class="sample-label">
          <span class="sample-dot" :class="currentSlide === 1 ? 'dot-saliva' : 'dot-sangre'"></span>
          {{ currentSlide === 1 ? "Muestra de saliva" : "Muestra de sangre" }}
        </div>
      </transition>

      <!-- Indicadores de slide -->
      <div class="slide-dots">
        <button
          v-for="i in 3"
          :key="i"
          class="slide-dot"
          :class="{ active: currentSlide === i - 1, paused: isPaused && currentSlide === i - 1 }"
          @click="goToSlide(i - 1)"
        ></button>
      </div>

      <div class="left-content">
        <div class="brand">
          <div class="brand-logo">
            <svg viewBox="0 0 40 40" fill="none">
              <circle
                cx="20"
                cy="20"
                r="18"
                stroke="white"
                stroke-width="1.5"
                stroke-dasharray="4 2"
                opacity="0.4"
              />
              <circle cx="20" cy="20" r="10" stroke="white" stroke-width="1.5" opacity="0.7" />
              <circle cx="20" cy="20" r="3.5" fill="white" />
              <circle cx="20" cy="9" r="2" fill="white" opacity="0.6" />
              <circle cx="29" cy="26" r="2" fill="white" opacity="0.6" />
              <circle cx="11" cy="26" r="2" fill="white" opacity="0.6" />
            </svg>
          </div>
          <span class="brand-name">SICAM</span>
        </div>

        <div class="left-tagline">
          <h1>Sistema Inteligente de Conteo y Análisis de Micronúcleos</h1>
          <p>Análisis celular</p>
        </div>

        <!-- Partículas decorativas -->
        <div class="particles">
          <span v-for="n in 12" :key="n" class="particle" :style="particleStyle(n)"></span>
        </div>
      </div>
    </div>

    <!-- Panel derecho: formulario -->
    <div class="login-right">
      <div class="form-container">
        <div class="form-header">
          <div class="form-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </div>
          <h2>Acceso médico</h2>
          <p>Ingresa con tus credenciales institucionales</p>
        </div>

        <transition name="alert-slide">
          <div v-if="errorMsg" class="error-alert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {{ errorMsg }}
          </div>
        </transition>

        <div class="form-body">
          <div
            class="field-group"
            :class="{ focused: focusedField === 'email', filled: form.email }"
          >
            <label class="field-label">Correo electrónico</label>
            <div class="field-input-wrap">
              <svg
                class="field-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path
                  d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                />
                <polyline points="22,6 12,13 2,6" />
              </svg>
              <input
                v-model="form.email"
                type="email"
                class="field-input"
                placeholder="doctor@hospital.mx"
                autocomplete="email"
                @focus="focusedField = 'email'"
                @blur="focusedField = null"
                @keyup.enter="handleLogin"
              />
            </div>
          </div>

          <div
            class="field-group"
            :class="{ focused: focusedField === 'password', filled: form.password }"
          >
            <label class="field-label">Contraseña</label>
            <div class="field-input-wrap">
              <svg
                class="field-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="field-input"
                placeholder="••••••••"
                autocomplete="current-password"
                @focus="focusedField = 'password'"
                @blur="focusedField = null"
                @keyup.enter="handleLogin"
              />
              <button
                class="toggle-pw"
                @click="showPassword = !showPassword"
                tabindex="-1"
                type="button"
              >
                <svg
                  v-if="!showPassword"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path
                    d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
                  />
                  <line x1="1" y1="1" x2="23" y2="23" />
                </svg>
              </button>
            </div>
          </div>

          <button
            class="btn-login"
            :class="{ loading: isLoading }"
            :disabled="isLoading || !form.email || !form.password"
            @click="handleLogin"
          >
            <svg
              v-if="isLoading"
              class="spinner"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <path
                d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"
              />
            </svg>
            <svg
              v-else
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
              <polyline points="10 17 15 12 10 7" />
              <line x1="15" y1="12" x2="3" y2="12" />
            </svg>
            {{ isLoading ? "Verificando…" : "Iniciar sesión" }}
          </button>
        </div>

        <p class="form-footer">
          ¿Problemas para acceder?
          <a href="mailto:admin@sicam.mx">Contacta al administrador</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

// ── Imágenes de muestras ─────────────────────────────────────────
// Para cambiar las imágenes, reemplaza los archivos en src/assets/:
//   src/assets/muestra-saliva.jpg
//   src/assets/muestra-sangre.jpeg
import imgSaliva from "@/assets/muestra-saliva.jpg";
import imgSangre from "@/assets/muestra-sangre.jpeg";

const emit = defineEmits(["login-success"]);

const form = ref({ email: "", password: "" });
const isLoading = ref(false);
const errorMsg = ref("");
const showPassword = ref(false);
const focusedField = ref(null);

// ── Slideshow ───────────────────────────────────────────────
// 0 = gradiente  1 = saliva  2 = sangre  → repite
const currentSlide = ref(0);
let slideTimer = null;
const SLIDE_DURATION = 5000; // ms por slide

const isPaused = ref(false);
let pauseTimeout = null;

function goToSlide(n) {
  currentSlide.value = n;
  isPaused.value = true;
  if (slideTimer) clearInterval(slideTimer);
  if (pauseTimeout) clearTimeout(pauseTimeout);
  pauseTimeout = setTimeout(() => {
    isPaused.value = false;
    slideTimer = setInterval(nextSlide, SLIDE_DURATION);
  }, 10000);
}

function nextSlide() {
  currentSlide.value = (currentSlide.value + 1) % 3;
}

onMounted(() => {
  slideTimer = setInterval(nextSlide, SLIDE_DURATION);
});

onUnmounted(() => {
  if (slideTimer) clearInterval(slideTimer);
  if (pauseTimeout) clearTimeout(pauseTimeout);
});

// ── Login ───────────────────────────────────────────────────
async function handleLogin() {
  if (!form.value.email || !form.value.password) return;
  errorMsg.value = "";
  isLoading.value = true;

  try {
    const res = await fetch("/api/auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: form.value.email.trim().toLowerCase(),
        password: form.value.password,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      errorMsg.value =
        data?.non_field_errors?.[0] ||
        data?.detail ||
        data?.email?.[0] ||
        "Credenciales inválidas. Intenta de nuevo.";
      return;
    }

    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    localStorage.setItem("doctor", JSON.stringify(data.doctor));

    emit("login-success", data.doctor);
  } catch {
    errorMsg.value = "Error de conexión. Verifica el servidor.";
  } finally {
    isLoading.value = false;
  }
}

// ── Partículas ──────────────────────────────────────────────
function particleStyle(n) {
  const positions = [
    { top: "10%", left: "15%", size: "6px", delay: "0s", dur: "4s" },
    { top: "25%", left: "80%", size: "4px", delay: "0.5s", dur: "5s" },
    { top: "60%", left: "10%", size: "8px", delay: "1s", dur: "3.5s" },
    { top: "75%", left: "70%", size: "5px", delay: "1.5s", dur: "4.5s" },
    { top: "40%", left: "50%", size: "3px", delay: "0.2s", dur: "6s" },
    { top: "85%", left: "30%", size: "6px", delay: "0.8s", dur: "3s" },
    { top: "15%", left: "60%", size: "4px", delay: "2s", dur: "5s" },
    { top: "50%", left: "88%", size: "7px", delay: "0.3s", dur: "4s" },
    { top: "30%", left: "25%", size: "3px", delay: "1.2s", dur: "5.5s" },
    { top: "70%", left: "55%", size: "5px", delay: "0.7s", dur: "3.8s" },
    { top: "90%", left: "85%", size: "4px", delay: "1.8s", dur: "4.2s" },
    { top: "5%", left: "40%", size: "6px", delay: "0.4s", dur: "4.8s" },
  ];
  const p = positions[(n - 1) % positions.length];
  return {
    top: p.top,
    left: p.left,
    width: p.size,
    height: p.size,
    animationDelay: p.delay,
    animationDuration: p.dur,
  };
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap");

/* ── Root ──────────────────────────────────────────────────── */
.login-root {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  font-family: "DM Sans", sans-serif;
}

/* ── Panel izquierdo ───────────────────────────────────────── */
.login-left {
  flex: 1.1;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── Slides de imágenes ─────────────────────────────────────── */
.micro-slides {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.slide {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 1.4s ease-in-out;
  animation: ken-burns 14s ease-in-out infinite alternate;
}

.slide.active {
  opacity: 1;
}

/* Slide 0: gradiente puro */
.slide-gradient {
  background: linear-gradient(145deg, #4f46e5 0%, #667eea 45%, #764ba2 100%);
  animation: none;
}

/* Slide 1: saliva — background-image se aplica via :style en el template */
.slide-saliva {
  background-size: cover;
  background-position: center;
  animation-delay: 0s;
}

/* Slide 2: sangre — background-image se aplica via :style en el template */
.slide-sangre {
  background-size: cover;
  background-position: center;
  animation-delay: -7s;
}

@keyframes ken-burns {
  from {
    transform: scale(1) translate(0, 0);
  }
  to {
    transform: scale(1.08) translate(-1%, -1%);
  }
}

/* ── Overlay de color de marca ─────────────────────────────── */
.color-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  transition: background-image 1.4s ease-in-out;
  background-image:
    radial-gradient(circle, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(
      145deg,
      rgba(79, 70, 229, 0.38) 0%,
      rgba(102, 126, 234, 0.28) 45%,
      rgba(118, 75, 162, 0.35) 100%
    );
  background-size:
    28px 28px,
    100% 100%;
  pointer-events: none;
}

.color-overlay.overlay-slide-0 {
  background-image:
    radial-gradient(circle, rgba(255, 255, 255, 0.08) 1px, transparent 1px),
    linear-gradient(
      145deg,
      rgba(79, 70, 229, 0) 0%,
      rgba(102, 126, 234, 0) 45%,
      rgba(118, 75, 162, 0) 100%
    );
  background-size:
    28px 28px,
    100% 100%;
}

.color-overlay.overlay-slide-1 {
  background-image:
    radial-gradient(circle, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(
      145deg,
      rgba(79, 70, 229, 0.42) 0%,
      rgba(102, 126, 234, 0.32) 45%,
      rgba(118, 75, 162, 0.38) 100%
    );
  background-size:
    28px 28px,
    100% 100%;
}

.color-overlay.overlay-slide-2 {
  background-image:
    radial-gradient(circle, rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(
      145deg,
      rgba(79, 70, 229, 0.18) 0%,
      rgba(102, 126, 234, 0.12) 45%,
      rgba(118, 75, 162, 0.15) 100%
    );
  background-size:
    28px 28px,
    100% 100%;
}

/* Orbe de fondo */
.login-left::after {
  content: "";
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.07) 0%, transparent 70%);
  bottom: -150px;
  right: -150px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 2;
}

/* ── Etiqueta de tipo de muestra ────────────────────────────── */
.sample-label {
  position: absolute;
  bottom: 80px;
  left: 56px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 100px;
  padding: 6px 16px 6px 10px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.92);
  font-weight: 500;
  letter-spacing: 0.3px;
}

.sample-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-saliva {
  background: rgba(200, 220, 255, 0.9);
}
.dot-sangre {
  background: rgba(255, 160, 160, 0.9);
}

.label-fade-enter-active,
.label-fade-leave-active {
  transition: all 0.4s ease;
}
.label-fade-enter-from,
.label-fade-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

/* ── Indicadores de slide ────────────────────────────────────── */
.slide-dots {
  position: absolute;
  bottom: 52px;
  left: 56px;
  z-index: 10;
  display: flex;
  gap: 8px;
}

.slide-dot {
  width: 28px;
  height: 3px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.3);
  border: none;
  cursor: pointer;
  padding: 0;
  transition: all 0.3s ease;
}

.slide-dot.active {
  background: rgba(255, 255, 255, 0.9);
  width: 40px;
}
.slide-dot.paused {
  background: rgba(255, 255, 255, 0.55);
  outline: 2px solid rgba(255, 255, 255, 0.7);
  outline-offset: 2px;
}

/* ── Contenido izquierdo ──────────────────────────────────── */
.left-content {
  position: relative;
  z-index: 5;
  padding: 60px 56px;
  width: 100%;
  max-width: 520px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 64px;
}
.brand-logo svg {
  width: 40px;
  height: 40px;
}
.brand-name {
  font-family: "DM Serif Display", serif;
  font-size: 28px;
  color: white;
  letter-spacing: 2px;
}

.left-tagline h1 {
  font-family: "DM Serif Display", serif;
  font-size: 38px;
  line-height: 1.2;
  color: white;
  margin: 0 0 16px;
  font-weight: 400;
}
.left-tagline p {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.7;
  margin: 0;
  max-width: 360px;
}

/* ── Partículas ─────────────────────────────────────────────── */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 3;
}
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  animation: float-particle linear infinite;
}
@keyframes float-particle {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-20px) scale(1.2);
    opacity: 0.7;
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 0.4;
  }
}

/* ── Panel derecho ─────────────────────────────────────────── */
.login-right {
  flex: 0.9;
  background: #f7f8fc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.form-container {
  width: 100%;
  max-width: 400px;
  animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ── Form header ───────────────────────────────────────────── */
.form-header {
  text-align: center;
  margin-bottom: 32px;
}
.form-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}
.form-icon svg {
  width: 24px;
  height: 24px;
  stroke: #667eea;
}
.form-header h2 {
  font-family: "DM Serif Display", serif;
  font-size: 26px;
  font-weight: 400;
  color: #1a202c;
  margin: 0 0 6px;
}
.form-header p {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
}

/* ── Error ─────────────────────────────────────────────────── */
.error-alert {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-radius: 10px;
  padding: 11px 14px;
  font-size: 13px;
  color: #be123c;
  margin-bottom: 20px;
}
.error-alert svg {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

.alert-slide-enter-active {
  transition: all 0.25s ease;
}
.alert-slide-leave-active {
  transition: all 0.2s ease;
}
.alert-slide-enter-from,
.alert-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ── Campos ────────────────────────────────────────────────── */
.form-body {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: #4b5563;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.field-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 13px;
  width: 16px;
  height: 16px;
  stroke: #9ca3af;
  flex-shrink: 0;
  transition: stroke 0.2s;
  pointer-events: none;
}
.field-group.focused .field-icon {
  stroke: #667eea;
}

.field-input {
  width: 100%;
  padding: 12px 40px 12px 40px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-family: "DM Sans", sans-serif;
  color: #1a202c;
  background: white;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}
.field-input::placeholder {
  color: #d1d5db;
}
.field-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.12);
}

.toggle-pw {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  color: #9ca3af;
  transition: color 0.2s;
  display: flex;
  align-items: center;
}
.toggle-pw:hover {
  color: #667eea;
}
.toggle-pw svg {
  width: 16px;
  height: 16px;
}

/* ── Botón login ───────────────────────────────────────────── */
.btn-login {
  width: 100%;
  padding: 13px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  font-family: "DM Sans", sans-serif;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.25s ease;
  margin-top: 8px;
  letter-spacing: 0.2px;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.35);
}
.btn-login:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 22px rgba(102, 126, 234, 0.45);
}
.btn-login:active:not(:disabled) {
  transform: translateY(0);
}
.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}
.btn-login svg {
  width: 18px;
  height: 18px;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.spinner {
  animation: spin 0.7s linear infinite;
}

/* ── Form footer ───────────────────────────────────────────── */
.form-footer {
  text-align: center;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 24px;
}
.form-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}
.form-footer a:hover {
  text-decoration: underline;
}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 768px) {
  .login-root {
    flex-direction: column;
  }
  .login-left {
    flex: 0;
    min-height: 220px;
  }
  .left-content {
    padding: 24px;
  }
  .brand {
    margin-bottom: 16px;
  }
  .left-tagline h1 {
    font-size: 24px;
  }
  .left-tagline p {
    display: none;
  }
  .sample-label,
  .slide-dots {
    left: 24px;
  }
  .login-right {
    flex: 1;
    padding: 32px 24px;
  }
}
</style>
