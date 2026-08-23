<template>
  <div class="registro-root">
    <!-- Fondo con textura sutil -->
    <div class="bg-texture"></div>

    <div class="registro-container">
      <!-- HEADER -->
      <header class="registro-header">
        <div class="header-eyebrow">Sistema de Gestión Clínica</div>
        <h1 class="header-title">Registro Clínico</h1>
        <p class="header-sub">Complete los pasos en orden para registrar un nuevo caso</p>
      </header>

      <!-- STEPPER -->
      <div class="stepper">
        <div
          v-for="(step, i) in pasos"
          :key="i"
          class="step"
          :class="{
            active: vistaActiva === step.key,
            completed: pasoCompletado(step.key),
          }"
          @click="irAPaso(step.key)"
        >
          <div class="step-bubble">
            <span v-if="!pasoCompletado(step.key)" class="step-num">{{ i + 1 }}</span>
            <svg
              v-else
              class="step-check"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
          <div class="step-info">
            <span class="step-label">{{ step.label }}</span>
            <span class="step-sub">{{ step.sub }}</span>
          </div>
          <div v-if="i < pasos.length - 1" class="step-connector">
            <div class="connector-line" :class="{ filled: pasoCompletado(step.key) }"></div>
          </div>
        </div>
      </div>

      <!-- PANEL DE FORMULARIOS -->
      <div class="form-panel">
        <!-- ===== PACIENTE ===== -->
        <transition name="slide-fade" mode="out-in">
          <div v-if="vistaActiva === 'paciente'" key="paciente" class="form-card">
            <div class="form-card-accent"></div>

            <div class="form-card-header">
              <div class="form-icon paciente-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div>
                <h2 class="form-title">Datos del Paciente</h2>
                <p class="form-desc">Información de identificación personal</p>
              </div>
            </div>

            <form @submit.prevent="crearPaciente" class="form-body">
              <div class="fields-grid two-col">
                <div class="field-float">
                  <input v-model="paciente.nombre" id="f-nombre" placeholder=" " required />
                  <label for="f-nombre">Nombre *</label>
                </div>
                <div class="field-float">
                  <input v-model="paciente.apellido" id="f-apellido" placeholder=" " required />
                  <label for="f-apellido">Apellido *</label>
                </div>
                <div class="field-float">
                  <input v-model="paciente.identificacion" id="f-id" placeholder=" " required />
                  <label for="f-id">Identificación *</label>
                </div>
                <div class="field-float">
                  <input
                    v-model="paciente.fecha_nacimiento"
                    id="f-fecha"
                    type="date"
                    placeholder=" "
                    required
                  />
                  <label for="f-fecha" class="label-up">Fecha de Nacimiento *</label>
                </div>
                <div class="field-float">
                  <input v-model="paciente.email" id="f-email" type="email" placeholder=" " />
                  <label for="f-email">Email</label>
                </div>
                <div class="field-float">
                  <input v-model="paciente.telefono" id="f-tel" placeholder=" " />
                  <label for="f-tel">Teléfono</label>
                </div>
              </div>

              <!-- Feedback -->
              <transition name="msg-fade">
                <div v-if="mensajes.paciente" class="feedback-msg" :class="mensajes.paciente.tipo">
                  {{ mensajes.paciente.texto }}
                </div>
              </transition>

              <div class="form-footer">
                <div class="footer-hint">Los campos con * son obligatorios</div>
                <button class="btn-submit" :disabled="cargando.paciente">
                  <span v-if="!cargando.paciente">Guardar Paciente ✓</span>
                  <span v-else class="btn-loading">
                    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                  </span>
                </button>
              </div>
            </form>
          </div>
        </transition>

        <!-- ===== CASO ===== -->
        <transition name="slide-fade" mode="out-in">
          <div v-if="vistaActiva === 'caso'" key="caso" class="form-card">
            <div class="form-card-accent caso-accent"></div>

            <div class="form-card-header">
              <div class="form-icon caso-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
              </div>
              <div>
                <h2 class="form-title">Caso Clínico</h2>
                <p class="form-desc">Asocie el caso a un paciente registrado</p>
              </div>
            </div>

            <form @submit.prevent="crearCaso" class="form-body">
              <div class="fields-grid one-col">
                <div class="field-select-group">
                  <label class="select-label">Paciente *</label>
                  <div class="select-wrapper">
                    <select v-model="caso.id_paciente_fk" required>
                      <option value="">— Seleccione un paciente —</option>
                      <option v-for="p in pacientes" :key="p.id_paciente" :value="p.id_paciente">
                        {{ p.nombre }} {{ p.apellido }} · {{ p.identificacion }}
                      </option>
                    </select>
                    <svg
                      class="select-arrow"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </div>
                </div>

                <div class="field-select-group">
                  <label class="select-label">Estado inicial</label>
                  <div class="select-wrapper">
                    <select v-model="caso.estado">
                      <option value="abierto">🟢 Abierto</option>
                      <option value="en_proceso">🟡 En Proceso</option>
                      <option value="cerrado">🔴 Cerrado</option>
                    </select>
                    <svg
                      class="select-arrow"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </div>
                </div>

                <div class="field-float textarea-field">
                  <textarea
                    v-model="caso.diagnostico"
                    id="f-diag"
                    placeholder=" "
                    rows="4"
                  ></textarea>
                  <label for="f-diag">Diagnóstico / Notas clínicas</label>
                </div>
              </div>

              <transition name="msg-fade">
                <div v-if="mensajes.caso" class="feedback-msg" :class="mensajes.caso.tipo">
                  {{ mensajes.caso.texto }}
                </div>
              </transition>

              <div class="form-footer">
                <div class="footer-hint">Los campos con * son obligatorios</div>
                <button class="btn-submit caso-submit" :disabled="cargando.caso">
                  <span v-if="!cargando.caso">Guardar Caso ✓</span>
                  <span v-else class="btn-loading">
                    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                  </span>
                </button>
              </div>
            </form>
          </div>
        </transition>

        <!-- ===== MUESTRA ===== -->
        <transition name="slide-fade" mode="out-in">
          <div v-if="vistaActiva === 'muestra'" key="muestra" class="form-card">
            <div class="form-card-accent muestra-accent"></div>

            <div class="form-card-header">
              <div class="form-icon muestra-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M8 3v3a2 2 0 0 1-2 2H3" />
                  <path
                    d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"
                  />
                </svg>
              </div>
              <div>
                <h2 class="form-title">Muestra Microscópica</h2>
                <p class="form-desc">Suba la imagen de la muestra para análisis</p>
              </div>
            </div>

            <form @submit.prevent="registrarMuestra" class="form-body">
              <div class="fields-grid one-col">
                <div class="field-select-group">
                  <label class="select-label">Paciente *</label>
                  <div class="select-wrapper">
                    <select v-model="pacienteSeleccionadoId" @change="filtrarCasosPorPaciente">
                      <option value="">— Seleccione un paciente —</option>
                      <option v-for="p in pacientes" :key="p.id_paciente" :value="p.id_paciente">
                        {{ p.nombre }} {{ p.apellido }} · {{ p.identificacion }}
                      </option>
                    </select>
                    <svg
                      class="select-arrow"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </div>
                </div>

                <div class="field-select-group">
                  <label class="select-label">Caso Clínico *</label>
                  <div class="select-wrapper" :class="{ disabled: !pacienteSeleccionadoId }">
                    <select
                      v-model="muestra.id_caso_fk"
                      :disabled="!pacienteSeleccionadoId"
                      required
                    >
                      <option value="">
                        {{
                          pacienteSeleccionadoId
                            ? "— Seleccione el caso —"
                            : "Primero elija un paciente"
                        }}
                      </option>
                      <option v-for="c in casosFiltrados" :key="c.id_caso" :value="c.id_caso">
                        Caso #{{ c.id_caso }} — {{ getEstadoLabel(c.estado) }}
                      </option>
                    </select>
                    <svg
                      class="select-arrow"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </div>
                </div>

                <div class="field-select-group">
                  <label class="select-label">Tipo de Muestra</label>
                  <div class="tipo-toggle">
                    <button
                      type="button"
                      class="tipo-btn"
                      :class="{ active: muestra.tipo_muestra === 'saliva' }"
                      @click="muestra.tipo_muestra = 'saliva'"
                    >
                      💧 Saliva
                    </button>
                    <button
                      type="button"
                      class="tipo-btn"
                      :class="{ active: muestra.tipo_muestra === 'sangre' }"
                      @click="muestra.tipo_muestra = 'sangre'"
                    >
                      🩸 Sangre
                    </button>
                  </div>
                </div>

                <!-- Dropzone multi-imagen -->
                <div
                  class="dropzone"
                  :class="{ 'has-file': archivos.length > 0, dragging: isDragging }"
                  @dragover.prevent="isDragging = true"
                  @dragleave="isDragging = false"
                  @drop.prevent="onDrop"
                  @click="$refs.fileInput.click()"
                >
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    multiple
                    style="display: none"
                    @change="onFileChange"
                  />

                  <!-- Estado vacío -->
                  <div v-if="archivos.length === 0" class="dropzone-empty">
                    <div class="dropzone-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                    </div>
                    <p class="dropzone-text">Arrastre las imágenes aquí</p>
                    <p class="dropzone-hint">
                      o haga click para seleccionar · PNG, JPG, TIFF · Múltiples archivos
                    </p>
                  </div>

                  <!-- Lista de archivos con progreso -->
                  <div v-else class="archivos-lista" @click.stop>
                    <div class="archivos-header">
                      <span class="archivos-count"
                        >{{ archivos.length }} imagen{{
                          archivos.length > 1 ? "es" : ""
                        }}
                        seleccionada{{ archivos.length > 1 ? "s" : "" }}</span
                      >
                      <button
                        type="button"
                        class="btn-agregar-mas"
                        @click="$refs.fileInput.click()"
                      >
                        + Agregar más
                      </button>
                    </div>

                    <div class="archivo-item" v-for="(a, i) in archivos" :key="i">
                      <!-- Preview -->
                      <div class="archivo-thumb">
                        <img :src="a.preview" :alt="a.nombre" />
                      </div>

                      <!-- Info + progreso -->
                      <div class="archivo-detalle">
                        <span class="archivo-nombre">{{ a.nombre }}</span>

                        <!-- Barra de progreso -->
                        <div class="progreso-wrap" v-if="a.estado !== 'pendiente'">
                          <div class="progreso-bar">
                            <div
                              class="progreso-fill"
                              :class="'estado-' + a.estado"
                              :style="{ width: a.progreso + '%' }"
                            ></div>
                          </div>
                          <span class="progreso-label" :class="'label-' + a.estado">
                            {{ estadoLabel(a) }}
                          </span>
                        </div>
                        <span v-else class="archivo-size">{{ formatSize(a.size) }}</span>
                      </div>

                      <!-- Quitar (solo si no está subiendo) -->
                      <button
                        type="button"
                        class="archivo-quitar"
                        @click.stop="quitarArchivo(i)"
                        :disabled="a.estado === 'subiendo'"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Resumen final al terminar -->
              <transition name="msg-fade">
                <div v-if="resumenSubida" class="resumen-subida">
                  <div class="resumen-item ok" v-if="resumenSubida.ok > 0">
                    ✅ {{ resumenSubida.ok }} imagen{{ resumenSubida.ok > 1 ? "es" : "" }} subida{{
                      resumenSubida.ok > 1 ? "s" : ""
                    }}
                    correctamente
                  </div>
                  <div class="resumen-item err" v-if="resumenSubida.err > 0">
                    ❌ {{ resumenSubida.err }} imagen{{
                      resumenSubida.err > 1 ? "es fallaron" : " falló"
                    }}
                  </div>
                </div>
              </transition>

              <transition name="msg-fade">
                <div v-if="mensajes.muestra" class="feedback-msg" :class="mensajes.muestra.tipo">
                  {{ mensajes.muestra.texto }}
                </div>
              </transition>

              <div class="form-footer">
                <div class="footer-hint">
                  {{
                    archivos.length > 0
                      ? `${archivos.filter((a) => a.estado === "listo").length}/${archivos.length} subidas`
                      : "Los campos con * son obligatorios"
                  }}
                </div>
                <button
                  class="btn-submit muestra-submit"
                  :disabled="cargando.muestra || archivos.length === 0"
                >
                  <span v-if="!cargando.muestra">
                    Subir {{ archivos.length > 1 ? archivos.length + " imágenes" : "imagen" }} ✓
                  </span>
                  <span v-else class="btn-loading">
                    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                  </span>
                </button>
              </div>
            </form>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios.js";

