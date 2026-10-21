
from comprension import extraer_json
from respuestas import generar_respuesta

# Orden que queremos procesar
transcripcion = "Lleva la botella verde a la cocina"

print("ORDEN ORIGINAL:")
print(transcripcion)

# Juliana: convertir texto en JSON
print("\nProcesando con el LLM...")

resultado_json = extraer_json(transcripcion)

print("\nJSON GENERADO:")
print(resultado_json)

# Sarah: convertir JSON en respuesta natural
respuesta = generar_respuesta(
    resultado_json,
    transcripcion
)

print("\nRESPUESTA GENERADA:")
print(respuesta)
