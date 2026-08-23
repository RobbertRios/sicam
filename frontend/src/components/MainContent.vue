<template>
  <main class="content">
    <header class="page-header">
      <div class="header-left">
        <h2 class="page-title">Resultados del Análisis</h2>
        <div class="breadcrumb">
          <span v-if="patientId" class="breadcrumb-item">
            <svg
              class="breadcrumb-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            {{ patientName || "Paciente " + patientId }}
          </span>

          <span v-if="caseId" class="breadcrumb-separator">›</span>

          <span v-if="caseId" class="breadcrumb-item active">
            <svg
              class="breadcrumb-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"
              ></path>
              <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
            </svg>
            Caso {{ caseId }}
          </span>

          <span v-if="!patientId" class="breadcrumb-placeholder">
            Seleccione un paciente y un caso para comenzar
          </span>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn-action csv" @click="exportarCSV">
          <span class="btn-icon">⬇</span>
          Exportar CSV
        </button>
        <button class="btn-action pdf" @click="generarPDF" :disabled="isGeneratingPDF">
          <span class="btn-icon">📄</span>
          {{ isGeneratingPDF ? `Generando... ${Math.round(pdfProgress)}%` : "Generar PDF" }}
        </button>
      </div>
    </header>

    <div class="layout-grid">
      <div class="gallery-column">
        <div class="gallery-header">
          <h3>Galería</h3>
          <span class="gallery-count">{{ totalImagenes }}</span>
        </div>

        <div class="gallery-section">
          <div class="gallery-toggle" @click="mostrarSegmentadas = !mostrarSegmentadas">
            <h4>Segmentadas</h4>
            <span class="section-count">
              {{ imagenesSegmentadas.length }}
            </span>
          </div>

          <div v-show="mostrarSegmentadas" class="gallery-grid">
            <div
              v-for="muestra in imagenesSegmentadas"
              :key="'seg-' + muestra.id_muestra"
              class="thumb"
              :class="{
                active: imagenSeleccionada && muestra.id_muestra === imagenSeleccionada.id_muestra,
                'needs-review': muestra.analisis_full?.requiere_revision_manual,
              }"
              @click="imagenSeleccionada = muestra"
            >
              <img :src="muestra.imagen_thumbnail" loading="lazy" />

              <div class="thumb-overlay">
                <span class="thumb-id">#{{ muestra.id_muestra }}</span>
              </div>

              <span
                class="tipo-chip"
                :class="'tipo-' + muestra.tipo"
                v-html="getIconoTipoMuestra(muestra.tipo)"
              ></span>

              <div
                v-if="muestra.analisis_full?.requiere_revision_manual"
                class="review-indicator"
                title="Requiere revisión manual"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="3"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path
                    d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                  ></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>

              <button
                class="btn-delete-thumb"
                title="Eliminar imagen"
                @click.stop="confirmarEliminar(muestra)"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path
                    d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="gallery-section">
          <div class="gallery-toggle" @click="mostrarNoSegmentadas = !mostrarNoSegmentadas">
            <h4>No segmentadas</h4>
            <span class="section-count original">
              {{ imagenesNoSegmentadas.length }}
            </span>
          </div>

          <div v-show="mostrarNoSegmentadas" class="gallery-grid">
            <div
              v-for="muestra in imagenesNoSegmentadas"
              :key="'no-' + muestra.id_muestra"
              class="thumb"
              :class="{
                active: imagenSeleccionada && muestra.id_muestra === imagenSeleccionada.id_muestra,
              }"
              @click="imagenSeleccionada = muestra"
            >
              <img :src="muestra.imagen_thumbnail" loading="lazy" />
              <div class="thumb-overlay">
                <span class="thumb-id">#{{ muestra.id_muestra }}</span>
              </div>
              <span
                class="tipo-chip"
                :class="'tipo-' + muestra.tipo"
                v-html="getIconoTipoMuestra(muestra.tipo)"
              ></span>
              <button
                class="btn-delete-thumb"
                title="Eliminar imagen"
                @click.stop="confirmarEliminar(muestra)"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path
                    d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="muestraAEliminar" class="modal-overlay" @click.self="muestraAEliminar = null">
        <div class="modal-content">
          <div class="modal-icon warning">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
              ></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </div>
          <h3>Eliminar Muestra</h3>
          <p>
            ¿Estás seguro de que deseas eliminar la
            <strong>Muestra #{{ muestraAEliminar.id_muestra }}</strong
            >? <br />Se borrará la imagen original y todos sus análisis. Esta acción no se puede
            deshacer.
          </p>
          <div class="modal-actions">
            <button class="btn-cancelar" @click="muestraAEliminar = null">Cancelar</button>
            <button class="btn-confirmar-eliminar" @click="ejecutarEliminar" :disabled="loading">
              {{ loading ? "Eliminando..." : "Sí, eliminar" }}
            </button>
          </div>
        </div>
      </div>

      <div class="viewer-column">
        <div class="card main-card">
          <div class="card-body split-view">
            <div class="image-container">
              <div class="img-placeholder">
                <img
                  v-if="imagenSeleccionada"
                  :src="imagenSeleccionada.imagen_original"
                  class="main-image clickable"
                  alt="Muestra microscópica"
                  @click="imagenEnEdicion = true"
                />

                <img
                  v-if="
                    imagenSeleccionada &&
                    verMascara &&
                    imagenSeleccionada.id_analisis &&
                    mascaraBlobUrl
                  "
                  :key="`mask-${imagenSeleccionada.id_analisis}-${mascaraActual}-${mascaraTimestamp}`"
                  :src="mascaraBlobUrl"
                  class="mask-overlay"
                  alt="Máscaras"
                />

                <div v-if="!imagenSeleccionada" class="empty-image-state">
                  <div class="empty-image-icon">🔬</div>
                  <p>Seleccione una imagen de la galería</p>
                </div>

                <div v-if="imagenSeleccionada" class="img-overlay">
                  <button
                    v-if="imagenSeleccionada.id_analisis"
                    class="seg-toggle"
                    :class="{ active: verMascara }"
                    @click="toggleTodasMascaras"
                    :title="verMascara ? 'Ocultar segmentación' : 'Ver segmentación'"
                  >
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path
                        v-if="verMascara"
                        d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24M1 1l22 22"
                      />
                      <template v-else>
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                        <circle cx="12" cy="12" r="3" />
                      </template>
                    </svg>
                    <span>{{ verMascara ? "Ocultar" : "Segmentación" }}</span>
                  </button>
                  <span v-else class="no-seg-badge">Sin segmentar</span>
                </div>
              </div>
            </div>

            <div class="data-container">
              <div class="card-header">
                <div class="card-title-section">
                  <h3>
                    {{
                      imagenSeleccionada
                        ? "Muestra #" + imagenSeleccionada.id_muestra
                        : "Vista previa"
                    }}
                  </h3>

                  <span
                    v-if="imagenSeleccionada"
                    class="tipo-badge-header"
                    :class="'tipo-badge-' + imagenSeleccionada.tipo"
                  >
                    <span
                      class="tipo-icon-wrapper"
                      v-html="getIconoTipoMuestra(imagenSeleccionada.tipo)"
                    ></span>
                    {{ imagenSeleccionada.tipo === "sangre" ? "Sangre" : "Saliva" }}
                  </span>
                </div>

                <div class="card-tools layer-toggles">
                  <button
                    class="layer-icon-btn"
                    :class="{ active: verMascara && mascaraActual === 'overlay' }"
                    @click="verMascaraSola('overlay')"
                    title="Ver todas las capas"
                  >
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </button>

                  <button
                    class="layer-icon-btn btn-membrana"
                    :class="{ active: verMascara && mascaraActual === 'membrana' }"
                    @click="verMascaraSola('membrana')"
                    title="Ver Membranas"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <circle cx="12" cy="12" r="8" stroke-dasharray="4 4" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  </button>

                  <button
                    class="layer-icon-btn btn-nucleo"
                    :class="{ active: verMascara && mascaraActual === 'nucleo' }"
                    :disabled="imagenSeleccionada?.tipo === 'sangre'"
                    @click="verMascaraSola('nucleo')"
                    :title="
                      imagenSeleccionada?.tipo === 'sangre'
                        ? 'Las células de sangre no tienen núcleo'
                        : 'Ver Núcleos'
                    "
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <circle cx="12" cy="12" r="8" />
                      <circle cx="12" cy="12" r="3" fill="currentColor" stroke="none" />
                    </svg>
                  </button>

                  <button
                    class="layer-icon-btn btn-micronucleo"
                    :class="{ active: verMascara && mascaraActual === 'micronucleo' }"
                    @click="verMascaraSola('micronucleo')"
                    title="Ver Micronúcleos"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <circle cx="12" cy="12" r="5" />
                      <circle cx="12" cy="12" r="2" fill="currentColor" stroke="none" />
                    </svg>
                  </button>
                </div>
              </div>

              <div class="data-header">
                <h4>Resumen de Conteo</h4>
              </div>

              <table class="data-table">
                <thead>
                  <tr>
                    <th>Estructura</th>
                    <th>Cantidad</th>
                  </tr>
                </thead>

                <tbody v-if="resultadoImagenSeleccionada">
                  <tr class="data-row nucleos">
                    <td>
                      <div class="structure-cell">
                        <svg
                          class="table-icon"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="#1e88e5"
                          stroke-width="2"
                        >
                          <circle cx="12" cy="12" r="8" />
                          <circle cx="12" cy="12" r="3" fill="#1e88e5" stroke="none" />
                        </svg>
                        <span>Núcleos</span>
                      </div>
                    </td>
                    <td class="count">{{ resultadoImagenSeleccionada.nucleos }}</td>
                  </tr>
                  <tr class="data-row membranas">
                    <td>
                      <div class="structure-cell">
                        <svg
                          class="table-icon"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="#4caf50"
                          stroke-width="2"
                        >
                          <circle cx="12" cy="12" r="7" stroke-dasharray="3 3" />
                          <circle cx="12" cy="12" r="3" />
                        </svg>
                        <span>Membranas</span>
                      </div>
                    </td>
                    <td class="count">{{ resultadoImagenSeleccionada.membranas }}</td>
                  </tr>
                  <tr class="data-row micronucleos highlight">
                    <td>
                      <div class="structure-cell">
                        <svg
                          class="table-icon"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="#ab47bc"
                          stroke-width="2"
                        >
                          <circle cx="12" cy="12" r="6" />
                          <circle cx="12" cy="12" r="2" fill="#ab47bc" stroke="none" />
                        </svg>
                        <span>Micronúcleos</span>
                      </div>
                    </td>
                    <td class="count critical">{{ resultadoImagenSeleccionada.micronucleos }}</td>
                  </tr>
                </tbody>

                <tbody v-else>
                  <tr>
                    <td colspan="2" class="no-data">
                      <div class="no-data-icon">📊</div>
                      <span>Sin resultados disponibles</span>
                    </td>
                  </tr>
                </tbody>
              </table>

              <button
                v-if="imagenSeleccionada && imagenSeleccionada.analisis_full"
                class="btn-review full-width"
                :class="{ marcado: requiereRevision }"
                @click="toggleRevisionManual"
                :disabled="loadingRevision"
              >
                <svg
                  class="btn-icon-svg"
                  viewBox="0 0 24 24"
                  :fill="requiereRevision ? 'currentColor' : 'none'"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
                  <line x1="4" y1="22" x2="4" y2="15"></line>
                </svg>

                <span>
                  {{
                    requiereRevision
                      ? "Revisión manual pendiente (Quitar)"
                      : "Marcar para revisión manual"
                  }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <div v-if="imagenEnEdicion" class="image-editor-overlay" @click.self="cerrarEditor">
    <div class="editor-container">
      <button class="close-btn" @click="cerrarEditor">✖</button>

      <transition name="toast-fade">
        <div v-if="toast.visible" class="editor-toast" :class="toast.tipo">
          <svg
            v-if="toast.tipo === 'exito'"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span>{{ toast.mensaje }}</span>
        </div>
      </transition>

      <div class="editor-layout">
        <!-- PANEL LATERAL -->
        <div class="editor-sidebar">
          <!-- SEPARADOR: VISIBILIDAD DE MASCARAS -->
          <div class="editor-section-label">Visibilidad</div>

          <button
            class="tool-option"
            :class="{
              'active overlay-active': editorVerMascara && editorMascaraActual === 'overlay',
            }"
            @click="editorToggleMascara('overlay')"
            :title="
              editorVerMascara && editorMascaraActual === 'overlay' ? 'Ocultar todas' : 'Ver todas'
            "
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#90caf9"
              stroke-width="1.5"
            >
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <span>Todas</span>
          </button>

          <button
            class="tool-option"
            :class="{
              'active membrana-active': editorVerMascara && editorMascaraActual === 'membrana',
            }"
            @click="editorToggleMascara('membrana')"
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#4caf50"
              stroke-width="1.5"
            >
              <path
                d="M4 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8-8-3.582-8-8z"
                stroke-dasharray="3 3"
              />
              <circle cx="12" cy="12" r="5" stroke="#4caf50" />
            </svg>
            <span>Membrana</span>
          </button>

          <button
            class="tool-option"
            :class="{
              'active nucleo-active': editorVerMascara && editorMascaraActual === 'nucleo',
            }"
            :disabled="imagenSeleccionada?.tipo === 'sangre'"
            @click="editorToggleMascara('nucleo')"
            :title="
              imagenSeleccionada?.tipo === 'sangre'
                ? 'Las células de sangre no tienen núcleo'
                : 'Ver capa de núcleos'
            "
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#64b5f6"
              stroke-width="1.5"
            >
              <circle cx="12" cy="12" r="8" />
              <circle cx="12" cy="12" r="3" fill="#1e88e5" stroke="none" />
            </svg>
            <span>Núcleo</span>
          </button>

          <button
            class="tool-option"
            :class="{
              'active micronucleo-active':
                editorVerMascara && editorMascaraActual === 'micronucleo',
            }"
            @click="editorToggleMascara('micronucleo')"
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#ba68c8"
              stroke-width="1.5"
            >
              <circle cx="12" cy="12" r="5" />
              <circle cx="12" cy="12" r="1.5" fill="#8e24aa" stroke="none" />
            </svg>
            <span>Micronúcleo</span>
          </button>

          <!-- SEPARADOR: INFO -->
          <div class="editor-section-label" style="margin-top: 8px">Info</div>
          <div class="editor-info" v-if="resultadoImagenSeleccionada">
            <div class="editor-info-row nucleo-color">
              <span class="editor-dot" style="background: #00dc00"></span>
              <span>{{ resultadoImagenSeleccionada.nucleos }} núcleos</span>
            </div>
            <div class="editor-info-row micronucleo-color">
              <span class="editor-dot" style="background: #ff0000"></span>
              <span>{{ resultadoImagenSeleccionada.micronucleos }} micronúcleos</span>
            </div>
            <div class="editor-info-row membrana-color">
              <span class="editor-dot" style="background: #0078ff"></span>
              <span>{{ resultadoImagenSeleccionada.membranas }} membranas</span>
            </div>
          </div>
          <div class="editor-info" v-else>
            <span class="editor-no-data">Sin análisis</span>
          </div>
        </div>

        <!-- IMAGEN + MASCARA + FLECHAS -->
        <div ref="editorWrapper" class="editor-image-wrapper" @wheel.prevent="onWheelZoom">
          <div
            class="editor-transform-group"
            :style="{
              transform: `translate(${offsetX}px, ${offsetY}px) scale(${zoom})`,
              cursor: cursorActual,
            }"
            @mousedown.prevent.stop="startDrag"
            @mousemove.prevent.stop="onDrag"
            @mouseup.prevent.stop="endDrag"
            @mouseleave="endDrag"
          >
            <img
              ref="editorImage"
              :src="imagenSeleccionada.imagen_original"
              class="editor-image"
              alt="Imagen en edición"
              @load="inicializarCanvas"
              @dblclick.stop="onCanvasDoubleClick"
            />

            <canvas
              ref="editorCanvas"
              class="editor-canvas"
              @mousedown="onCanvasMouseDown"
              @mousemove="onCanvasMouseMove"
              @mouseup="onCanvasMouseUp"
              @dblclick.stop="onCanvasDoubleClick"
            ></canvas>
          </div>

          <!-- FLECHAS -->
          <button
            class="nav-arrow left"
            @click.stop="imagenAnterior"
            :disabled="indiceImagenSeleccionada <= 0"
          >
            ‹
          </button>

          <button
            class="nav-arrow right"
            @click.stop="siguienteImagen"
            :disabled="indiceImagenSeleccionada >= imagenes.length - 1"
          >
            ›
          </button>

          <!-- ZOOM INDICATOR -->
          <div v-if="zoom > 1" class="zoom-indicator">{{ Math.round(zoom * 100) }}%</div>
        </div>
        <!-- PANEL DERECHO - EDICIÓN -->
        <div class="editor-sidebar editor-sidebar-right">
          <div class="editor-section-label">Edición</div>

          <!-- Edición Activa / Inactiva -->
          <button
            class="tool-option"
            :class="{ 'active modo-edicion-active': edicionActiva }"
            @click="edicionActiva = !edicionActiva"
          >
            <svg
              v-if="edicionActiva"
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 9.9-1"></path>
            </svg>

            <svg
              v-else
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>

            <span>{{ edicionActiva ? "Edición Activa" : "Edición Inactiva" }}</span>
          </button>

          <!-- Agregar Membrana -->
          <button
            class="tool-option"
            :class="{
              'active membrana-active': herramientaActiva === 'agregar-membrana' && edicionActiva,
            }"
            :disabled="!edicionActiva"
            @click="
              herramientaActiva =
                herramientaActiva === 'agregar-membrana' ? null : 'agregar-membrana'
            "
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#4caf50"
              stroke-width="1.5"
            >
              <path
                d="M4 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8-8-3.582-8-8z"
                stroke-dasharray="3 3"
              />
              <circle cx="12" cy="12" r="5" stroke="#4caf50" />
            </svg>
            <span>Agregar Membrana</span>
          </button>

          <!-- Agregar Núcleo -->
          <button
            class="tool-option"
            :class="{
              'active nucleo-active': herramientaActiva === 'agregar-nucleo' && edicionActiva,
            }"
            :disabled="!edicionActiva || imagenSeleccionada?.tipo === 'sangre'"
            @click="
              herramientaActiva = herramientaActiva === 'agregar-nucleo' ? null : 'agregar-nucleo'
            "
            :title="
              imagenSeleccionada?.tipo === 'sangre'
                ? 'Las células de sangre no tienen núcleo'
                : 'Agregar Núcleo'
            "
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#64b5f6"
              stroke-width="1.5"
            >
              <circle cx="12" cy="12" r="8" />
              <circle cx="12" cy="12" r="3" fill="#1e88e5" stroke="none" />
            </svg>
            <span>Agregar Núcleo</span>
          </button>

          <!-- Agregar Micronúcleo -->
          <button
            class="tool-option"
            :class="{
              'active micronucleo-active':
                herramientaActiva === 'agregar-micronucleo' && edicionActiva,
            }"
            :disabled="!edicionActiva"
            @click="
              herramientaActiva =
                herramientaActiva === 'agregar-micronucleo' ? null : 'agregar-micronucleo'
            "
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#ba68c8"
              stroke-width="1.5"
            >
              <circle cx="12" cy="12" r="5" />
              <circle cx="12" cy="12" r="1.5" fill="#8e24aa" stroke="none" />
            </svg>
            <span>Agregar Micronúcleo</span>
          </button>

          <!-- Borrar -->
          <button
            class="tool-option danger"
            :class="{ 'active borrar-active': herramientaActiva === 'borrar' && edicionActiva }"
            :disabled="!edicionActiva"
            @click="herramientaActiva = herramientaActiva === 'borrar' ? null : 'borrar'"
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#e0e0e0"
              stroke-width="1.5"
            >
              <path d="M2.5 13.5l6-6a2.828 2.828 0 014 0l7 7a2.828 2.828 0 010 4h-11l-6-5z" />
              <path d="M12.5 10.5l-6 6" />
            </svg>
            <span>Borrar</span>
          </button>

          <!-- Editar -->
          <button
            class="tool-option"
            :class="{ 'active editar-active': herramientaActiva === 'editar' && edicionActiva }"
            :disabled="!edicionActiva"
            @click="herramientaActiva = herramientaActiva === 'editar' ? null : 'editar'"
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#b388ff"
              stroke-width="1.5"
            >
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
            </svg>
            <span>Editar</span>
          </button>

          <div style="display: flex; gap: 10px; width: 100%; margin-top: auto; margin-bottom: 10px">
            <button
              class="tool-option"
              style="flex: 1; padding: 10px 0; justify-content: center"
              :disabled="!puedeDeshacer"
              @click="deshacer"
              title="Deshacer"
            >
              <svg
                class="elegant-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                style="width: 20px; height: 20px"
              >
                <path d="M3 10h10a5 5 0 0 1 5 5v2"></path>
                <polyline points="7 6 3 10 7 14"></polyline>
              </svg>
            </button>
            <button
              class="tool-option"
              style="flex: 1; padding: 10px 0; justify-content: center"
              :disabled="!puedeRehacer"
              @click="rehacer"
              title="Rehacer"
            >
              <svg
                class="elegant-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                style="width: 20px; height: 20px"
              >
                <path d="M21 10H11a5 5 0 0 0-5 5v2"></path>
                <polyline points="17 6 21 10 17 14"></polyline>
              </svg>
            </button>
          </div>

          <button
            class="tool-option btn-guardar-edicion"
            :disabled="!edicionActiva"
            @click="guardarCambiosEdicion"
          >
            <svg
              class="elegant-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17 21 17 13 7 13 7 21"></polyline>
              <polyline points="7 3 7 8 15 8"></polyline>
            </svg>
            <span>Guardar Cambios</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="pdf-offscreen-container">
    <div id="plantilla-pdf-main" class="pdf-document">
      <div v-for="img in imagenesConAnalisis" :key="'pdf-' + img.id_muestra" class="pdf-page">
        <div class="pdf-header">
          <h2>SICAM - Reporte de Segmentación</h2>
          <p>
            <strong>{{ patientName || "Paciente " + patientId }}</strong> | Caso ID: {{ caseId }} |
            Muestra: #{{ img.id_muestra }} ({{ img.tipo === "sangre" ? "Sangre" : "Saliva" }})
          </p>
          <hr />
        </div>

        <div class="pdf-image-wrapper">
          <img :src="img.imagen_original" class="pdf-base-img" crossorigin="anonymous" />

          <img
            v-if="pdfMaskBlobs[img.id_analisis]"
            :src="pdfMaskBlobs[img.id_analisis]"
            class="pdf-mask-img"
          />
        </div>

        <div class="pdf-table-container">
          <h4>Conteo de la Muestra</h4>
          <table class="pdf-table">
            <thead>
              <tr>
                <th>Estructura</th>
                <th>Cantidad Detectada</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Núcleos</td>
                <td>{{ conteoPorImagen(img).nucleos }}</td>
              </tr>
              <tr>
                <td>Membranas</td>
                <td>{{ conteoPorImagen(img).membranas }}</td>
              </tr>
              <tr
                :style="
                  conteoPorImagen(img).micronucleos > 0
                    ? 'background-color: #fffbeb; color: #b45309; font-weight: bold;'
                    : ''
                "
              >
                <td>Micronúcleos</td>
                <td>{{ conteoPorImagen(img).micronucleos }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios.js";
import html2pdf from "html2pdf.js";

export default {
  name: "MainContent",

  props: {
    patientId: [String, Number],
    patientName: String,
    caseId: [String, Number],
    refreshKey: { type: Number, default: 0 },
  },

  emits: ["edicion-guardada"],

  data() {
    return {
      API_URL: "/api",
      BASE_MEDIA_URL: "",

      analisis: [],
      loading: false,
      imagenSeleccionada: null,
      imagenEnEdicion: false,
      verMascara: false,

      // Blob URL de la máscara activa
      mascaraBlobUrl: null,

      // Estado de mascara en el editor
      editorVerMascara: false,
      editorMascaraActual: "overlay",

      // Estado del editor
      edicionActiva: false,

      // Control de máscaras
      mascarasVisibles: {
        nucleo: true,
        micronucleo: true,
        membrana: true,
      },
      mascaraActual: "overlay",
      mascaraTimestamp: Date.now(),

      // Variables del PDF
      isGeneratingPDF: false,
      pdfProgress: 100,
      pdfMaskBlobs: {},

      loadingRevision: false,

      // Zoom y navegación
      zoom: 1,
      zoomMin: 1,
      zoomMax: 4,
      zoomStep: 0.15,
      offsetX: 0,
      offsetY: 0,

      isDragging: false,
      startX: 0,
      startY: 0,

      herramientaActiva: "editar",

      // Galeria
      muestras: [],
      mostrarSegmentadas: true,
      mostrarNoSegmentadas: true,

      // Edicion
      modoAgregar: null,
      modoAjustar: false,

      poligonos: {
        membranas: [],
        nucleos: [],
        micronucleos: [],
      },

      poligonoSeleccionado: null,
      poligonoTemporal: [],
      dibujando: false,
      verticeSeleccionado: null,

      // Historial para Deshacer/Rehacer
      historial: [],
      historialIndex: -1,

      // Toast
      toast: { visible: false, mensaje: "", tipo: "exito" },

      // Para el Modal de Eliminar
      muestraAEliminar: null,
    };
  },

  computed: {
    imagenes() {
      return this.analisis.map((a) => {
        return {
          id_muestra: a.id_muestra_fk.id_muestra,
          id_analisis: a.id_analisis,

          imagen_thumbnail: `${this.BASE_MEDIA_URL}${a.id_muestra_fk.thumbnail}`,
          imagen_original: `${this.BASE_MEDIA_URL}${a.id_muestra_fk.ruta_imagen}`,

          tipo: a.id_muestra_fk.tipo_muestra,
          fecha: a.id_muestra_fk.fecha_toma,
          analisis_full: a,
        };
      });
    },

    imagenesSegmentadas() {
      return this.imagenes;
    },

    imagenesNoSegmentadas() {
      const idsAnalizados = this.analisis.map((a) => a.id_muestra_fk.id_muestra);

      return this.muestras
        .filter((m) => !idsAnalizados.includes(m.id_muestra))
        .map((m) => ({
          id_muestra: m.id_muestra,
          id_analisis: null,
          imagen_thumbnail: `${this.BASE_MEDIA_URL}${m.thumbnail}`,
          imagen_original: `${this.BASE_MEDIA_URL}${m.ruta_imagen}`,
          tipo: m.tipo_muestra,
          fecha: m.fecha_toma,
          analisis_full: null,
        }));
    },

    totalImagenes() {
      return this.imagenesSegmentadas.length + this.imagenesNoSegmentadas.length;
    },

    imagenesConAnalisis() {
      return this.imagenes.filter(
        (img) => img.analisis_full && img.analisis_full.estado === "listo",
      );
    },

    requiereRevision() {
      return this.imagenSeleccionada?.analisis_full?.requiere_revision_manual || false;
    },

    resultadoImagenSeleccionada() {
      const analisis = this.imagenSeleccionada?.analisis_full;
      if (!analisis) return null;

      // Prioridad 1: resultados tipados del modelo AnalisisResultados
      if (analisis.resultados) {
        return {
          nucleos: analisis.resultados.total_nucleos,
          membranas: analisis.resultados.total_membranas,
          micronucleos: analisis.resultados.total_micronucleos,
        };
      }

      // Prioridad 2: contenido_json del archivo activo (fallback)
      const archivoActivo = analisis.archivos?.find((a) => a.activo);
      if (!archivoActivo?.contenido_json) return null;

      const json = archivoActivo.contenido_json;
      const objetos = json.objetos ?? [];

      return {
        nucleos: objetos.filter((o) => o.tipo === "nucleo").length,
        membranas: objetos.filter((o) => o.tipo === "membrana").length,
        micronucleos: objetos.filter((o) => o.tipo === "micronucleo").length,
      };
    },

    indiceImagenSeleccionada() {
      if (!this.imagenSeleccionada) return -1;
      return this.imagenes.findIndex((i) => i.id_muestra === this.imagenSeleccionada.id_muestra);
    },

    cursorActual() {
      if (this.edicionActiva && this.herramientaActiva) {
        return "crosshair";
      }
      return this.zoom > 1 ? (this.isDragging ? "grabbing" : "grab") : "zoom-in";
    },

    puedeDeshacer() {
      return this.historialIndex > 0;
    },

    puedeRehacer() {
      return this.historialIndex < this.historial.length - 1;
    },
  },

  watch: {
    refreshKey(newVal, oldVal) {
      if (newVal !== oldVal && this.caseId) {
        this.recargarDatosCaso(this.caseId, false);
      }
    },

    imagenSeleccionada(nueva) {
      if (!nueva || !nueva.id_analisis) {
        this.verMascara = false;
      }
      this.mascarasVisibles = { nucleo: true, micronucleo: true, membrana: true };
      this.mascaraActual = "overlay";
      this.mascaraTimestamp = Date.now();
      this.liberarBlobMascara();
    },

    verMascara(activa) {
      if (activa && this.imagenSeleccionada?.id_analisis) {
        this.cargarMascaraConToken();
      } else {
        this.liberarBlobMascara();
      }
    },

    mascaraActual() {
      if (this.verMascara && this.imagenSeleccionada?.id_analisis) {
        this.cargarMascaraConToken();
      }
    },

    mascaraTimestamp() {
      if (this.verMascara && this.imagenSeleccionada?.id_analisis) {
        this.cargarMascaraConToken();
      }
    },

    imagenEnEdicion(nuevo) {
      if (nuevo) {
        this.editorVerMascara = true;
        this.editorMascaraActual = "overlay";

        this.$nextTick(() => {
          this.inicializarCanvas();
        });
      }
    },

    edicionActiva() {
      this.$nextTick(() => {
        this.redibujarCanvas();
      });
    },

    herramientaActiva(nueva, vieja) {
      if (vieja === "editar" && this.modoAjustar) {
        this.guardarAjusteTemporal();
      }

      this.modoAjustar = false;
      this.poligonoSeleccionado = null;
      this.verticeSeleccionado = null;
      this.dibujando = false;

      if (!nueva || !nueva.startsWith("agregar")) {
        this.poligonoTemporal = [];
      }

      this.redibujarCanvas();
    },

    caseId: {
      immediate: true,
      async handler(id) {
        Object.values(this.pdfMaskBlobs || {}).forEach((url) => URL.revokeObjectURL(url));
        this.pdfMaskBlobs = {};
        if (!id) {
          this.analisis = [];
          this.muestras = [];
          this.imagenSeleccionada = null;
          this.verMascara = false;
          return;
        }
        await this.recargarDatosCaso(id, true);
      },
    },
  },

  mounted() {
    window.addEventListener("keydown", this.teclasOverlay);
  },

  beforeUnmount() {
    window.removeEventListener("keydown", this.teclasOverlay);
    this.liberarBlobMascara();
  },

  methods: {
    getIconoTipoMuestra(tipo) {
      if (tipo === "sangre") {
        return `<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" stroke="none" style="display: block;"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>`;
      }
      if (tipo === "saliva") {
        return `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display: block;"><path d="M14.5 2v17.5c0 1.4-1.1 2.5-2.5 2.5h0c-1.4 0-2.5-1.1-2.5-2.5V2"/><path d="M8.5 2h7"/><path d="M14.5 16h-5"/></svg>`;
      }
      return "";
    },

    exportarCSV() {
      if (!this.imagenes || this.imagenes.length === 0) {
        this.mostrarToast("No hay imágenes analizadas para exportar.", "error");
        return;
      }

      // 1. Agregamos Paciente y Caso a los encabezados
      const headers = [
        "Paciente ID",
        "Caso ID",
        "Muestra ID",
        "Tipo",
        "Membranas",
        "Núcleos",
        "Micronúcleos",
      ];

      const rows = this.imagenes.map((img) => {
        let membranas = 0,
          nucleos = 0,
          micronucleos = 0;
        const analisis = img.analisis_full;

        if (analisis) {
          if (analisis.resultados) {
            membranas = analisis.resultados.total_membranas || 0;
            nucleos = analisis.resultados.total_nucleos || 0;
            micronucleos = analisis.resultados.total_micronucleos || 0;
          } else {
            const archivoActivo = analisis.archivos?.find((a) => a.activo);
            if (archivoActivo?.contenido_json?.objetos) {
              const objetos = archivoActivo.contenido_json.objetos;
              membranas = objetos.filter((o) => o.tipo === "membrana").length;
              nucleos = objetos.filter((o) => o.tipo === "nucleo").length;
              micronucleos = objetos.filter((o) => o.tipo === "micronucleo").length;
            }
          }
        }

        const tipoTexto = img.tipo === "sangre" ? "Sangre" : "Saliva";

        // 2. Metemos this.patientId y this.caseId al inicio de cada fila
        return [
          this.patientId,
          this.caseId,
          img.id_muestra,
          tipoTexto,
          membranas,
          nucleos,
          micronucleos,
        ].join(",");
      });

      const csvContent = [headers.join(","), ...rows].join("\n");
      const blob = new Blob(["\uFEFF" + csvContent], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.setAttribute("href", url);
      // 3. Mejoramos el nombre del archivo para que incluya los IDs
      const nombreDescarga = this.patientName
        ? this.patientName.replace(/ /g, "_")
        : `Paciente_${this.patientId}`;
      link.setAttribute("download", `SICAM_${nombreDescarga}_Caso_${this.caseId}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      this.mostrarToast("CSV descargado con éxito", "exito");
    },

    // Extrae los datos exactos de 1 imagen para el PDF
    conteoPorImagen(img) {
      let membranas = 0,
        nucleos = 0,
        micronucleos = 0;
      const analisis = img.analisis_full;
      if (analisis) {
        if (analisis.resultados) {
          membranas = analisis.resultados.total_membranas || 0;
          nucleos = analisis.resultados.total_nucleos || 0;
          micronucleos = analisis.resultados.total_micronucleos || 0;
        } else {
          const archivoActivo = analisis.archivos?.find((a) => a.activo);
          if (archivoActivo?.contenido_json?.objetos) {
            const objetos = archivoActivo.contenido_json.objetos;
            membranas = objetos.filter((o) => o.tipo === "membrana").length;
            nucleos = objetos.filter((o) => o.tipo === "nucleo").length;
            micronucleos = objetos.filter((o) => o.tipo === "micronucleo").length;
          }
        }
      }
      return { membranas, nucleos, micronucleos };
    },

    // Genera y descarga el PDF
    async generarPDF() {
      if (this.imagenesConAnalisis.length === 0) {
        this.mostrarToast("No hay imágenes segmentadas para generar el reporte.", "error");
        return;
      }

      this.isGeneratingPDF = true;
      this.pdfProgress = 5;

      try {
        // 1. Descargar las máscaras usando Axios (para que pasen la seguridad)
        for (let i = 0; i < this.imagenesConAnalisis.length; i++) {
          const img = this.imagenesConAnalisis[i];
          if (!this.pdfMaskBlobs[img.id_analisis]) {
            const res = await axios.get(`${this.API_URL}/mascaras/${img.id_analisis}/overlay/`, {
              responseType: "blob",
            });
            this.pdfMaskBlobs[img.id_analisis] = URL.createObjectURL(res.data);
          }
          // Subir la barra de progreso mientras descarga
          this.pdfProgress = 5 + Math.round(((i + 1) / this.imagenesConAnalisis.length) * 40);
        }

        // 2. Esperar a que Vue actualice el HTML y las imágenes carguen
        await this.$nextTick();
        await new Promise((r) => setTimeout(r, 800)); // Pausa vital para que renderice el DOM

        // 3. Simular el resto del progreso mientras html2pdf hace su trabajo pesado
        const interval = setInterval(() => {
          if (this.pdfProgress < 90) this.pdfProgress += Math.random() * 15;
        }, 400);

        // 4. Construir y guardar el documento
        const element = document.getElementById("plantilla-pdf-main");
        const opt = {
          margin: 10,
          filename: `SICAM_Reporte_${this.patientName ? this.patientName.replace(/ /g, "_") : "Paciente_" + this.patientId}_Caso_${this.caseId}.pdf`,
          image: { type: "jpeg", quality: 0.98 },
          html2canvas: { scale: 2, useCORS: true, letterRendering: true },
          jsPDF: { unit: "mm", format: "letter", orientation: "portrait" },
        };

        await html2pdf().set(opt).from(element).save();

        clearInterval(interval);
        this.pdfProgress = 100;
        this.mostrarToast("PDF generado con éxito", "exito");
      } catch (error) {
        console.error("Error generando PDF:", error);
        this.mostrarToast("Hubo un error al generar el PDF.", "error");
        this.pdfProgress = 100;
      } finally {
        setTimeout(() => {
          this.isGeneratingPDF = false;
        }, 800);
      }
    },

    async toggleRevisionManual() {
      if (!this.imagenSeleccionada?.analisis_full) return;

      this.loadingRevision = true;
      const nuevoEstado = !this.requiereRevision;
      const idAnalisis = this.imagenSeleccionada.analisis_full.id_analisis;

      try {
        // Hacemos un PATCH a tu API para actualizar solo ese campo
        await axios.patch(`${this.API_URL}/analisis/${idAnalisis}/`, {
          requiere_revision_manual: nuevoEstado,
        });

        // Actualizamos el dato localmente en Vue para que el botón cambie al instante
        this.imagenSeleccionada.analisis_full.requiere_revision_manual = nuevoEstado;

        this.mostrarToast(
          nuevoEstado ? "Imagen marcada para revisión" : "Marca de revisión eliminada",
          "exito",
        );
      } catch (error) {
        console.error("Error al actualizar estado de revisión:", error);
        this.mostrarToast("Error al conectar con el servidor", "error");
      } finally {
        this.loadingRevision = false;
      }
    },

    // ============================================================
    // CARGA / RECARGA DE DATOS DEL CASO
    // ============================================================
    async recargarDatosCaso(id, resetImg = false) {
      this.loading = true;
      const idMuestraActual = this.imagenSeleccionada?.id_muestra ?? null;
      try {
        const [resAnalisis, resMuestras] = await Promise.all([
          axios.get(`${this.API_URL}/casos/${id}/analisis/`),
          axios.get(`${this.API_URL}/casos/${id}/muestras/`),
        ]);
        this.analisis = resAnalisis.data;
        this.muestras = resMuestras.data;
        if (resetImg || !idMuestraActual) {
          this.imagenSeleccionada =
            this.imagenesSegmentadas[0] ?? this.imagenesNoSegmentadas[0] ?? null;
        } else {
          const todas = [...this.imagenesSegmentadas, ...this.imagenesNoSegmentadas];
          const restaurada = todas.find((i) => i.id_muestra === idMuestraActual);
          this.imagenSeleccionada =
            restaurada ?? this.imagenesSegmentadas[0] ?? this.imagenesNoSegmentadas[0] ?? null;
        }
      } catch (e) {
        console.error("Error cargando datos del caso:", e);
      } finally {
        this.loading = false;
      }
    },

    // ============================================================
    // ELIMINAR MUESTRA (MODAL)
    // ============================================================
    confirmarEliminar(muestra) {
      this.muestraAEliminar = muestra;
    },

    async ejecutarEliminar() {
      if (!this.muestraAEliminar) return;

      this.loading = true;
      try {
        await axios.delete(`${this.API_URL}/muestras/${this.muestraAEliminar.id_muestra}/`);

        this.mostrarToast(
          `Muestra #${this.muestraAEliminar.id_muestra} eliminada correctamente.`,
          "exito",
        );

        // Verificamos si la imagen que estamos borrando es la que estábamos viendo
        const eraLaMisma =
          this.imagenSeleccionada &&
          this.imagenSeleccionada.id_muestra === this.muestraAEliminar.id_muestra;

        // Cierra el modal primero para evitar conflictos visuales
        this.muestraAEliminar = null;

        // Recargamos los datos desde cero
        await this.recargarDatosCaso(this.caseId, eraLaMisma);

        // Si después de recargar no hay imágenes, nos aseguramos de no mostrar errores
        if (this.totalImagenes === 0) {
          this.imagenSeleccionada = null;
          this.verMascara = false;
        }

        // Avisamos al Sidebar para que actualice sus contadores
        this.$emit("edicion-guardada");
      } catch (error) {
        console.error("Error eliminando muestra:", error);
        this.mostrarToast("Error al eliminar la muestra.", "error");
        this.muestraAEliminar = null; // Cierra el modal aunque haya error
      } finally {
        this.loading = false;
      }
    },

    // ============================================================
    // NAVEGACIÓN DE IMÁGENES
    // ============================================================
    siguienteImagen() {
      if (this.indiceImagenSeleccionada < this.imagenes.length - 1) {
        this.imagenSeleccionada = this.imagenes[this.indiceImagenSeleccionada + 1];
        this.resetZoom();
      }
    },

    imagenAnterior() {
      if (this.indiceImagenSeleccionada > 0) {
        this.imagenSeleccionada = this.imagenes[this.indiceImagenSeleccionada - 1];
        this.resetZoom();
      }
    },

    teclasOverlay(e) {
      if (!this.imagenEnEdicion) return;
      if (e.key === "ArrowRight") this.siguienteImagen();
      if (e.key === "ArrowLeft") this.imagenAnterior();
      if (e.key === "Escape") this.imagenEnEdicion = false;

      // Atajos de teclado para Deshacer/Rehacer
      if (e.ctrlKey && e.key === "z") {
        e.preventDefault();
        this.deshacer();
      }
      if (e.ctrlKey && e.key === "y") {
        e.preventDefault();
        this.rehacer();
      }
    },

    // ============================================================
    // ZOOM Y ARRASTRE
    // ============================================================
    onWheelZoom(e) {
      const zoomAnterior = this.zoom;

      if (e.deltaY < 0 && this.zoom < this.zoomMax) {
        this.zoom += this.zoomStep;
      }
      if (e.deltaY > 0 && this.zoom > this.zoomMin) {
        this.zoom -= this.zoomStep;
      }

      if (this.zoom === zoomAnterior) return;

      const rect = e.currentTarget.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const dx = mouseX - centerX;
      const dy = mouseY - centerY;

      const factor = this.zoom / zoomAnterior;

      this.offsetX -= dx * (factor - 1);
      this.offsetY -= dy * (factor - 1);

      if (this.zoom === 1) {
        this.offsetX = 0;
        this.offsetY = 0;
      }
      this.limitarMovimiento();
    },

    resetZoom() {
      this.zoom = 1;
      this.offsetX = 0;
      this.offsetY = 0;
    },

    startDrag(e) {
      if (this.zoom <= 1) return;

      if (this.edicionActiva && this.herramientaActiva && e.button === 0) {
        return;
      }

      this.isDragging = true;
      this.startX = e.clientX - this.offsetX;
      this.startY = e.clientY - this.offsetY;
    },

    onDrag(e) {
      if (!this.isDragging || this.zoom <= 1) return;

      this.offsetX = e.clientX - this.startX;
      this.offsetY = e.clientY - this.startY;

      this.limitarMovimiento();
    },

    endDrag() {
      this.isDragging = false;
    },

    limitarMovimiento() {
      const wrapper = this.$refs.editorWrapper;
      const img = this.$refs.editorImage;

      if (!wrapper || !img) return;

      const wrapperRect = wrapper.getBoundingClientRect();

      const imgWidth = img.offsetWidth * this.zoom;
      const imgHeight = img.offsetHeight * this.zoom;

      const maxX = imgWidth > wrapperRect.width ? (imgWidth - wrapperRect.width) / 2 : 0;
      const maxY = imgHeight > wrapperRect.height ? (imgHeight - wrapperRect.height) / 2 : 0;

      this.offsetX = Math.min(maxX, Math.max(-maxX, this.offsetX));
      this.offsetY = Math.min(maxY, Math.max(-maxY, this.offsetY));
    },

    async cargarMascaraConToken() {
      if (!this.imagenSeleccionada?.id_analisis) return;
      this.liberarBlobMascara();
      try {
        const url = `${this.API_URL}/mascaras/${this.imagenSeleccionada.id_analisis}/${this.mascaraActual}/?t=${this.mascaraTimestamp}`;

        const res = await axios.get(url, { responseType: "blob" });
        this.mascaraBlobUrl = URL.createObjectURL(res.data);
      } catch (e) {
        console.error("Error cargando máscara:", e);
        this.mascaraBlobUrl = null;
        // this.verMascara = false;
      }
    },
    liberarBlobMascara() {
      if (this.mascaraBlobUrl) {
        URL.revokeObjectURL(this.mascaraBlobUrl);
        this.mascaraBlobUrl = null;
      }
    },

    // ============================================================
    // CONTROL DE MÁSCARAS
    // ============================================================
    verMascaraSola(tipo) {
      this.mascaraActual = tipo;
      this.verMascara = true;

      this.mascarasVisibles = {
        nucleo: tipo === "nucleo",
        micronucleo: tipo === "micronucleo",
        membrana: tipo === "membrana",
      };
    },

    actualizarMascara() {
      const activas = Object.values(this.mascarasVisibles).filter((v) => v).length;

      if (activas === 0) {
        this.verMascara = false;
      } else if (activas === 1) {
        const tipoActivo = Object.keys(this.mascarasVisibles).find(
          (key) => this.mascarasVisibles[key],
        );
        this.mascaraActual = tipoActivo;
        this.verMascara = true;
      } else {
        this.mascaraActual = "overlay";
        this.verMascara = true;
      }
    },

    toggleTodasMascaras() {
      this.verMascara = !this.verMascara;

      if (this.verMascara) {
        this.mascarasVisibles = {
          nucleo: true,
          micronucleo: true,
          membrana: true,
        };
        this.mascaraActual = "overlay";
      }
    },

    obtenerUrlMascara() {
      if (!this.imagenSeleccionada?.id_analisis) return "";
      const tipoUrl = this.mascaraActual;
      if (!tipoUrl) return "";
      return `${this.API_URL}/mascaras/${this.imagenSeleccionada.id_analisis}/${tipoUrl}/?t=${this.mascaraTimestamp || tipoUrl}`;
    },

    handleMascaraError(event) {
      console.error("Error cargando mascara:", event.target?.src);
      this.verMascara = false;
    },

    // ============================================================
    // HISTORIAL (DESHACER / REHACER)
    // ============================================================
    guardarEstadoHistorial() {
      if (this.historialIndex < this.historial.length - 1) {
        this.historial = this.historial.slice(0, this.historialIndex + 1);
      }

      const snapshot = JSON.parse(JSON.stringify(this.poligonos));
      this.historial.push(snapshot);

      if (this.historial.length > 30) {
        this.historial.shift();
      } else {
        this.historialIndex++;
      }
    },

    deshacer() {
      if (this.puedeDeshacer) {
        this.historialIndex--;
        this.poligonos = JSON.parse(JSON.stringify(this.historial[this.historialIndex]));
        this.redibujarCanvas();
      }
    },

    rehacer() {
      if (this.puedeRehacer) {
        this.historialIndex++;
        this.poligonos = JSON.parse(JSON.stringify(this.historial[this.historialIndex]));
        this.redibujarCanvas();
      }
    },

    cerrarEditor() {
      this.imagenEnEdicion = false;
      this.zoom = 1;
      this.offsetX = 0;
      this.offsetY = 0;
    },

    editorToggleMascara(tipo) {
      if (this.editorVerMascara && this.editorMascaraActual === tipo) {
        this.editorVerMascara = false;
      } else {
        this.editorVerMascara = true;
        this.editorMascaraActual = tipo;
      }
      this.redibujarCanvas();
    },

    obtenerUrlMascaraEditor() {
      if (!this.imagenSeleccionada?.id_analisis) return "";
      return `${this.API_URL}/mascaras/${this.imagenSeleccionada.id_analisis}/${this.editorMascaraActual}/?t=${this.editorMascaraActual}`;
    },

    mostrarToast(mensaje, tipo = "exito", duracion = 3500) {
      if (this.$toastTimer) clearTimeout(this.$toastTimer);
      this.toast = { visible: true, mensaje, tipo };
      this.$toastTimer = setTimeout(() => {
        this.toast.visible = false;
      }, duracion);
    },

    async guardarCambiosEdicion() {
      if (!this.imagenSeleccionada?.id_analisis) return;

      if (this.modoAjustar) {
        this.guardarAjusteTemporal();
      }

      const objetos = [];
      this.poligonos.membranas.forEach((pts) => {
        objetos.push({
          tipo: "membrana",
          puntos: pts.map((p) => [Math.round(p.x), Math.round(p.y)]),
        });
      });
      this.poligonos.nucleos.forEach((pts) => {
        objetos.push({
          tipo: "nucleo",
          puntos: pts.map((p) => [Math.round(p.x), Math.round(p.y)]),
        });
      });
      this.poligonos.micronucleos.forEach((pts) => {
        objetos.push({
          tipo: "micronucleo",
          puntos: pts.map((p) => [Math.round(p.x), Math.round(p.y)]),
        });
      });

      try {
        const res = await axios.patch(
          `${this.API_URL}/analisis/${this.imagenSeleccionada.id_analisis}/editar/`,
          { objetos },
        );

        // 1. Rompemos el caché generando un nuevo timestamp ANTES de pedir la imagen
        this.mascaraTimestamp = Date.now();

        // 2. FALSO para que NO te mueva de imagen, te deje en la misma
        await this.recargarDatosCaso(this.caseId, false);

        // 3. Volvemos a pedir la máscara al servidor
        if (this.verMascara) {
          await this.cargarMascaraConToken();
        }

        this.edicionActiva = false;
        this.herramientaActiva = null;
        this.modoAjustar = false;
        this.poligonoSeleccionado = null;

        this.$emit("edicion-guardada");

        this.mostrarToast(
          `Guardado · v${res.data.version}/${res.data.max_versiones} · ` +
            `${res.data.nucleos}N · ${res.data.micronucleos}MN · ${res.data.membranas}M`,
        );
      } catch (err) {
        console.error("Error al guardar:", err);
        this.mostrarToast("Error al guardar. Intenta de nuevo.", "error", 5000);
      }
    },

    obtenerCoordenadas(e) {
      const canvas = this.$refs.editorCanvas;
      const rect = canvas.getBoundingClientRect();

      const xVisual = e.clientX - rect.left;
      const yVisual = e.clientY - rect.top;

      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;

      return {
        x: xVisual * scaleX,
        y: yVisual * scaleY,
      };
    },

    inicializarCanvas() {
      const canvas = this.$refs.editorCanvas;
      const img = this.$refs.editorImage;
      if (!canvas || !img) return;

      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;

      this.cargarPoligonosDesdeJSON();
      this.redibujarCanvas();
    },

    redibujarCanvas() {
      const canvas = this.$refs.editorCanvas;
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (this.editorVerMascara) {
        const COLORES = {
          membranas: "#0078ff", // Azul
          nucleos: "#00dc00", // Verde
          micronucleos: "#ff0000", // Rojo
        };

        let capasADibujar = [];
        if (this.editorMascaraActual === "overlay")
          capasADibujar = ["membranas", "nucleos", "micronucleos"];
        else if (this.editorMascaraActual === "membrana") capasADibujar = ["membranas"];
        else if (this.editorMascaraActual === "nucleo") capasADibujar = ["nucleos"];
        else if (this.editorMascaraActual === "micronucleo") capasADibujar = ["micronucleos"];

        for (const tipo of capasADibujar) {
          if (!this.poligonos[tipo]) continue;

          this.poligonos[tipo].forEach((poly, i) => {
            const esSeleccionado =
              this.modoAjustar &&
              this.poligonoSeleccionado?.tipo === tipo &&
              this.poligonoSeleccionado?.index === i;

            ctx.beginPath();
            const ptsADibujar = esSeleccionado ? this.poligonoTemporal : poly;

            ptsADibujar.forEach((p, idx) => {
              if (idx === 0) ctx.moveTo(p.x, p.y);
              else ctx.lineTo(p.x, p.y);
            });
            ctx.closePath();

            ctx.strokeStyle = esSeleccionado ? "yellow" : COLORES[tipo];

            const grosorBase = esSeleccionado ? 4 : this.edicionActiva ? 3 : 2;

            ctx.lineWidth = Math.max(1.5, grosorBase / this.zoom);
            ctx.stroke();

            if (esSeleccionado) {
              ptsADibujar.forEach((p) => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, 7 / this.zoom, 0, 2 * Math.PI);
                ctx.fillStyle = "cyan";
                ctx.fill();
                ctx.lineWidth = Math.max(1, 1.5 / this.zoom);
                ctx.strokeStyle = "black";
                ctx.stroke();
              });
            }
          });
        }
      }

      if (this.poligonoTemporal.length > 1 && !this.modoAjustar) {
        ctx.beginPath();
        this.poligonoTemporal.forEach((p, i) => {
          if (i === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        });
        ctx.strokeStyle = "white";
        ctx.lineWidth = Math.max(1.5, 3 / this.zoom);
        ctx.stroke();
      }
    },

    onCanvasMouseDown(e) {
      if (!this.edicionActiva) return;

      if (this.herramientaActiva && e.button === 0) {
        e.stopPropagation();
      }

      const { x, y } = this.obtenerCoordenadas(e);

      if (this.herramientaActiva === "editar") {
        if (this.modoAjustar) {
          const vIndex = this.seleccionarVertice(x, y);
          if (vIndex !== null) {
            this.verticeSeleccionado = vIndex;
            return;
          } else {
            const seleccionado = this.detectarPoligonoClick(x, y);

            if (
              seleccionado &&
              this.poligonoSeleccionado &&
              seleccionado.tipo === this.poligonoSeleccionado.tipo &&
              seleccionado.index === this.poligonoSeleccionado.index
            ) {
              return;
            }

            this.guardarAjusteTemporal();
            this.modoAjustar = false;
            this.poligonoSeleccionado = null;
            if (seleccionado) this.activarModoAjustar(seleccionado);
            this.redibujarCanvas();
            return;
          }
        } else {
          const seleccionado = this.detectarPoligonoClick(x, y);
          if (seleccionado) this.activarModoAjustar(seleccionado);
          return;
        }
      }

      if (this.herramientaActiva === "borrar") {
        const seleccionado = this.detectarPoligonoClick(x, y);
        if (seleccionado) {
          this.poligonos[seleccionado.tipo].splice(seleccionado.index, 1);
          this.guardarEstadoHistorial();
          this.redibujarCanvas();
        }
        return;
      }

      if (this.herramientaActiva?.startsWith("agregar")) {
        this.dibujando = true;
        this.poligonoTemporal = [{ x, y }];
      }
    },

    onCanvasMouseMove(e) {
      const { x, y } = this.obtenerCoordenadas(e);

      if (this.herramientaActiva === "editar" && this.verticeSeleccionado !== null) {
        this.poligonoTemporal[this.verticeSeleccionado] = { x, y };
        this.redibujarCanvas();
        return;
      }

      if (!this.dibujando) return;
      this.poligonoTemporal.push({ x, y });
      this.redibujarCanvas();
    },

    onCanvasMouseUp() {
      if (this.herramientaActiva === "editar" && this.verticeSeleccionado !== null) {
        this.guardarAjusteTemporal();
        this.verticeSeleccionado = null;
        this.guardarEstadoHistorial();
        return;
      }

      if (!this.dibujando) return;
      this.dibujando = false;

      if (!this.modoAjustar && this.poligonoTemporal.length > 5) {
        if (this.herramientaActiva === "agregar-membrana")
          this.poligonos.membranas.push([...this.poligonoTemporal]);
        if (this.herramientaActiva === "agregar-nucleo")
          this.poligonos.nucleos.push([...this.poligonoTemporal]);
        if (this.herramientaActiva === "agregar-micronucleo")
          this.poligonos.micronucleos.push([...this.poligonoTemporal]);
        this.guardarEstadoHistorial();
      }

      if (!this.modoAjustar) {
        this.poligonoTemporal = [];
      }
      this.redibujarCanvas();
    },

    detectarPoligonoClick(x, y) {
      const ctx = this.$refs.editorCanvas.getContext("2d");
      const ordenCapas = ["micronucleos", "nucleos", "membranas"];

      for (const tipo of ordenCapas) {
        for (let i = this.poligonos[tipo].length - 1; i >= 0; i--) {
          const poly = this.poligonos[tipo][i];

          ctx.beginPath();
          poly.forEach((p, index) => {
            if (index === 0) ctx.moveTo(p.x, p.y);
            else ctx.lineTo(p.x, p.y);
          });
          ctx.closePath();

          if (ctx.isPointInPath(x, y)) {
            return { tipo, index: i };
          }
        }
      }

      return null;
    },

    cargarPoligonosDesdeJSON() {
      const analisis = this.imagenSeleccionada?.analisis_full;
      if (!analisis) return;

      const archivoActivo = analisis.archivos?.find((a) => a.activo);
      if (!archivoActivo?.contenido_json) return;

      const objetos = archivoActivo.contenido_json.objetos ?? [];

      const img = this.$refs.editorImage;
      if (!img) return;

      this.poligonos = {
        membranas: [],
        nucleos: [],
        micronucleos: [],
      };

      objetos.forEach((obj) => {
        if (!obj.puntos) return;

        const puntos = obj.puntos.map((p) => ({
          x: p[0],
          y: p[1],
        }));

        if (obj.tipo === "membrana") {
          this.poligonos.membranas.push(puntos);
        }

        if (obj.tipo === "nucleo") {
          this.poligonos.nucleos.push(puntos);
        }

        if (obj.tipo === "micronucleo") {
          this.poligonos.micronucleos.push(puntos);
        }
      });

      this.historial = [];
      this.historialIndex = -1;
      this.guardarEstadoHistorial();
    },

    // ============================================================
    // LÓGICA DE EDICIÓN DE VÉRTICES
    // ============================================================
    onCanvasDoubleClick(e) {
      if (this.herramientaActiva === "editar") {
        if (this.modoAjustar) {
          const { x, y } = this.obtenerCoordenadas(e);
          const idx = this.encontrarAristaCercana(x, y, this.poligonoTemporal);
          this.poligonoTemporal.splice(idx, 0, { x, y });
          this.guardarAjusteTemporal();
          this.guardarEstadoHistorial();
          this.redibujarCanvas();
        }
      } else {
        this.resetZoom();
      }
    },

    activarModoAjustar(seleccionado) {
      this.poligonoSeleccionado = seleccionado;
      this.modoAjustar = true;
      const pts = this.poligonos[seleccionado.tipo][seleccionado.index];

      if (pts.length > 20) {
        this.poligonoTemporal = this.simplificarPoligono(pts, 2.0);
      } else {
        this.poligonoTemporal = JSON.parse(JSON.stringify(pts));
      }
      this.guardarAjusteTemporal();
      this.redibujarCanvas();
    },

    seleccionarVertice(x, y) {
      if (!this.poligonoTemporal) return null;
      const hitbox = 25 / this.zoom;

      for (let i = 0; i < this.poligonoTemporal.length; i++) {
        const p = this.poligonoTemporal[i];
        if (Math.abs(p.x - x) < hitbox && Math.abs(p.y - y) < hitbox) {
          return i;
        }
      }
      return null;
    },

    encontrarAristaCercana(px, py, poligono) {
      let min_dist = Infinity;
      let indice_insertar = 0;
      const n = poligono.length;

      for (let i = 0; i < n; i++) {
        const p1 = poligono[i];
        const p2 = poligono[(i + 1) % n];
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;

        let dist;
        if (dx === 0 && dy === 0) {
          dist = Math.hypot(px - p1.x, py - p1.y);
        } else {
          let t = ((px - p1.x) * dx + (py - p1.y) * dy) / (dx * dx + dy * dy);
          t = Math.max(0, Math.min(1, t));
          const proj_x = p1.x + t * dx;
          const proj_y = p1.y + t * dy;
          dist = Math.hypot(px - proj_x, py - proj_y);
        }

        if (dist < min_dist) {
          min_dist = dist;
          indice_insertar = i + 1;
        }
      }
      return indice_insertar;
    },

    guardarAjusteTemporal() {
      if (!this.poligonoSeleccionado || !this.poligonoTemporal) return;
      const { tipo, index } = this.poligonoSeleccionado;
      this.poligonos[tipo][index] = JSON.parse(JSON.stringify(this.poligonoTemporal));
    },

    simplificarPoligono(puntos, epsilon) {
      if (puntos.length <= 2) return puntos;

      const getDistancia = (p, p1, p2) => {
        let x = p1.x,
          y = p1.y,
          dx = p2.x - p1.x,
          dy = p2.y - p1.y;
        if (dx !== 0 || dy !== 0) {
          const t = ((p.x - p1.x) * dx + (p.y - p1.y) * dy) / (dx * dx + dy * dy);
          if (t > 1) {
            x = p2.x;
            y = p2.y;
          } else if (t > 0) {
            x += dx * t;
            y += dy * t;
          }
        }
        dx = p.x - x;
        dy = p.y - y;
        return Math.sqrt(dx * dx + dy * dy);
      };

      let dmax = 0,
        index = 0;
      const end = puntos.length - 1;
      for (let i = 1; i < end; i++) {
        const d = getDistancia(puntos[i], puntos[0], puntos[end]);
        if (d > dmax) {
          index = i;
          dmax = d;
        }
      }

      if (dmax > epsilon) {
        const rec1 = this.simplificarPoligono(puntos.slice(0, index + 1), epsilon);
        const rec2 = this.simplificarPoligono(puntos.slice(index), epsilon);
        return rec1.slice(0, rec1.length - 1).concat(rec2);
      } else {
        return [puntos[0], puntos[end]];
      }
    },
  },
};
</script>

