
from comprension import extraer_json
from respuestas import generar_respuesta
from tts import sintetizar

# ==========================================
# INTEGRACION JULIANA + SARAH + PIPER
# ==========================================

# 1. Orden recibida
transcripcion = "Busca el libro azul y llévalo a la oficina"

print("1. ORDEN ORIGINAL:")
print(transcripcion)

# 2. Comprension mediante LLM
print("\n2. PROCESANDO CON EL LLM...")

resultado_json = extraer_json(transcripcion)

print("\nJSON GENERADO:")
print(resultado_json)

# 3. Generacion de respuesta natural
respuesta = generar_respuesta(
    resultado_json,
    transcripcion
)

print("\n3. RESPUESTA GENERADA:")
print(respuesta)

# 4. Conversion de texto a voz
print("\n4. GENERANDO AUDIO CON PIPER...")

archivo_audio = sintetizar(
    respuesta,
    "respuesta_final.wav"
)

print("\nAUDIO GENERADO CORRECTAMENTE:")
print(archivo_audio)

print("\nPROCESO FINALIZADO")
