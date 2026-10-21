
import wave
from pathlib import Path
from piper import PiperVoice

# Carpeta donde se encuentra este archivo
CARPETA = Path(__file__).resolve().parent

# Modelo de voz descargado
MODELO = CARPETA / "es_ES-davefx-medium.onnx"

# Cargar el modelo de voz
voz = PiperVoice.load(str(MODELO))


def sintetizar(texto, salida="respuesta.wav"):

    # Ubicación del archivo de salida
    ruta_salida = CARPETA / salida

    # Crear el archivo WAV con la voz sintetizada
    with wave.open(str(ruta_salida), "wb") as archivo:
        voz.synthesize_wav(texto, archivo)

    return str(ruta_salida)


# Prueba independiente
if __name__ == "__main__":

    texto = "Voy a llevar la botella verde a la cocina."

    print("TEXTO A SINTETIZAR:")
    print(texto)

    archivo_audio = sintetizar(texto)

    print("\nAUDIO GENERADO:")
    print(archivo_audio)