<style scoped>
.content {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
  background: #f8f9fa;
  height: 100%;
}

/* HEADER */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e0e0e0;
  height: 60px;
}

.header-left {
  flex: 1;
}

.page-title {
  margin: 0 0 6px 0;
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  padding: 6px 12px;
  background: #f0f4f8;
  border-radius: 8px;
  font-weight: 500;
}

.breadcrumb-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.breadcrumb-separator {
  color: #999;
}

.breadcrumb-icon {
  width: 14px;
  height: 14px;
  opacity: 0.8;
}

.breadcrumb-separator {
  color: #999;
  font-size: 16px;
  font-weight: 600;
}

.breadcrumb-placeholder {
  color: #999;
  font-style: italic;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-action {
  padding: 10px 18px;
  border: 2px solid #e0e0e0;
  background: white;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  border-radius: 10px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #2c3e50;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-action.csv:hover {
  border-color: #43a047;
  background: #e8f5e9;
}

.btn-action.pdf:hover {
  border-color: #e53935;
  background: #ffebee;
}

.btn-icon {
  font-size: 16px;
}

/* LAYOUT */
.layout-grid {
  display: flex;
  gap: 16px;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* GALERÍA */
.gallery-column {
  width: 200px;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.gallery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  position: sticky;
  top: -12px;
  background: white;
  z-index: 10;
}

.gallery-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.gallery-count {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-auto-rows: 60px;
  gap: 8px;
}

.thumb {
  cursor: pointer;
  border: 3px solid transparent;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0.7;
  overflow: hidden;
  position: relative;
  background: #f0f0f0;
}

.thumb:hover {
  opacity: 1;
  transform: scale(1.05);
}

.thumb.active {
  border-color: #667eea;
  opacity: 1;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  transform: scale(1.05);
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumb-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  padding: 4px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.thumb:hover .thumb-overlay,
.thumb.active .thumb-overlay {
  opacity: 1;
}

.thumb-id {
  color: white;
  font-size: 10px;
  font-weight: 600;
}

.empty-gallery {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 20px;
  text-align: center;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.3;
}

.empty-gallery p {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 500;
  color: #666;
}

.empty-gallery span {
  font-size: 12px;
  color: #999;
}
/* Nuevo Galeria */
.gallery-section {
  margin-bottom: 12px;
}

.gallery-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 6px 8px;
  background: #f0f4f8;
  border-radius: 8px;
  margin-bottom: 6px;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.2s ease;
}

.gallery-toggle:hover {
  background: #e2e8f0;
}

.section-count {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  min-width: 22px;
  text-align: center;
  transition: all 0.2s ease;
}

.section-count.original {
  background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
}

.gallery-toggle:hover .section-count {
  transform: scale(1.1);
}

/* VISOR */
.viewer-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 0; /* <--- CRÍTICO: Esta línea faltaba en tu código */
  overflow: hidden;
}

/* TARJETAS */
.card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.main-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* Contenedor del título y la etiqueta apilados */
.card-title-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px; /* Espacio entre el título y la etiqueta */
}

