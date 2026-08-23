# ✅ DEBE SER LO PRIMERO — antes de cualquier import de numpy/torch/cellpose
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

from app.routers.segmentacion import router as segmentacion_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se ejecuta al arrancar y al apagar el servidor.
    La carga del modelo ocurre aquí, una sola vez, en un thread separado
    para no bloquear el event loop de asyncio mientras PyTorch inicializa.
    """
    from segmentacion_core.seg_pipeline_v2 import inicializar_modelo

    print("[main] Precargando modelo Cellpose al iniciar el servidor...")
    await run_in_threadpool(inicializar_modelo, gpu=False)
    print("[main] Modelo listo. Servidor disponible para recibir requests.")

    yield  # ← servidor corriendo

    print("[main] Servidor apagándose.")


app = FastAPI(
    title="Microservicio Segmentación Saliva",
    description="Segmentación de imágenes de saliva (membranas, núcleos, micronúcleos)",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(segmentacion_router)