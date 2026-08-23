# Guía de instalación — Sistema de Segmentación (Saliva + Sangre)

Esta guía te permite levantar el proyecto completo desde cero, sin necesidad de tener Python, Anaconda, ni ninguna dependencia instalada manualmente. Todo corre dentro de Docker.

---

## 1. Requisitos previos

Antes de empezar, instala en tu computadora:

1. **Docker Desktop** — descárgalo de [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) e instálalo (Windows, Mac o Linux). Ábrelo al menos una vez para confirmar que está corriendo (verás la ballena de Docker en la barra de tareas).

**Recursos mínimos recomendados:**
- Al menos **10 GB de espacio libre en disco** (las imágenes de Docker con PyTorch + los modelos de IA pesan varios GB por microservicio).
- Al menos **8 GB de RAM** asignados a Docker Desktop (revisa en Docker Desktop → Settings → Resources).
- **Conexión a internet estable** para el primer arranque (se descargan librerías y modelos de IA, ~2-3 GB en total).

---

## 2. Obtener el proyecto

**como ZIP**
Descarga el proyecto, descomprímelo, y abre una terminal dentro de esa carpeta (la que contiene el archivo `docker-compose.yml`).

---

## 3. Primer arranque (construir todo)

Desde la terminal, dentro de la carpeta del proyecto, corre:

```bash
docker-compose up --build
```

**Esto va a tardar bastante la primera vez — es normal.** Vas a ver mucho texto pasando en la terminal mientras Docker:
- Descarga las imágenes base de Python y PostgreSQL
- Instala las dependencias de cada servicio (PyTorch, Cellpose, Django, Vue, etc.)
- Descarga los modelos de inteligencia artificial preentrenados (esto pasa **una sola vez**, durante la construcción, no en cada arranque)

Dependiendo de tu conexión, esto puede tardar entre **15 y 40 minutos** la primera vez. Las siguientes veces será mucho más rápido porque Docker reutiliza lo ya construido.

> **Si el build falla a mitad de una descarga** (error tipo "PytorchStreamReader failed" o similar), normalmente es solo un corte de red. Vuelve a correr el mismo comando — Docker retoma desde donde se quedó y solo reintenta el paso que falló.

Cuando termine, deberías ver en la terminal los logs de los 5 servicios corriendo:
- `postgres-db`
- `django-app`
- `vue-app`
- `micro-saliva`
- `micro-sangre`

Déjalo corriendo así, y abre una **segunda terminal** para los siguientes pasos.

---

## 4. Verificar que todo esté arriba

En la segunda terminal, dentro de la misma carpeta del proyecto:

```bash
docker-compose ps
```

Deberías ver los 5 contenedores con estado `Up` (o `running`). Si alguno dice `Exit` o `Restarting`, revisa sus logs específicos:

```bash
docker-compose logs <nombre-del-servicio>
```

Por ejemplo: `docker-compose logs backend` o `docker-compose logs micro-saliva`.

---

## 5. Preparar la base de datos (si hace falta)

La primera vez que se levanta el proyecto, es posible que la base de datos esté vacía y Django necesite crear sus tablas. Comprueba primero si ya se hizo automáticamente:

```bash
docker-compose logs backend | grep -i migrat
```

- **Si ves líneas mencionando migraciones aplicadas** → ya está listo, sigue al paso 6.
- **Si no ves nada, o al abrir la aplicación ves errores de "tabla no existe"** → corre manualmente:

```bash
docker-compose exec backend python manage.py migrate
```

Si además necesitas un usuario administrador para entrar al panel de Django:

```bash
docker-compose exec backend python manage.py createsuperuser
```

(Te va a pedir usuario, correo y contraseña — ponle lo que quieras).

---

## 6. Usar la aplicación

Con todo arriba, abre en tu navegador:

| Servicio | URL |
|---|---|
| **Aplicación (frontend)** | http://localhost:5173 |
| **Panel de administración de Django** (si lo usas) | http://localhost:8000/admin |
| **API de Django** | http://localhost:8000/api/ |

Los microservicios de segmentación (`micro-saliva`, `micro-sangre`) **no están expuestos al exterior** por seguridad — solo el backend de Django puede hablarles internamente. No necesitas ni debes acceder a ellos directamente para usar la aplicación normal.

---

## 7. Apagar y volver a prender

**Para apagar todo** (sin borrar nada):
```bash
docker-compose down
```

**Para volver a prenderlo después** (ya no tarda, no vuelve a construir):
```bash
docker-compose up
```
o en segundo plano, sin ocupar la terminal:
```bash
docker-compose up -d
```

**Para ver los logs en vivo** de todo (si corriste con `-d`):
```bash
docker-compose logs -f
```
o de un solo servicio:
```bash
docker-compose logs -f backend
```

---

## 8. Si algo se actualiza (código nuevo)

Si te pasan una versión nueva del proyecto con cambios en el código:

```bash
docker-compose down
docker-compose up --build
```

El `--build` es importante si cambiaron dependencias (`requirements.txt`, `package.json`) o el `Dockerfile` de algún servicio. Si solo cambió código de la aplicación (no dependencias), a veces ni siquiera hace falta reconstruir, pero por seguridad siempre es buena idea usar `--build`.

---

## 9. Problemas comunes

**Docker no tiene suficiente memoria**
> Ve a Docker Desktop → Settings → Resources → aumenta la RAM a mínimo 6 GB

**El puerto 5173 o 8000 ya está en uso**
> Cierra otras aplicaciones que usen esos puertos o reinicia Docker

**El build falla a mitad**
> Vuelve a ejecutar `docker-compose up --build`, Docker retomará desde donde se quedó

**Los contenedores se detienen solos al inicio**
> Espera unos segundos y vuelve a ejecutar `docker-compose up` (sin --build). Django a veces intenta conectarse a la base de datos antes de que esté lista, pero se recupera solo.

**No hay datos en la base de datos**
> Baja la base de datos y ejecuta `docker exec -it postgres-db pg_restore -U postgres -d pruebas_web /backup_pruebas.sql` ya con el backup y el nombre que le pusiste. 

**Si tienes problemas con el backup, elimina y vuelve a crear la basde ded datos**
> Para Borrar la base de datos `docker exec -it postgres-db psql -U postgres -c "DROP DATABASE pruebas_web WITH (FORCE);`para volverla a crear y hacer de nuevo el backup `docker exec -it postgres-db psql -U postgres -c "CREATE DATABASE pruebas_web;`. 

## 10. Estructura del proyecto (referencia rápida)

```
proyecto_segmentacion/
├── docker-compose.yml       ← orquesta todos los servicios
├── backend/                 ← Django (API + lógica de negocio)
├── frontend/                ← Vue.js (interfaz de usuario)
├── micro-saliva/             ← Microservicio de segmentación de saliva (FastAPI + Cellpose)
└── micro-sangre/             ← Microservicio de segmentación de sangre (FastAPI + Cellpose)
```

Cada microservicio (`micro-saliva`, `micro-sangre`) es independiente: tiene su propio `Dockerfile`, `requirements.txt` y modelo de IA. Django los consume internamente vía HTTP, sin que el usuario final los vea directamente.