.card-title-section h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1;
}

/* ── BADGE DE TIPO EN EL HEADER DEL VISOR ── */
.tipo-badge-header {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 9px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  /* Eliminamos el margin-left y vertical-align que tenía antes */
}

.tipo-badge-sangre {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fca5a5;
}

.tipo-badge-saliva {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #93c5fd;
}

.card-subtitle {
  font-size: 12px;
  color: #999;
}

.card-tools {
  display: flex;
  gap: 8px;
}

.tool-btn {
  width: 36px;
  height: 36px;
  border: 2px solid #e0e0e0;
  background: white;
  cursor: pointer;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-btn:hover {
  background: #f0f4f8;
  transform: translateY(-2px);
}

.tool-btn.danger:hover {
  border-color: #ef5350;
  background: #ffebee;
}

.tool-btn.success:hover {
  border-color: #66bb6a;
  background: #e8f5e9;
}

/* ============================================ */
/* VISTA DIVIDIDA */
/* ============================================ */

.split-view {
  display: flex;
  gap: 20px;
  padding: 16px;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.image-container {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
  min-height: 0;
}

/* ============================================ */
/* CONTENEDOR DE IMAGEN Y OVERLAY DE MÁSCARAS */
/* ============================================ */

.img-placeholder {
  position: relative;
  flex: 1; /* <--- Cambio importante aquí */
  width: 100%;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border-radius: 12px;
  overflow: hidden;
}

/* Imagen principal */
.main-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  display: block;
  position: relative;
  z-index: 1; /* Imagen en capa base */
}

/* ⭐ OVERLAY DE MÁSCARAS - POSICIÓN ABSOLUTA SOBRE LA IMAGEN */
.mask-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  pointer-events: none; /* Los clicks pasan a través del overlay */
  z-index: 2; /* Máscara encima de la imagen */
  opacity: 0.85; /* Semi-transparente para ver ambas capas */
  transition: opacity 0.3s ease;
}

