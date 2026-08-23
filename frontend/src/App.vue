<template>
  <!-- ================================================
       LOGIN — se muestra si no hay doctor autenticado
  ================================================ -->
  <LoginView v-if="!doctor" @login-success="onLoginSuccess" />

  <!-- ================================================
       APP PRINCIPAL
  ================================================ -->
  <template v-else>
    <TopBar
      :seccion="seccion"
      :caseId="selectedCaseId"
      :patientName="selectedPatientName"
      :doctor="doctor"
      @change-section="seccion = $event"
      @toggle-sidebar="sidebarOpen = !sidebarOpen"
      @logout="handleLogout"
    />

    <!-- Overlay oscuro del sidebar en mobile -->
    <div
      v-show="sidebarOpen && seccion === 'segmentacion'"
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    ></div>

    <!-- SEGMENTACIÓN -->
    <div class="app" v-show="seccion === 'segmentacion'">
      <SideBar
        ref="sidebar"
        :isOpen="sidebarOpen"
        :doctorId="doctor.id_doctor"
        @close-sidebar="sidebarOpen = false"
        @select-patient="onSelectPatient"
        @select-case="onSelectCase"
        @reset-selection="resetSelection"
        @analisis-progreso="mainContentRefreshKey = Date.now()"
        @analisis-completado="mainContentRefreshKey = Date.now()"
      />
      <MainContent
        :patientId="selectedPatientId"
        :patientName="selectedPatientName"
        :caseId="selectedCaseId"
        :refreshKey="mainContentRefreshKey"
        @edicion-guardada="
          () => {
            $refs.sidebar.recargarResumen();
            mainContentRefreshKey++;
          }
        "
      />
    </div>

    <!-- CARACTERIZACIÓN -->
    <div class="app-single" v-show="seccion === 'caracterizacion'">
      <CaracterizacionView
        :patientId="selectedPatientId"
        :caseId="selectedCaseId"
        :refreshKey="mainContentRefreshKey"
        @update-patient="onSelectPatient"
        @update-case="onSelectCase"
        @go-segmentacion="seccion = 'segmentacion'"
      />
    </div>

    <!-- REGISTRO -->
    <div class="app-single app-registro" v-show="seccion === 'registro'">
      <RegistroView
        @paciente-registrado="$refs.sidebar?.cargarPacientes()"
        @muestra-registrada="onMuestraRegistrada"
      />
    </div>
  </template>
</template>

<script>
import TopBar from "./components/TopBar.vue";
import SideBar from "./components/SideBar.vue";
import MainContent from "./components/MainContent.vue";
import RegistroView from "./views/RegistroView.vue";
import CaracterizacionView from "./views/CaracterizacionView.vue";
import LoginView from "./views/LoginView.vue";

export default {
  name: "App",

  components: {
    TopBar,
    SideBar,
    MainContent,
    RegistroView,
    CaracterizacionView,
    LoginView,
  },

  data() {
    return {
      seccion: "segmentacion",
      selectedPatientId: null,
      selectedPatientName: null,
      selectedCaseId: null,
      sidebarOpen: false,
      doctor: null, // null = no autenticado → muestra LoginView
      mainContentRefreshKey: 0,
    };
  },

  created() {
    // Al recargar la página, restaurar sesión guardada en localStorage
    this.restoreSession();
  },

  methods: {
    // ── Autenticación ───────────────────────────────────────────────

    restoreSession() {
      const token = localStorage.getItem("access_token");
      const doctorGuard = localStorage.getItem("doctor");

      if (token && doctorGuard) {
        try {
          this.doctor = JSON.parse(doctorGuard);
        } catch {
          this.clearSession();
        }
      }
    },

    onLoginSuccess(doctor) {
      this.doctor = doctor;
      this.seccion = "segmentacion";
      this.sidebarOpen = true;
    },

    async handleLogout() {
      // Blacklistear el token en el backend (best-effort: no bloquear si falla)
      try {
        await fetch("/api/auth/logout/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            refresh: localStorage.getItem("refresh_token"),
          }),
        });
      } catch {
        // Si falla la red, igual limpiamos la sesión local
      }

      this.clearSession();
    },

    clearSession() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("doctor");

      this.doctor = null;
      this.selectedPatientId = null;
      this.selectedPatientName = null;
      this.selectedCaseId = null;
      this.seccion = "segmentacion";
      this.sidebarOpen = false;
    },

    // ── Selección de paciente / caso ────────────────────────────────

    onSelectPatient(patientId, patientName = "") {
      // <-- Añade patientName aquí
      this.selectedPatientId = patientId;
      this.selectedPatientName = patientName; // <-- Guárdalo aquí
      this.selectedCaseId = null;
    },

    onSelectCase(caseId) {
      this.selectedCaseId = caseId;
    },

    resetSelection() {
      this.selectedPatientId = null;
      this.selectedPatientName = null;
      this.selectedCaseId = null;
    },

    onMuestraRegistrada() {
      // 1. Si el Sidebar está activo, le decimos que recargue el resumen del caso actual
      if (this.$refs.sidebar) {
        this.$refs.sidebar.recargarResumen();
      }

      // 2. Cambiamos la "llave" del componente principal para forzar
      // que vuelva a pedir las imágenes a la base de datos (como si dieras F5)
      this.mainContentRefreshKey++;
    },
  },

  watch: {
    seccion(nueva, vieja) {
      // Cerrar sidebar automáticamente al cambiar a otra sección
      this.sidebarOpen = nueva === "segmentacion";
      // Al volver a segmentación desde registro, recargar lista de pacientes
      if (nueva === "segmentacion" && vieja === "registro") {
        this.$nextTick(() => {
          this.$refs.sidebar?.cargarPacientes();
        });
      }
    },
  },
};
</script>

<style>
/* ============================================================
   RESET Y BASE
============================================================ */
* {
  box-sizing: border-box;
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

body {
  margin: 0;
  background: #f0f2f5;
  color: #2c3e50;
  height: 100vh;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ============================================================
   LAYOUTS DE SECCIÓN
============================================================ */
.app {
  display: flex;
  height: calc(100vh - 60px);
  background: #f0f2f5;
  overflow: hidden;
}

.app-single {
  height: calc(100vh - 60px);
  overflow: hidden;
}

.app-registro {
  overflow-y: auto !important;
  overflow-x: hidden;
}

/* ============================================================
   SCROLLBAR PERSONALIZADA
============================================================ */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* ============================================================
   UTILIDADES GLOBALES
============================================================ */
*:focus-visible {
  outline: 3px solid #667eea;
  outline-offset: 2px;
}

::selection {
  background: #667eea;
  color: white;
}

/* ============================================================
   OVERLAY SIDEBAR (mobile)
============================================================ */
.sidebar-overlay {
  display: none;
}

@media (max-width: 1200px) {
  .app {
    position: relative;
  }

  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.35);
    z-index: 900;
  }
}
</style>
