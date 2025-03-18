""" This script takes the dataset in TIF format from the Photoacoustic_Microscopy_Dataset
    and converts it to PNG format. The dataset is available at:

    https://figshare.com/articles/dataset/Photoacoustic_Microscopy_Dataset/12871805

"""

from pathlib import Path
from PIL import Image
from wasabi import Printer
import numpy as np


class TifToPngConverter:
    """Clase para convertir imágenes TIF a PNG con normalización adecuada."""

    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.msg = Printer()  # Instancia de wasabi para mensajes

        # Crear directorio de salida si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert(self):
        """Convierte todas las imágenes TIF en el directorio de entrada a PNG."""
        tif_files = list(self.input_dir.glob("*.tif"))
        if not tif_files:
            self.msg.warn("No se encontraron archivos TIF para convertir.")
            return

        self.msg.info(f"Archivos encontrados: {len(tif_files)}")
        for tif_file in tif_files:
            self._convert_file(tif_file)

        self.msg.good("Conversión completada.")

    def _convert_file(self, tif_file: Path):
        """Convierte un archivo TIF a PNG con normalización."""
        try:
            with Image.open(tif_file) as img:
                # Convertir a un array NumPy para manipular los datos
                img_array = np.array(img)

                # Normalizar los valores al rango 0-255
                img_normalized = self._normalize_image(img_array)

                # Convertir de vuelta a imagen PIL en escala de grises
                img_normalized = Image.fromarray(img_normalized.astype("uint8"), mode="L")

                output_file = self.output_dir / f"{tif_file.stem}.png"
                img_normalized.save(output_file, format="PNG")
                self.msg.good(f"Convertido: {tif_file.name} -> {output_file.name}")
        except Exception as e:
            self.msg.fail(f"Error al procesar {tif_file.name}: {e}")

    @staticmethod
    def _normalize_image(img_array: np.ndarray) -> np.ndarray:
        """Normaliza la imagen al rango 0-255."""
        img_min = img_array.min()
        img_max = img_array.max()
        if img_max > img_min:  # Evitar división por cero
            img_normalized = 255 * (img_array - img_min) / (img_max - img_min)
        else:
            img_normalized = np.zeros_like(img_array)  # Si la imagen es uniforme, devolver negro
        return img_normalized


if __name__ == "__main__":
    # Definir rutas de entrada y salida
    INPUT_DIR = Path(
        r"C:\Users\zned897\Documents\GitHub\ai4arthritisra\data\datasets\12871805"
    )
    OUTPUT_DIR = Path(
        r"C:\Users\zned897\Documents\GitHub\ai4arthritisra\data\converted_images"
    )

    # Crear instancia de la clase y ejecutar la conversión
    converter = TifToPngConverter(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR)
    converter.convert()