.mask-overlay:hover {
  opacity: 1; /* Más opaca al pasar el mouse */
}

/* Estados de carga de la máscara */
.mask-overlay[src=""],
.mask-overlay:not([src]) {
  display: none; /* Ocultar si no hay src */
}

/* Estado vacío cuando no hay imagen */
.empty-image-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #999;
}

.empty-image-icon {
  font-size: 64px;
  opacity: 0.3;
}

.empty-image-state p {
  margin: 0;
  font-size: 14px;
}

/* ⭐ TOGGLE DE SEGMENTACIÓN — esquina inferior derecha, no tapa la imagen */
.img-overlay {
  position: absolute;
  bottom: 12px;
  right: 12px;
  z-index: 10;
  pointer-events: none;
}

.seg-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px 7px 10px;
  border: none;
  border-radius: 20px;
  background: rgba(20, 20, 30, 0.72);
  color: rgba(255, 255, 255, 0.88);
  font-size: 12px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  pointer-events: auto;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
  transition: all 0.2s ease;
  letter-spacing: 0.3px;
}

.seg-toggle svg {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
  transition: stroke 0.2s;
}

.seg-toggle:hover {
  background: rgba(40, 40, 55, 0.9);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.seg-toggle.active {
  background: rgba(76, 175, 80, 0.85);
  color: white;
  box-shadow: 0 2px 12px rgba(76, 175, 80, 0.45);
}

.seg-toggle.active:hover {
  background: rgba(56, 142, 60, 0.92);
}

.no-seg-badge {
  display: inline-block;
  padding: 5px 11px;
  border-radius: 20px;
  background: rgba(20, 20, 30, 0.55);
  color: rgba(255, 255, 255, 0.55);
  font-size: 11px;
  font-weight: 500;
  backdrop-filter: blur(8px);
  pointer-events: none;
}

.clickable {
  cursor: zoom-in;
}

/* DATOS */
.data-container {
  flex: none;
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  /* (Borramos el justify-content: center para que suba) */
}

.data-header {
  padding-bottom: 8px;
  border-bottom: 2px solid #f0f0f0;
}

.data-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
}

