
from pathlib import Path
from Lab7_S2T_Melanie.reconocimiento_voz import transcribir

# Carpeta principal del proyecto
CARPETA = Path(__file__).resolve().parent

# Audio de prueba incluido por Melanie
audio = (
    CARPETA
    / "Lab7_S2T_Melanie"
    / "audios_evaluacion"
    / "orden_001.wav"
)

print("INICIANDO RECONOCIMIENTO DE VOZ...")

# Convertir audio a texto
texto = transcribir(str(audio))

print("\nTRANSCRIPCIÓN GENERADA:")
print(texto)

print("\nPRUEBA FINALIZADA")
