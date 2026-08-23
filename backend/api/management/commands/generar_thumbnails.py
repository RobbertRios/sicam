from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import os

from api.models import Muestra  # 👈 tu app es api


class Command(BaseCommand):
    help = 'Genera thumbnails para muestras antiguas'

    def handle(self, *args, **kwargs):
        muestras = Muestra.objects.filter(thumbnail__isnull=True)

        if not muestras.exists():
            self.stdout.write(self.style.SUCCESS('No hay thumbnails pendientes 🎉'))
            return

        for muestra in muestras:
            try:
                if not muestra.ruta_imagen:
                    continue

                img_path = muestra.ruta_imagen.path
                img = Image.open(img_path)

                img.thumbnail((300, 300))

                base_name = os.path.basename(muestra.ruta_imagen.name)
                thumb_name = f"thumb_{base_name}"

                thumb_relative_path = os.path.join('thumbnails', thumb_name)
                thumb_full_path = os.path.join(settings.MEDIA_ROOT, thumb_relative_path)

                os.makedirs(os.path.dirname(thumb_full_path), exist_ok=True)

                img.save(thumb_full_path)

                muestra.thumbnail = thumb_relative_path
                muestra.save(update_fields=['thumbnail'])

                self.stdout.write(
                    self.style.SUCCESS(f'Thumbnail generado para Muestra {muestra.id_muestra}')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error en muestra {muestra.id_muestra}: {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS('Proceso finalizado 🚀'))