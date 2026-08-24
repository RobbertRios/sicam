from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
import traceback
import asyncio

from app.services.segmentador import segmentar_pipeline
from app.utils.poligonos import obtener_poligonos_desde_mascara

router = APIRouter()

# Aquí está el cambio: El semáforo permite hasta 3 imágenes simultáneas
semaforo_procesamiento = asyncio.Semaphore(3)

@router.post("/segmentar")
async def segmentar(file: UploadFile = File(...)):
    """
    Recibe una imagen de saliva y retorna los polígonos de membranas,
    núcleos y micronúcleos detectados.

    El procesamiento corre en un thread separado y está protegido por un
    semáforo para permitir un máximo de 3 tareas concurrentes.
    """
    try:
        contenido = await file.read()

        # Las imágenes pasan en grupos de máximo 3; las demás esperan su turno
        async with semaforo_procesamiento:
            resultado = await run_in_threadpool(segmentar_pipeline, contenido)

        objetos = []
        objetos += obtener_poligonos_desde_mascara(resultado["membranas"], "membrana")
        objetos += obtener_poligonos_desde_mascara(resultado["nucleos"], "nucleo")
        objetos += obtener_poligonos_desde_mascara(resultado["micronucleos"], "micronucleo")

        return {"objetos": objetos}

    except Exception as e:
        print("\n ERROR EN SEGMENTACIÓN")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))