export default {
  name: "RegistroClinico",

  emits: ["paciente-registrado", "muestra-registrada"],

  data() {
    return {
      API: "/api",
      vistaActiva: "paciente",

      pasos: [
        { key: "paciente", label: "Paciente", sub: "Datos personales" },
        { key: "caso", label: "Caso Clínico", sub: "Historia médica" },
        { key: "muestra", label: "Muestra", sub: "Imagen microscópica" },
      ],

      // Datos completados (para el stepper)
      completados: { paciente: false, caso: false },

      // Listas del API
      pacientes: [],
      casos: [],

      // Selección en muestra
      pacienteSeleccionadoId: "",
      casosFiltrados: [],

      // Modelos de formulario
      paciente: {
        nombre: "",
        apellido: "",
        identificacion: "",
        fecha_nacimiento: "",
        email: "",
        telefono: "",
      },

      caso: {
        id_paciente_fk: "",
        diagnostico: "",
        estado: "abierto",
      },

      muestra: {
        id_caso_fk: "",
        tipo_muestra: "saliva",
      },

      // UI state — multi-imagen
      archivos: [], // [{ file, nombre, size, preview, estado, progreso }]
      isDragging: false,
      resumenSubida: null, // { ok, err } al finalizar

      cargando: { paciente: false, caso: false, muestra: false },
      mensajes: { paciente: null, caso: null, muestra: null },
    };
  },

  mounted() {
    this.cargarPacientes();
    this.cargarCasos();
  },

  methods: {
    // ─── NAVEGACIÓN STEPPER — libre, sin dependencias ───────────────
    irAPaso(key) {
      this.vistaActiva = key;
    },

    pasoCompletado(key) {
      return this.completados[key] || false;
    },

    // ─── PACIENTE ────────────────────────────────────────────────────
    async cargarPacientes() {
      try {
        const r = await axios.get(`${this.API}/pacientes/`);
        this.pacientes = r.data;
      } catch (e) {
        console.error("Error al cargar pacientes:", e);
      }
    },

    async crearPaciente() {
      this.cargando.paciente = true;
      this.mensajes.paciente = null;
      try {
        await axios.post(`${this.API}/pacientes/`, this.paciente);
        this.mensajes.paciente = { tipo: "success", texto: "✅ Paciente registrado correctamente" };
        this.completados.paciente = true;
        this.$emit("paciente-registrado");
        this.paciente = {
          nombre: "",
          apellido: "",
          identificacion: "",
          fecha_nacimiento: "",
          email: "",
          telefono: "",
        };
        await this.cargarPacientes();
      } catch (e) {
        const err = e.response?.data;
        const msg = typeof err === "object" ? Object.values(err).flat().join(" · ") : e.message;
        this.mensajes.paciente = { tipo: "error", texto: "❌ " + msg };
      } finally {
        this.cargando.paciente = false;
      }
    },

    // ─── CASO ────────────────────────────────────────────────────────
    async cargarCasos() {
      try {
        const r = await axios.get(`${this.API}/casos/`);
        this.casos = r.data;
      } catch (e) {
        console.error("Error al cargar casos:", e);
      }
    },

    async crearCaso() {
      this.cargando.caso = true;
      this.mensajes.caso = null;
      try {
        await axios.post(`${this.API}/casos/`, this.caso);
        this.mensajes.caso = { tipo: "success", texto: "✅ Caso clínico creado correctamente" };
        this.completados.caso = true;
        this.caso = { id_paciente_fk: "", diagnostico: "", estado: "abierto" };
        await this.cargarCasos();
      } catch (e) {
        const err = e.response?.data;
        const msg = typeof err === "object" ? Object.values(err).flat().join(" · ") : e.message;
        this.mensajes.caso = { tipo: "error", texto: "❌ " + msg };
      } finally {
        this.cargando.caso = false;
      }
    },

    // ─── MUESTRA — MULTI-IMAGEN ──────────────────────────────────────
    onFileChange(e) {
      this.agregarArchivos(Array.from(e.target.files));
      // Reset input para poder agregar los mismos archivos de nuevo si se quitaron
      e.target.value = "";
    },

    onDrop(e) {
      this.isDragging = false;
      const files = Array.from(e.dataTransfer.files).filter((f) => f.type.startsWith("image/"));
      this.agregarArchivos(files);
    },

    agregarArchivos(files) {
      const nuevos = files.map((file) => ({
        file,
        nombre: file.name,
        size: file.size,
        preview: URL.createObjectURL(file),
        estado: "pendiente", // pendiente | subiendo | listo | error
        progreso: 0,
      }));
      this.archivos = [...this.archivos, ...nuevos];
      this.resumenSubida = null;
    },

    quitarArchivo(index) {
      URL.revokeObjectURL(this.archivos[index].preview);
      this.archivos.splice(index, 1);
    },

    estadoLabel(a) {
      if (a.estado === "subiendo") return `${a.progreso}%`;
      if (a.estado === "listo") return "✓ Subida";
      if (a.estado === "error") return "✗ Error";
      return "";
    },

    formatSize(bytes) {
      if (bytes < 1024) return bytes + " B";
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
      return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    },

    filtrarCasosPorPaciente() {
      this.muestra.id_caso_fk = "";
      if (!this.pacienteSeleccionadoId) {
        this.casosFiltrados = [];
        return;
      }
      this.casosFiltrados = this.casos.filter(
        (c) => Number(c.id_paciente_fk) === Number(this.pacienteSeleccionadoId),
      );
    },

    async registrarMuestra() {
      if (!this.muestra.id_caso_fk) {
        this.mensajes.muestra = { tipo: "error", texto: "❌ Selecciona un caso clínico" };
        return;
      }
      if (this.archivos.length === 0) {
        this.mensajes.muestra = { tipo: "error", texto: "❌ Agrega al menos una imagen" };
        return;
      }

      this.cargando.muestra = true;
      this.mensajes.muestra = null;
      this.resumenSubida = null;

      let ok = 0,
        err = 0;

      // Subir secuencialmente — evita saturar el servidor
      for (const archivo of this.archivos) {
        if (archivo.estado === "listo") {
          ok++;
          continue;
        } // ya subida

        archivo.estado = "subiendo";
        archivo.progreso = 0;

        const formData = new FormData();
        formData.append("id_caso_fk", this.muestra.id_caso_fk);
        formData.append("tipo_muestra", this.muestra.tipo_muestra);
        formData.append("ruta_imagen", archivo.file);

        try {
          await axios.post(`${this.API}/subir-muestra/`, formData, {
            headers: { "Content-Type": "multipart/form-data" },
            onUploadProgress: (e) => {
              archivo.progreso = Math.round((e.loaded / e.total) * 100);
            },
          });
          archivo.estado = "listo";
          archivo.progreso = 100;
          ok++;
        } catch (e) {
          archivo.estado = "error";
          console.error(`Error subiendo ${archivo.nombre}:`, e);
          err++;
        }
      }

      this.resumenSubida = { ok, err };
      this.cargando.muestra = false;

      // Si todo fue bien, limpiar después de 2s
      if (err === 0) {
        setTimeout(() => {
          this.archivos.forEach((a) => URL.revokeObjectURL(a.preview));
          this.archivos = [];
          this.resumenSubida = null;
          this.muestra.id_caso_fk = "";
          this.pacienteSeleccionadoId = "";
          this.casosFiltrados = [];

          this.$emit("muestra-registrada");
        }, 2000);
      }
    },

    getEstadoLabel(estado) {
      return { abierto: "Abierto", en_proceso: "En Proceso", cerrado: "Cerrado" }[estado] || estado;
    },
  },
};
</script>