.data-table thead th {
  padding: 12px;
  background: #f8f9fa;
  border-bottom: 2px solid #e0e0e0;
  text-align: left;
  font-weight: 600;
  color: #666;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ⭐ NUEVAS REGLAS PARA ALINEAR ÍCONO Y TEXTO ⭐ */
.structure-cell {
  display: flex;
  align-items: center; /* Alinea verticalmente al centro */
  gap: 12px; /* Espacio entre el icono y la palabra */
}

.table-icon {
  width: 18px; /* Tamaño perfecto para texto normal */
  height: 18px;
  flex-shrink: 0;
}

.count {
  font-weight: 700;
  font-size: 15px; /* Un poco más sutil */
  text-align: right; /* Alineado a la derecha como en tu imagen */
  color: #2c3e50;
  vertical-align: middle; /* Asegura que el número no flote arriba o abajo */
}

.count.critical {
  color: #ef5350; /* Rojo para destacar micronúcleos */
}

.data-table tbody td {
  padding: 14px 12px;
  border-bottom: 1px solid #f0f0f0;
}

.data-row {
  transition: background 0.2s ease;
}

.data-row:hover {
  background: #f8f9fa;
}

.data-row.highlight {
  background: #fff3e0;
}

.data-row.highlight:hover {
  background: #ffe0b2;
}

.structure-icon {
  margin-right: 8px;
  font-size: 14px;
}

.count {
  font-weight: 700;
  font-size: 16px;
  text-align: right;
  color: #2c3e50;
}

.count.critical {
  color: #ef5350;
}

.no-data {
  text-align: center;
  padding: 40px 20px !important;
  color: #999;
}

.no-data-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.3;
}

