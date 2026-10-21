# Laboratorio 7 - Módulo de reconocimiento de voz (S2T)

## Descripción

Módulo de reconocimiento de órdenes habladas en español para
un sistema robótico basado en modelos de lenguaje ligeros.

Implementa Whisper Base mediante faster-whisper, utilizando
CPU, cuantización INT8 y beam_size=3.

Se evaluó frente a Vosk Small Spanish utilizando diez
grabaciones propias.

## Requisitos

- Python compatible con las dependencias instaladas
- CPU
- Memoria RAM suficiente
- Modelo Whisper Base incluido en modelos/whisper-base/

## Instalación

Desde la carpeta principal del proyecto:

```bash
python -m pip install -r requirements.txt
```

La instalación requiere conexión para descargar las
dependencias que no estén disponibles localmente.

## Estructura principal

- reconocimiento_voz.py: módulo de transcripción
- requirements.txt: dependencias
- modelos/whisper-base/: archivos del modelo
- audios_evaluacion/: diez grabaciones WAV
- anotaciones_ordenes.json: anotaciones de referencia
- resultados_whisper_vosk.csv: resultados por orden
- metricas_globales_s2t.csv: métricas generales
- optimizacion_whisper_cpu.csv: comparación de beam_size
- analisis_errores_s2t.csv: errores de reconocimiento

## Ejemplo de uso

```python
from reconocimiento_voz import transcribir

texto = transcribir("audios_evaluacion/orden_003.wav")
print(texto)
```

La función recibe la ruta de un archivo de audio WAV
y devuelve una cadena de texto en español.

El modelo se carga una sola vez y puede reutilizarse
para procesar múltiples archivos.

## Ejecución sin Internet

El modelo se carga desde la carpeta local
modelos/whisper-base/ con local_files_only=True.

No se requieren descargas del modelo durante la inferencia
si todos sus archivos están presentes.

La instalación de las dependencias debe completarse antes
de desconectar el equipo.

## Resultados experimentales

Se evaluaron diez órdenes en español de cinco niveles.

| Métrica | Whisper Base | Vosk Small |
|---|---:|---:|
| WER global | 18.03 % | 21.31 % |
| Latencia mediana inicial | 2.65 s | 0.91 s |
| Pico RAM observado | 494.31 MB | 236.71 MB |

Los tiempos y la memoria corresponden al entorno
experimental utilizado y pueden variar en otros equipos.

La configuración beam_size=3 obtuvo un WER global de
18.03 % y una latencia mediana de 2.48 segundos.

## Limitaciones

- El WER se evaluó solamente sobre diez grabaciones.
- Los resultados no garantizan igual precisión con otras voces.
- El pico de RAM se midió mediante muestreo.
- La ejecución completamente desconectada y la
  integración final deben validarse en el equipo de destino.
- El módulo devuelve texto; el LLM debe encargarse de
  identificar acciones, objetos, personas y lugares.

## Integración

El módulo entrega una cadena de texto que puede enviarse
al componente de comprensión de órdenes desarrollado
por otro integrante del equipo.