<style scoped>
/* =============================================
   ROOT & BACKGROUND
   — mismo fondo claro que MainContent (#f8f9fa)
============================================= */
.registro-root {
  background: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  position: relative;
  overflow-y: auto;
  padding: 20px 20px 40px;
  /* No min-height: 100vh — deja que el layout padre controle la altura */
}

.bg-texture {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 40% at 15% 0%, rgba(102, 126, 234, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse 50% 35% at 85% 90%, rgba(118, 75, 162, 0.05) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.registro-container {
  position: relative;
  z-index: 1;
  max-width: 780px;
  margin: 0 auto;
}

/* =============================================
   HEADER  — mismo tono que .page-title
============================================= */
.registro-header {
  text-align: center;
  margin-bottom: 20px;
  animation: fadeDown 0.6s ease both;
}

.header-eyebrow {
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #667eea;
  margin-bottom: 8px;
  font-weight: 600;
}

.header-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50; /* = .page-title */
  margin: 0 0 6px;
  letter-spacing: -0.3px;
}

.header-sub {
  font-size: 13px;
  color: #999;
  margin: 0;
}

/* =============================================
   STEPPER
============================================= */
.stepper {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0;
  margin-bottom: 20px;
  animation: fadeDown 0.6s 0.1s ease both;
}

.step {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  position: relative;
}

.step-bubble {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid #e0e0e0;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.35s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.step-num {
  font-size: 13px;
  font-weight: 600;
  color: #bbb;
  transition: color 0.3s;
}

.step-check {
  width: 15px;
  height: 15px;
  color: #667eea;
  stroke-width: 2.5;
}

.step.active .step-bubble {
  border-color: #667eea;
  background: #ffffff;
  box-shadow:
    0 0 0 4px rgba(102, 126, 234, 0.12),
    0 2px 8px rgba(102, 126, 234, 0.2);
}

.step.active .step-num {
  color: #667eea;
}

.step.completed .step-bubble {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.08);
}