/* ESTADO NORMAL (Desmarcado) */
.btn-review {
  padding: 14px;
  border: 2px solid #cbd5e1; /* Gris sutil */
  background: white;
  color: #475569; /* Gris oscuro */
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  border-radius: 10px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: auto;
}

.btn-review:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #94a3b8;
  transform: translateY(-2px);
}

.btn-icon-svg {
  width: 18px;
  height: 18px;
  transition: all 0.3s ease;
}

/* ESTADO MARCADO (Llamativo) */
.btn-review.marcado {
  border-color: #ef4444; /* Rojo llamativo */
  background: #fef2f2;
  color: #dc2626;
}

.btn-review.marcado:hover:not(:disabled) {
  background: #fee2e2;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

/* ESTADO CARGANDO */
.btn-review:disabled {
  opacity: 0.6;
  cursor: wait;
}

.btn-review:hover {
  background: #fff3e0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.2);
}

.full-width {
  width: 100%;
}

.card-header {
  padding: 8px 20px; /* Reducido para que sea más delgada */
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(to right, #fafbfc, #ffffff);
  flex-shrink: 0;
  height: 50px;
}

.card-header-simple h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.obj-table thead th {
  padding: 12px;
  background: #f8f9fa;
  border-bottom: 2px solid #e0e0e0;
  text-align: center;
  font-weight: 600;
  color: #666;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.obj-table tbody td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  text-align: center;
}

.obj-row:hover {
  background: #f8f9fa;
}

.obj-icon.nucleos {
  color: #66bb6a;
}

.obj-icon.micronucleos {
  color: #ef5350;
}

.obj-icon.membranas {
  color: #8d6e63;
}

.obj-btn:hover {
  background: #f0f4f8;
  border-color: #1e88e5;
  transform: scale(1.1);
}

/* OVERLAY EDICIÓN (Nuevo diseño oscuro y flechas integradas) */
.image-editor-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85); /* Fondo más oscuro para el "modo cine" */
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

.editor-container {
  position: relative;
  background: transparent;
  border-radius: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  box-shadow: none;
}

/* ⭐ ESTA ES LA CLASE QUE TE FALTABA ⭐ */
.editor-layout {
  display: flex;
  flex-direction: row; /* Fuerza a que estén en fila (lado a lado) */
  flex-wrap: nowrap; /* Prohíbe terminantemente que se bajen de línea */
  align-items: center;
  justify-content: center;
  gap: 40px;
  width: 100%;
  padding: 0 40px;
}

.editor-sidebar-right {
  border-left: 1px solid #2a2a2a;
  border-right: none;
}

/* --- PANEL LATERAL TIPO GLASSMORPHISM --- */
.editor-sidebar {
  width: 130px;
  min-width: 130px;
  max-width: 130px;
  box-sizing: border-box;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 12px;
  background: rgba(30, 30, 35, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.editor-sidebar-right {
  width: 220px;
  min-width: 220px;
  max-width: 220px;
  border-left: 1px solid rgba(255, 255, 255, 0.08);
}

.editor-image-wrapper {
  position: relative;
  /* ⭐ Restamos: 130px (izq) + 220px (der) + 80px (gaps) = 430px */
  max-width: calc(100vw - 430px);
  max-height: 85vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a1a;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.editor-image {
  max-width: 100%;
  max-height: 85vh;
  width: auto;
  height: auto;
  display: block;
  user-select: none;
  -webkit-user-drag: none;
}

/* --- BOTONES (BASE PARA EL IZQUIERDO) --- */
.tool-option {
  display: flex;
  flex-direction: column; /* Icono arriba, texto abajo */
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 6px;
  width: 100%;
  box-sizing: border-box;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(20, 20, 25, 0.4);
  color: #a0a0b0;
  font-size: 11px;
  line-height: 1.2;
  text-align: center;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tool-option span {
  display: block;
  width: 100%;
  white-space: normal;
  word-wrap: break-word;
}

.elegant-icon {
  width: 26px;
  height: 26px;
  transition: all 0.3s ease;
}

/* ⭐ EXCLUSIVO PARA LOS BOTONES DEL PANEL DERECHO ⭐ */
.editor-sidebar-right .tool-option {
  flex-direction: row; /* Icono a la izquierda, texto a la derecha */
  justify-content: flex-start; /* Alineado a la izquierda */
  padding: 12px 16px;
  gap: 12px;
  font-size: 13px; /* Letra un poquito más grande */
  text-align: left;
}

.editor-sidebar-right .elegant-icon {
  width: 20px; /* Icono más pequeño para formato fila */
  height: 20px;
  flex-shrink: 0;
}

.tool-option:hover {
  background: rgba(50, 50, 60, 0.8);
  transform: translateY(-2px);
  color: white;
}

/* Nuevos estilos para las flechas integradas */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.35);
  color: #ffffff;
  font-size: 36px;
  cursor: pointer;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(6px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.nav-arrow:hover {
  background: rgba(255, 255, 255, 0.7);
  color: black;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
  border-color: white;
}

.nav-arrow.left {
  left: 16px;
}
.nav-arrow.right {
  right: 16px;
}
.nav-arrow:disabled {
  opacity: 0;
  pointer-events: none;
}

/* Botón de cerrar rediseñado */
.close-btn {
  position: absolute;
  top: 20px;
  right: 40px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  z-index: 110;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(239, 83, 80, 0.8);
  color: white;
  transform: rotate(90deg);
}

/* --- BOTONES INACTIVOS --- */
.tool-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 8px;
  width: 100%;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(20, 20, 25, 0.4);
  color: #a0a0b0;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tool-option:hover {
  background: rgba(50, 50, 60, 0.8);
  transform: translateY(-2px);
  color: white;
}

.elegant-icon {
  width: 26px;
  height: 26px;
  transition: all 0.3s ease;
}

/* --- ESTADOS ACTIVOS (ILUMINACIÓN ESPECÍFICA) --- */
.tool-option.active.membrana-active {
  background: linear-gradient(135deg, rgba(46, 125, 50, 0.8), rgba(27, 94, 32, 0.9));
  border-color: #4caf50;
  color: white;
  box-shadow: 0 0 16px rgba(76, 175, 80, 0.4);
}
.tool-option.active.membrana-active .elegant-icon {
  stroke: white;
}
.tool-option.active.membrana-active .elegant-icon circle {
  stroke: white;
}

.tool-option.active.nucleo-active {
  background: linear-gradient(135deg, rgba(21, 101, 192, 0.8), rgba(13, 71, 161, 0.9));
  border-color: #1e88e5;
  color: white;
  box-shadow: 0 0 16px rgba(30, 136, 229, 0.4);
}
.tool-option.active.nucleo-active .elegant-icon {
  stroke: white;
}
.tool-option.active.nucleo-active .elegant-icon circle[fill] {
  fill: white;
}

.tool-option.active.micronucleo-active {
  background: linear-gradient(135deg, rgba(106, 27, 154, 0.8), rgba(74, 20, 140, 0.9));
  border-color: #ab47bc;
  color: white;
  box-shadow: 0 0 16px rgba(171, 71, 188, 0.4);
}
.tool-option.active.micronucleo-active .elegant-icon {
  stroke: white;
}
.tool-option.active.micronucleo-active .elegant-icon circle[fill] {
  fill: white;
}

.tool-option.active.borrar-active {
  background: linear-gradient(135deg, rgba(97, 97, 97, 0.8), rgba(66, 66, 66, 0.9));
  border-color: #9e9e9e;
  color: white;
  box-shadow: 0 0 16px rgba(158, 158, 158, 0.4);
}
.tool-option.active.borrar-active .elegant-icon {
  stroke: white;
}

.tool-option.active.editar-active {
  background: linear-gradient(135deg, rgba(123, 97, 255, 0.9), rgba(94, 53, 177, 0.9));
  border-color: #8c9eff;
  color: white;
  box-shadow: 0 0 20px rgba(123, 97, 255, 0.6);
}
.tool-option.active.editar-active .elegant-icon {
  stroke: white;
}

/* ANIMACIÓN */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  .editor-image-wrapper {
    max-width: 95vw;
    max-height: 70vh;
  }
  .nav-arrow {
    width: 40px;
    height: 40px;
    font-size: 28px;
  }
  .nav-arrow.left {
    left: 8px;
  }
  .nav-arrow.right {
    right: 8px;
  }
  .close-btn {
    top: -45px;
    right: 10px;
  }
}

@media (max-width: 1200px) {
  /* Galería más delgada */
  .gallery-column {
    width: 120px; /* antes 230px */
    padding: 8px;
  }

  /* Galería en UNA sola columna */
  .gallery-grid {
    grid-template-columns: 1fr;
    grid-auto-rows: 70px;
  }

  /* Miniaturas más compactas */
  .thumb {
    border-width: 2px;
    border-radius: 8px;
  }

  .thumb-id {
    font-size: 9px;
  }
}

/* ── EDITOR: MASCARA OVERLAY ── */
.editor-mask-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
  z-index: 5;
  opacity: 0.85;
  border-radius: 12px;
  transform-origin: center center;
}

/* ── EDITOR: SEPARADORES DE SECCION ── */
.editor-section-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.35);
  padding: 0 4px;
  margin-top: 4px;
}

