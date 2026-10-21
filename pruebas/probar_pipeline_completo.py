
import json
from pathlib import Path

# Módulo de Melanie: voz a texto
from Lab7_S2T_Melanie.reconocimiento_voz import transcribir

# Módulo de Juliana: comprensión del lenguaje
from comprension import extraer_json

# Módulos de Sarah: respuesta y voz
from respuestas import generar_respuesta
from tts import sintetizar


# ========================================
# CONFIGURACIÓN DE ARCHIVOS
# ========================================

CARPETA = Path(__file__).resolve().parent

AUDIO_ENTRADA = (
    CARPETA
    / "Lab7_S2T_Melanie"
    / "audios_evaluacion"
    / "orden_001.wav"
)

ARCHIVO_JSON = CARPETA / "prediccion_final.json"


# ========================================
# PIPELINE COMPLETO
# ========================================

def ejecutar_pipeline(ruta_audio):

    # 1. RECONOCIMIENTO DE VOZ - MELANIE
    print("\n1. TRANSCRIBIENDO AUDIO...")

    transcripcion = transcribir(str(ruta_audio))

    print("TRANSCRIPCIÓN:")
    print(transcripcion)

    if not transcripcion.strip():
        raise ValueError(
            "No se reconoció texto en el audio."
        )

    # 2. COMPRENSIÓN DEL LENGUAJE - JULIANA
    print("\n2. PROCESANDO CON EL LLM...")

    resultado_json = extraer_json(transcripcion)

    print("JSON GENERADO:")
    print(resultado_json)

    # 3. GENERACIÓN DE RESPUESTA - SARAH
    print("\n3. GENERANDO RESPUESTA...")

    respuesta = generar_respuesta(
        resultado_json,
        transcripcion
    )

    print("RESPUESTA:")
    print(respuesta)

    # 4. SÍNTESIS DE VOZ - SARAH
    print("\n4. GENERANDO AUDIO CON PIPER...")

    archivo_audio = sintetizar(
        respuesta,
        "respuesta_final.wav"
    )

    print("AUDIO GENERADO:")
    print(archivo_audio)

    # 5. GUARDAR RESULTADOS EN JSON
    datos = json.loads(resultado_json)

    datos["transcripcion"] = transcripcion
    datos["respuesta"] = respuesta

    with open(
        ARCHIVO_JSON,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    print("\nJSON FINAL GUARDADO:")
    print(ARCHIVO_JSON)

    print("\nPROCESO COMPLETADO")

    return datos


# ========================================
# EJECUCIÓN
# ========================================

if __name__ == "__main__":

    ejecutar_pipeline(AUDIO_ENTRADA)
