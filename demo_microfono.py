
import json
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from Lab7_S2T_Melanie.reconocimiento_voz import transcribir
from comprension import extraer_json
from respuestas import generar_respuesta
from tts import sintetizar


# ==========================================
# CONFIGURACION
# ==========================================

CARPETA = Path(__file__).resolve().parent

FRECUENCIA = 16000
DURACION = 6

AUDIO_TEMPORAL = CARPETA / "microfono_temporal.wav"


# ==========================================
# 1. GRABAR DESDE EL MICROFONO
# ==========================================

def grabar_microfono():

    print("\n🎤 HABLA AHORA...")
    print(f"Grabando durante {DURACION} segundos.")

    audio = sd.rec(
        int(DURACION * FRECUENCIA),
        samplerate=FRECUENCIA,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    sf.write(
        str(AUDIO_TEMPORAL),
        audio,
        FRECUENCIA
    )

    print("Grabacion finalizada.")

    return str(AUDIO_TEMPORAL)


# ==========================================
# 2. EJECUTAR PIPELINE COMPLETO
# ==========================================

def ejecutar():

    # MELANIE: Voz a texto
    ruta_audio = grabar_microfono()

    print("\n1. TRANSCRIBIENDO...")

    texto = transcribir(ruta_audio)

    print("TRANSCRIPCION:", texto)

    if not texto.strip():
        print("No se detecto ninguna frase.")
        return

    # JULIANA: Comprension con LLM
    print("\n2. PROCESANDO CON LLM...")

    resultado_json = extraer_json(texto)

    print("JSON:", resultado_json)

    # SARAH: Generar respuesta
    print("\n3. GENERANDO RESPUESTA...")

    respuesta = generar_respuesta(
        resultado_json,
        texto
    )

    print("RESPUESTA:", respuesta)

    # SARAH: Convertir a voz
    print("\n4. GENERANDO AUDIO...")

    archivo_audio = sintetizar(
        respuesta,
        "respuesta_final.wav"
    )

    print("AUDIO:", archivo_audio)

    
    # Reproducir automáticamente la respuesta
    print("\nREPRODUCIENDO RESPUESTA...")

    audio_respuesta, frecuencia = sf.read(archivo_audio)

    sd.play(audio_respuesta, frecuencia)
    sd.wait()

    print("Respuesta hablada finalizada.")


    # Guardar resultado JSON
    datos = json.loads(resultado_json)

    datos["transcripcion"] = texto
    datos["respuesta"] = respuesta

    with open(
        CARPETA / "prediccion_final.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    print("\nPROCESO COMPLETADO")


# ==========================================
# 3. DEMOSTRACION
# ==========================================

if __name__ == "__main__":

    while True:

        opcion = input(
            "\nPresiona ENTER para hablar "
            "o escribe salir: "
        )

        if opcion.strip().lower() == "salir":
            break

        try:
            ejecutar()
        except Exception as error:
            print("ERROR:", error)
