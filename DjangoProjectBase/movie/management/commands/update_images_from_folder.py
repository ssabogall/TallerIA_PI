import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Assign images from media/movie/images/ to movies in the database"

    def handle(self, *args, **kwargs):
        # ✅ Carpeta de imágenes
        images_folder = os.path.join("media", "movie", "images")

        if not os.path.exists(images_folder):
            self.stderr.write(self.style.ERROR(f"Folder not found: {images_folder}"))
            return

        # ✅ Crear un diccionario con las imágenes disponibles
        available_images = {f.lower(): f for f in os.listdir(images_folder) if f.endswith((".png", ".jpg", ".jpeg"))}

        updated_count = 0
        not_found = []

        # ✅ Recorrer todas las películas
        for movie in Movie.objects.all():
            # Nombre esperado (ejemplo: m_Titanic.png → titanic)
            expected_filename = f"m_{movie.title}.png".lower()

            if expected_filename in available_images:
                relative_path = os.path.join("movie", "images", available_images[expected_filename])

                # Actualizar solo si está vacío o diferente
                if movie.image != relative_path:
                    movie.image = relative_path
                    movie.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title} → {relative_path}"))
            else:
                not_found.append(movie.title)

        self.stdout.write(self.style.SUCCESS(f"\n✅ Process finished: {updated_count} movies updated."))

        if not_found:
            self.stdout.write(self.style.WARNING(f"⚠️ No image found for {len(not_found)} movies: {', '.join(not_found)}"))