.step-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.step-label {
  font-size: 13px;
  font-weight: 600;
  color: #bbb;
  transition: color 0.3s;
  white-space: nowrap;
}

.step-sub {
  font-size: 11px;
  color: #ccc;
  white-space: nowrap;
}

.step.active .step-label {
  color: #667eea;
}
.step.active .step-sub {
  color: #999;
}
.step.completed .step-label {
  color: #667eea;
}
.step.completed .step-sub {
  color: #999;
}

.step-connector {
  display: flex;
  align-items: center;
  padding: 0 14px;
  margin-bottom: 20px;
}

.connector-line {
  width: 60px;
  height: 2px;
  background: #e0e0e0;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.connector-line::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: translateX(-100%);
  transition: transform 0.5s ease;
}

.connector-line.filled::after {
  transform: translateX(0);
}

/* =============================================
   FORM CARD  — mismo white/shadow que .card
============================================= */
.form-panel {
  animation: fadeUp 0.5s 0.2s ease both;
}

.form-card {
  background: #ffffff; /* igual que .card */
  border-radius: 12px; /* igual que .card */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); /* igual que .card */
  overflow: hidden;
  position: relative;
}

/* Franja superior de color — igual que .card-header::before */
.form-card-accent {
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.caso-accent {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.muestra-accent {
  background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
}

.form-card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px 24px 16px;
  border-bottom: 2px solid #f0f0f0; /* = .card-header border */
  background: linear-gradient(to right, #fafbfc, #ffffff); /* = .card-header bg */
}

.form-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.form-icon svg {
  width: 20px;
  height: 20px;
}

/* Iconos: usan los mismos gradientes del sidebar */
.paciente-icon {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}
.caso-icon {
  background: rgba(118, 75, 162, 0.1);
  color: #764ba2;
}
.muestra-icon {
  background: rgba(66, 165, 245, 0.1);
  color: #1e88e5;
}

.form-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50; /* = .card-title-section h3 */
  margin: 0 0 2px;
}

.form-desc {
  font-size: 12px;
  color: #999; /* = .card-subtitle */
  margin: 0;
}

.form-body {
  padding: 24px;
}

/* =============================================
   FIELDS  — mismo estilo que inputs del SideBar
============================================= */
.fields-grid {
  display: grid;
  gap: 18px;
}
.two-col {
  grid-template-columns: 1fr 1fr;
}
.one-col {
  grid-template-columns: 1fr;
}

/* Floating label */
.field-float {
  position: relative;
}

.field-float input,
.field-float textarea {
  width: 100%;
  padding: 18px 14px 8px;
  background: #ffffff;
  border: 1.8px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  color: #2c3e50;
  outline: none;
  transition:
    border-color 0.25s,
    background 0.25s,
    box-shadow 0.25s;
  box-sizing: border-box;
  font-family: inherit;
}

.field-float textarea {
  resize: vertical;
  min-height: 100px;
}

.field-float input:focus,
.field-float textarea:focus {
  border-color: #667eea;
  background: #f9faff; /* mismo tono que el SideBar en focus */
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.field-float label {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 13px;
  color: #999;
  pointer-events: none;
  transition: all 0.2s ease;
}

.textarea-field label {
  top: 18px;
  transform: none;
}

.field-float input:focus + label,
.field-float input:not(:placeholder-shown) + label,
.field-float textarea:focus + label,
.field-float textarea:not(:placeholder-shown) + label,
.field-float .label-up {
  top: 7px;
  transform: translateY(0);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: #667eea;
  text-transform: uppercase;
}

/* Select custom */
.field-select-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.select-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #666;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  width: 100%;
  padding: 11px 40px 11px 12px;
  background: #ffffff;
  border: 1.8px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  color: #2c3e50;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition:
    border-color 0.25s,
    box-shadow 0.25s;
  font-family: inherit;
}

.select-wrapper select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.select-wrapper.disabled select {
  opacity: 0.45;
  cursor: not-allowed;
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 15px;
  height: 15px;
  color: #999;
  pointer-events: none;
}

/* Tipo toggle */
.tipo-toggle {
  display: flex;
  gap: 8px;
}

.tipo-btn {
  flex: 1;
  padding: 10px;
  border: 1.8px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.tipo-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f9faff;
}

.tipo-btn.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
}

