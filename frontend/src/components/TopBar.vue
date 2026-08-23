<template>
  <nav class="topbar">
    <!-- IZQUIERDA: Logo + hamburguesa -->
    <div class="topbar-left">
      <button class="menu-btn" @click="$emit('toggle-sidebar')">
        <svg
          width="22"
          height="22"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>
      <div class="logo-text">SICAM</div>
    </div>

    <!-- CENTRO: Navegación siempre centrada -->
    <div class="topbar-center">
      <!-- Registro -->
      <button
        class="nav-btn"
        :class="{ active: seccion === 'registro' }"
        @click="$emit('change-section', 'registro')"
      >
        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
        </svg>
        <span class="nav-label">Registro</span>
      </button>

      <!-- Segmentación -->
      <button
        class="nav-btn"
        :class="{ active: seccion === 'segmentacion' }"
        @click="$emit('change-section', 'segmentacion')"
      >
        <svg
          class="nav-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M2 12h4l3-9 5 18 3-9h5" />
        </svg>
        <span class="nav-label">Segmentación</span>
      </button>

      <!-- Caracterización -->
      <div class="nav-btn-wrap">
        <button
          class="nav-btn"
          :class="{ active: seccion === 'caracterizacion', locked: !caseId }"
          @click="$emit('change-section', 'caracterizacion')"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
            <path d="M22 12A10 10 0 0 0 12 2v10z" />
          </svg>
          <span class="nav-label">Caracterización</span>
          <svg
            v-if="!caseId"
            class="lock-icon"
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
        </button>
        <div v-if="!caseId" class="nav-tooltip">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          Selecciona un caso primero
        </div>
      </div>
    </div>

    <!-- DERECHA: Chip + Doctor — mismo ancho que la izquierda -->
    <div class="topbar-right">
      <transition name="chip-fade">
        <div v-if="caseId" class="case-chip">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span class="chip-patient">{{ patientName || "Paciente" }}</span>
          <span class="chip-divider">·</span>
          <span class="chip-case">Caso #{{ caseId }}</span>
        </div>
      </transition>

      <div class="doctor-menu-wrap" v-if="doctor">
        <button
          class="doctor-avatar-btn"
          :class="{ active: menuOpen }"
          @click="menuOpen = !menuOpen"
        >
          <div class="doctor-avatar">{{ doctorInitials }}</div>
          <div class="doctor-info">
            <span class="doctor-name">{{ doctor.nombre }} {{ doctor.apellido }}</span>
            <span class="doctor-role">{{ doctor.especialidad_display || "Doctor" }}</span>
          </div>
          <svg
            class="chevron"
            :class="{ rotated: menuOpen }"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>

        <transition name="menu-drop">
          <div v-if="menuOpen" class="doctor-dropdown">
            <div class="dropdown-header">
              <div class="dropdown-avatar">{{ doctorInitials }}</div>
              <div class="dropdown-header-info">
                <div class="dropdown-name">
                  {{ doctor.nombre_completo || `Dr. ${doctor.nombre} ${doctor.apellido}` }}
                </div>
                <div class="dropdown-email">{{ doctor.email }}</div>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item logout-item" @click="onLogout">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
              Cerrar sesión
            </button>
          </div>
        </transition>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "TopBar",

  props: {
    seccion: { type: String, required: true },
    caseId: { type: [String, Number], default: null },
    patientName: { type: String, default: null },
    doctor: { type: Object, default: null },
  },

  emits: ["change-section", "toggle-sidebar", "logout"],

  data() {
    return { menuOpen: false };
  },

  computed: {
    doctorInitials() {
      if (!this.doctor) return "?";
      return (
        (this.doctor.nombre || "").charAt(0).toUpperCase() +
        (this.doctor.apellido || "").charAt(0).toUpperCase()
      );
    },
  },

  methods: {
    onLogout() {
      this.menuOpen = false;
      this.$emit("logout");
    },
  },
};
</script>

<style scoped>
/* ============================================================
   TOPBAR — grid de 3 columnas simétricas
   La columna izquierda y derecha tienen el MISMO ancho fijo,
   así el centro siempre queda perfectamente centrado sin importar
   si el chip aparece o desaparece.
============================================================ */
.topbar {
  height: 60px;
  background: linear-gradient(to right, #ffffff 0%, #f8f9fa 100%);
  border-bottom: 2px solid #e0e0e0;
  display: grid;
  grid-template-columns: 220px 1fr 300px;
  align-items: center;
  padding: 0 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 100;
  box-sizing: border-box;
}

/* ── IZQUIERDA ── */
.topbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
}

.menu-btn {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #2c3e50;
  padding: 4px;
  border-radius: 6px;
  flex-shrink: 0;
  transition: background 0.2s;
}

.menu-btn:hover {
  background: #f0f4f8;
}

.logo-text {
  font-weight: 700;
  font-size: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  white-space: nowrap;
}