/* ── EDITOR: PANEL DE INFO ── */
.editor-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.25);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.editor-info-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.75);
  white-space: nowrap;
}

.editor-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  opacity: 0.9;
}

.editor-no-data {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.3);
  text-align: center;
  padding: 4px 0;
}

/* ── EDITOR: INDICADOR DE ZOOM ── */
.zoom-indicator {
  position: absolute;
  bottom: 14px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.55);
  color: rgba(255, 255, 255, 0.8);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  backdrop-filter: blur(8px);
  pointer-events: none;
  z-index: 20;
}

/* ── EDITOR: ESTADO ACTIVO OVERLAY ── */
.tool-option.active.overlay-active {
  background: rgba(144, 202, 249, 0.2);
  border-color: rgba(144, 202, 249, 0.5);
  box-shadow: 0 0 10px rgba(144, 202, 249, 0.25);
}

/* ── EDICION ── */
/* ── Edicion Inactivo ── */
.tool-option:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Color especial (Teal/Verde Azulado) para el Switch Maestro de Edición */
.tool-option.active.modo-edicion-active {
  /* Un degradado diferente para que se note que es un control principal */
  background: linear-gradient(135deg, rgba(0, 188, 212, 0.8), rgba(0, 151, 167, 0.9));
  border-color: #00bcd4;
  color: white;
  box-shadow: 0 0 20px rgba(0, 188, 212, 0.5);
}
/* Asegura que el candado se pinte de blanco al activarse */
.tool-option.active.modo-edicion-active .elegant-icon {
  stroke: white;
}