/* Dropzone */
.dropzone {
  border: 2px dashed #e0e0e0;
  border-radius: 10px;
  background: #fafbfc;
  cursor: pointer;
  transition: all 0.25s ease;
  overflow: hidden;
  min-height: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dropzone:hover,
.dropzone.dragging {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.04);
}

.dropzone.has-file {
  border-style: solid;
  border-color: #667eea;
}

.dropzone-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 28px 20px;
  text-align: center;
}

.dropzone-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: rgba(102, 126, 234, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
}

.dropzone-icon svg {
  width: 20px;
  height: 20px;
}

.dropzone-text {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin: 0;
}
.dropzone-hint {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.dropzone-filled {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  width: 100%;
}

/* ── Multi-archivo ── */
.archivos-lista {
  width: 100%;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.archivos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  margin-bottom: 6px;
  border-bottom: 1px solid #f0f0f0;
}

.archivos-count {
  font-size: 12px;
  font-weight: 600;
  color: #667eea;
}

.btn-agregar-mas {
  font-size: 11px;
  font-weight: 600;
  color: #667eea;
  border: 1.5px solid #667eea;
  background: transparent;
  padding: 3px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.btn-agregar-mas:hover {
  background: rgba(102, 126, 234, 0.08);
}

.archivo-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #f8f8f8;
}
.archivo-item:last-child {
  border-bottom: none;
}

.archivo-thumb {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid #e0e0e0;
  background: #f5f5f5;
}
.archivo-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.archivo-detalle {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.archivo-nombre {
  font-size: 12px;
  color: #2c3e50;
  font-family: "SFMono-Regular", monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.archivo-size {
  font-size: 11px;
  color: #999;
}

/* Barra de progreso */
.progreso-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progreso-bar {
  flex: 1;
  height: 5px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
}

.progreso-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progreso-fill.estado-subiendo {
  background: linear-gradient(90deg, #667eea, #764ba2);
}
.progreso-fill.estado-listo {
  background: #66bb6a;
}
.progreso-fill.estado-error {
  background: #ef5350;
}

.progreso-label {
  font-size: 10px;
  font-weight: 600;
  white-space: nowrap;
  min-width: 45px;
  text-align: right;
}
.label-subiendo {
  color: #667eea;
}
.label-listo {
  color: #43a047;
}
.label-error {
  color: #e53935;
}

.archivo-quitar {
  width: 24px;
  height: 24px;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  background: white;
  color: #999;
  font-size: 10px;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: inherit;
}
.archivo-quitar:hover:not(:disabled) {
  border-color: #ef5350;
  color: #ef5350;
  background: #ffebee;
}
.archivo-quitar:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Resumen al finalizar */
.resumen-subida {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.resumen-item {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}
.resumen-item.ok {
  background: #e8f5e9;
  border: 1px solid #a5d6a7;
  color: #2e7d32;
}
.resumen-item.err {
  background: #ffebee;
  border: 1px solid #ef9a9a;
  color: #c62828;
}

.file-preview-wrap {
  width: 68px;
  height: 68px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid #e0e0e0;
}

.file-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-info {
  display: flex;
  flex-direction: column;
  gap: 7px;
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 12px;
  color: #666;
  font-family: "SFMono-Regular", "Consolas", monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-remove {
  display: inline-flex;
  width: fit-content;
  padding: 3px 10px;
  border: 1px solid #ef5350;
  border-radius: 6px;
  background: transparent;
  color: #ef5350;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.file-remove:hover {
  background: #ffebee;
}

/* =============================================
   FEEDBACK
============================================= */
.feedback-msg {
  margin-top: 16px;
  padding: 11px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}

.feedback-msg.success {
  background: #e8f5e9;
  border: 1px solid #a5d6a7;
  color: #2e7d32;
}

.feedback-msg.error {
  background: #ffebee;
  border: 1px solid #ef9a9a;
  color: #c62828;
}

/* =============================================
   FOOTER / BOTONES
============================================= */
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  padding-top: 18px;
  border-top: 2px solid #f0f0f0; /* = .card-header border */
}

.footer-hint {
  font-size: 12px;
  color: #bbb;
}

/* Botón principal — degradado idéntico al .breadcrumb-item.active */
.btn-submit {
  padding: 11px 26px;
  border-radius: 10px;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transition: all 0.25s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  min-width: 185px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: inherit;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Paso 2: azul/morado más oscuro */
.caso-submit {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  box-shadow: 0 4px 12px rgba(118, 75, 162, 0.3);
}
.caso-submit:hover:not(:disabled) {
  box-shadow: 0 6px 18px rgba(118, 75, 162, 0.4);
}

/* Paso 3: azul de MainContent (.breadcrumb-item) */
.muestra-submit {
  background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
}
.muestra-submit:hover:not(:disabled) {
  box-shadow: 0 6px 18px rgba(30, 136, 229, 0.4);
}

.btn-back {
  padding: 10px 18px;
  border: 2px solid #e0e0e0; /* = .btn-action border */
  border-radius: 10px;
  background: white;
  color: #666;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.btn-back:hover {
  background: #f0f4f8;
  border-color: #ccc;
  transform: translateY(-1px);
}

/* Loading dots */
.btn-loading {
  display: flex;
  gap: 5px;
  align-items: center;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
  animation: bounce 1s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.15s;
}
.dot:nth-child(3) {
  animation-delay: 0.3s;
}

/* =============================================
   TRANSITIONS & ANIMATIONS
============================================= */
.slide-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fade-leave-active {
  transition: all 0.2s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(18px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-14px);
}

.msg-fade-enter-active,
.msg-fade-leave-active {
  transition: all 0.3s ease;
}
.msg-fade-enter-from,
.msg-fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

@keyframes fadeDown {
  from {
    opacity: 0;
    transform: translateY(-14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* =============================================
   RESPONSIVE
============================================= */
@media (max-width: 640px) {
  .registro-root {
    padding: 20px 12px 50px;
  }
  .header-title {
    font-size: 22px;
  }
  .step-info {
    display: none;
  }
  .connector-line {
    width: 32px;
  }
  .step-connector {
    padding: 0 8px;
  }
  .two-col {
    grid-template-columns: 1fr;
  }
  .form-card-header {
    padding: 16px;
  }
  .form-body {
    padding: 16px;
  }
  .form-footer {
    flex-direction: column-reverse;
    gap: 10px;
  }
  .btn-submit {
    width: 100%;
  }
  .btn-back {
    width: 100%;
    text-align: center;
  }
}
</style>