/* ── CENTRO ── */
.topbar-center {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.nav-btn-wrap {
  position: relative;
}

.nav-btn {
  background: transparent;
  border: 2px solid transparent;
  padding: 8px 16px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  font-family: inherit;
}

.nav-btn:hover {
  background: #f0f4f8;
  color: #2c3e50;
  transform: translateY(-1px);
}

.nav-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-weight: 600;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.nav-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  transition: transform 0.25s ease;
}

.nav-btn:hover .nav-icon {
  transform: scale(1.1);
}

.nav-btn.locked {
  color: #aaa;
  border-color: #e8e8e8;
  background: #fafafa;
}

.nav-btn.locked:hover {
  background: #f5f0ff;
  color: #9c7dd4;
  border-color: #d4c5f0;
}

.lock-icon {
  width: 12px;
  height: 12px;
  opacity: 0.5;
  margin-left: 2px;
}

.nav-btn-wrap:hover .nav-tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.nav-tooltip {
  position: absolute;
  bottom: -38px;
  left: 50%;
  transform: translateX(-50%) translateY(-4px);
  background: #2c3e50;
  color: white;
  font-size: 11px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 6px;
  white-space: nowrap;
  opacity: 0;
  transition: all 0.2s ease;
  pointer-events: none;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 5px;
}

.nav-tooltip svg {
  width: 11px;
  height: 11px;
}

.nav-tooltip::before {
  content: "";
  position: absolute;
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  border: 4px solid transparent;
  border-bottom-color: #2c3e50;
  border-top: 0;
}

/* ── DERECHA ── */
.topbar-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  overflow: visible; /* el chip nunca desborda la columna */
  min-width: 0;
}

.case-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #667eea;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
  border-radius: 20px;
  padding: 6px 12px 6px 10px;

  max-width: 100%;
  min-width: 80px;

  overflow: hidden;
  flex-shrink: 1;
}

.case-chip svg {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  stroke: #667eea;
}

.chip-patient {
  font-weight: 600;
  color: #4338ca;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
  flex: 1;
}

.chip-divider {
  color: #a5b4fc;
  flex-shrink: 0;
}

.chip-case {
  color: #818cf8;
  white-space: nowrap;
  flex-shrink: 0;
  font-size: 10px;
}

.chip-fade-enter-active {
  transition: all 0.25s ease;
}
.chip-fade-leave-active {
  transition: all 0.2s ease;
}
.chip-fade-enter-from,
.chip-fade-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* ── Doctor ── */
.doctor-menu-wrap {
  position: relative;
  flex-shrink: 0;
}

.doctor-avatar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  padding: 5px 10px 5px 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.doctor-avatar-btn:hover,
.doctor-avatar-btn.active {
  background: #f0f4f8;
  border-color: #667eea;
}

.doctor-avatar {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: 0.5px;
}

.doctor-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.doctor-name {
  font-size: 12px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.2;
  white-space: nowrap;
}

.doctor-role {
  font-size: 10px;
  color: #9ca3af;
  line-height: 1.2;
  white-space: nowrap;
}

.chevron {
  width: 14px;
  height: 14px;
  stroke: #9ca3af;
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.chevron.rotated {
  transform: rotate(180deg);
}

/* Dropdown */
.doctor-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  width: 240px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  z-index: 9999;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #fafbff;
}

.dropdown-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dropdown-header-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.dropdown-name {
  font-size: 13px;
  font-weight: 600;
  color: #1a202c;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-email {
  font-size: 11px;
  color: #9ca3af;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-divider {
  height: 1px;
  background: #f0f0f0;
  margin: 4px 0;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 9px 16px;
  background: none;
  border: none;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
  font-family: inherit;
}

.dropdown-item:hover {
  background: #f8f9ff;
}
.dropdown-item svg {
  width: 15px;
  height: 15px;
  stroke: #9ca3af;
  flex-shrink: 0;
}
.logout-item {
  color: #dc2626;
}
.logout-item:hover {
  background: #fff5f5;
}
.logout-item svg {
  stroke: #dc2626;
}

.menu-drop-enter-active {
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.menu-drop-leave-active {
  transition: all 0.15s ease;
}
.menu-drop-enter-from,
.menu-drop-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* ============================================================
   RESPONSIVE
============================================================ */

/* Tablet grande */
@media (max-width: 1100px) {
  .topbar {
    grid-template-columns: 180px 1fr 180px;
    padding: 0 12px;
  }
  .nav-btn {
    padding: 8px 12px;
    font-size: 13px;
  }
}

/* Tablet pequeña: ocultar textos, solo iconos en nav */
@media (max-width: 860px) {
  .topbar {
    grid-template-columns: 100px 1fr 100px;
    padding: 0 10px;
  }
  .menu-btn {
    display: flex;
  }
  .nav-label {
    display: none;
  }
  .nav-btn {
    padding: 8px 10px;
  }
  .case-chip {
    display: none;
  }
  .doctor-info,
  .chevron {
    display: none;
  }
  .doctor-avatar-btn {
    padding: 5px;
    border-radius: 8px;
  }
  .logo-text {
    font-size: 15px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .topbar {
    grid-template-columns: 40px 1fr 40px;
    padding: 0 8px;
  }
  .logo-text {
    display: none;
  }
}
</style>