/* ── BOTON DE GUARDAR CAMBIOS (EDITOR) ── */
.btn-guardar-edicion {
  margin-top: auto; /* Empuja el botón hacia el fondo del panel */
  background: linear-gradient(135deg, #10b981 0%, #059669 100%); /* Verde brillante */
  border-color: transparent;
  color: white;
  font-weight: 600;
  padding: 14px 16px;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.btn-guardar-edicion:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%); /* Verde más oscuro al hover */
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* El icono del botón guardar hereda el color blanco del texto */
.btn-guardar-edicion .elegant-icon {
  stroke: white;
}

/* Estado deshabilitado del botón guardar */
.btn-guardar-edicion:disabled {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.3);
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.btn-guardar-edicion:disabled .elegant-icon {
  stroke: rgba(255, 255, 255, 0.3);
}

.editor-image-wrapper {
  position: relative;
}

.editor-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.editor-transform-group {
  position: relative;
  display: inline-block;
  transform-origin: center center;
  line-height: 0;
}
.editor-toast {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 20px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  z-index: 200;
  pointer-events: none;
  white-space: nowrap;
  backdrop-filter: blur(12px);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
}
.editor-toast svg {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
}
.editor-toast.exito {
  background: rgba(0, 90, 50, 0.93);
  border: 1px solid rgba(0, 210, 110, 0.45);
  color: rgba(170, 255, 200, 0.95);
}
.editor-toast.error {
  background: rgba(110, 0, 0, 0.93);
  border: 1px solid rgba(255, 80, 80, 0.45);
  color: rgba(255, 200, 200, 0.95);
}
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}
.toast-fade-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(-8px);
}
.toast-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-5px);
}

/* ── CHIP DE TIPO EN MINIATURAS (SOLO ÍCONO) ── */
.tipo-chip {
  position: absolute;
  top: 6px;
  left: 6px;
  z-index: 5;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tipo-chip svg {
  width: 16px;
  height: 16px;
  /* Sombra para que el ícono resalte sobre cualquier foto sin necesitar cuadro de fondo */
  filter: drop-shadow(0px 2px 3px rgba(0, 0, 0, 0.7));
}

.tipo-sangre {
  color: #fb7185; /* Rojo claro para que resalte en fondos oscuros */
}

.tipo-saliva {
  color: #60a5fa; /* Azul celeste brillante */
}

/* ── BADGE DE TIPO EN EL HEADER DEL VISOR ── */
.tipo-badge-header {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 9px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  margin-left: 8px;
  vertical-align: middle;
}
.tipo-badge-sangre {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fca5a5;
}
.tipo-badge-saliva {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #93c5fd;
}

/* BOTÓN ELIMINAR EN MINIATURAS */
.btn-delete-thumb {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(239, 83, 80, 0.85); /* Rojo semi transparente */
  color: white;
  border: none;
  border-radius: 6px;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0; /* Oculto por defecto */
  transition: all 0.2s ease;
  z-index: 10;
  backdrop-filter: blur(4px);
}

.btn-delete-thumb svg {
  width: 12px;
  height: 12px;
}

.thumb:hover .btn-delete-thumb {
  opacity: 1; /* Aparece al hacer hover en la miniatura */
}

.btn-delete-thumb:hover {
  background: #e53935; /* Rojo sólido al hover */
  transform: scale(1.1);
}

/* ========================================= */
/* MODAL DE CONFIRMACIÓN */
/* ========================================= */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: modalPopUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-icon.warning {
  width: 48px;
  height: 48px;
  background: #fef2f2;
  color: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.modal-icon.warning svg {
  width: 24px;
  height: 24px;
}

.modal-content h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #1e293b;
}

.modal-content p {
  margin: 0 0 24px;
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.btn-cancelar {
  flex: 1;
  padding: 10px;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-cancelar:hover {
  background: #e2e8f0;
}

.btn-confirmar-eliminar {
  flex: 1;
  padding: 10px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-confirmar-eliminar:hover:not(:disabled) {
  background: #dc2626;
}

.btn-confirmar-eliminar:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@keyframes modalPopUp {
  0% {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* ========================================= */
/* BOTONES DE CAPAS EN EL ENCABEZADO */
/* ========================================= */

.card-header {
  padding: 12px 20px;
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center; /* Alinea texto y botones verticalmente */
  background: white;
  flex-shrink: 0;
  height: auto;
}

.card-title-section h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  white-space: nowrap; /* Evita que el texto baje a la siguiente línea */
}

/* Contenedor de botones flotantes */
.layer-toggles {
  display: flex;
  gap: 6px;
  background: #f8f9fa;
  padding: 4px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
}

/* Base de los botones cuadrados */
.layer-icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  color: #64748b; /* Color inactivo */
}

.layer-icon-btn svg {
  width: 16px;
  height: 16px;
}

/* Efectos Hover */
.layer-icon-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.layer-icon-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #f8f9fa; /* Fondo grisáceo para indicar inactividad */
}

/* Evitar que haga el efecto de saltito (hover) si está bloqueado */
.layer-icon-btn:disabled:hover {
  transform: none;
  box-shadow: none;
}

/* --- ESTADOS ACTIVOS (COLORIDOS) --- */

/* Ojo (Ver todas) */
.layer-icon-btn.active {
  background: #1e293b;
  border-color: #1e293b;
  color: white;
  box-shadow: 0 2px 8px rgba(30, 41, 59, 0.3);
}

/* Núcleos (Azul) */
.layer-icon-btn.btn-nucleo.active {
  background: #e3f2fd;
  border-color: #1e88e5;
  color: #1e88e5;
  box-shadow: 0 2px 8px rgba(30, 136, 229, 0.2);
}

/* Membranas (Verde) */
.layer-icon-btn.btn-membrana.active {
  background: #e8f5e9;
  border-color: #4caf50;
  color: #2e7d32;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
}

/* Micronúcleos (Morado) */
.layer-icon-btn.btn-micronucleo.active {
  background: #f3e5f5;
  border-color: #ab47bc;
  color: #8e24aa;
  box-shadow: 0 2px 8px rgba(171, 71, 188, 0.2);
}

.tipo-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ========================================= */
/* ESTILOS PARA EL REPORTE PDF (OCULTO) */
/* ========================================= */
.pdf-offscreen-container {
  position: absolute;
  left: -9999px;
  top: -9999px;
}
.pdf-document {
  width: 800px;
  background: white;
  color: #2c3e50;
  font-family: "Helvetica", "Arial", sans-serif;
}
.pdf-page {
  padding: 20px 30px;
  page-break-after: always;
}
.pdf-header h2 {
  margin: 0 0 5px 0;
  color: #1e3c72;
}
.pdf-header p {
  margin: 0 0 10px 0;
  color: #6b7280;
  font-size: 14px;
}
.pdf-image-wrapper {
  position: relative;
  width: 100%;
  height: 400px; /* Tamaño fijo para la foto en el PDF */
  background: #f0f0f0;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.pdf-base-img,
.pdf-mask-img {
  position: absolute;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.pdf-mask-img {
  z-index: 2;
  opacity: 0.85;
}
.pdf-table-container h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #2c3e50;
}
.pdf-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.pdf-table th {
  background-color: #f8f9fa;
  color: #666;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #e0e0e0;
}
.pdf-table td {
  border-bottom: 1px solid #ddd;
  padding: 10px;
}

/* INDICADOR DE REVISIÓN EN MINIATURAS */
.review-indicator {
  position: absolute;
  bottom: 4px; /* Posición abajo */
  right: 4px; /* Posición derecha */
  background: #f59e0b; /* Amarillo/Naranja de alerta */
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50; /* Super importante para que no se esconda */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  border: 1.5px solid white;
  animation: pulseAlertYellow 2s infinite;
}

.review-indicator svg {
  width: 12px;
  height: 12px;
}

/* Borde amarillo en la miniatura cuando necesita revisión */
.thumb.needs-review {
  border-color: rgba(245, 158, 11, 0.5);
}
.thumb.needs-review.active {
  border-color: #f59e0b;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.4);
}

@keyframes pulseAlertYellow {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7);
  }
  70% {
    transform: scale(1.1);
    box-shadow: 0 0 0 4px rgba(245, 158, 11, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(245, 158, 11, 0);
  }
}
</style>
