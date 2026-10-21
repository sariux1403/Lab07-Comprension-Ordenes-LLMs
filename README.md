# Laboratorio 7 — Comprensión de órdenes en español para robots

**Asignatura:** NLP y LLMs · **Integrantes:** Melanie, Juliana y Sarah.

## Componentes

- **Melanie:** `Lab7_S2T_Melanie/reconocimiento_voz.py` — Whisper Base INT8 CPU, audio WAV → transcripción.
- **Juliana:** `comprension.py` — LLM Qwen local mediante Ollama, transcripción → JSON con acciones y entidades.
- **Sarah:** `respuestas.py` — JSON + transcripción → confirmación o aclaración escrita.
- **Sarah:** `tts.py` — Piper `es_ES-davefx-medium` → archivo WAV.
- **Integración:** `predecir.py` procesa archivos o carpetas, y `demo_microfono.py` es para sustentación con micrófono.

## Requisitos

- Python 3.x compatible con las bibliotecas de `requirements.txt` (el equipo probó Python 3.14 en Windows).
- Ollama instalado y ejecutándose localmente. Descargar el modelo de Juliana **antes** de trabajar sin conexión:
  `ollama pull qwen2.5:1.5b-instruct-q4_K_M`
- Micrófono y parlantes para la demo en vivo; autorización de micrófono en Windows.
- Tras descargar el repositorio, descargar **primero** los archivos grandes Whisper (`model.bin`) y Piper (`es_ES-davefx-medium.onnx`) con los comandos de abajo. Los archivos de configuración pequeños sí están en GitHub.
- La inferencia se configura para CPU. Internet solo para instalar dependencias/obtener Ollama y su modelo por primera vez.

## Instalación de Python

En una terminal ubicada dentro de esta carpeta:

```bash
python -m pip install -r requirements.txt
```

No se incluye el ejecutable de Ollama ni el modelo Qwen dentro del ZIP. Se instalan con `ollama pull` antes de ejecutar; comprueba `ollama list`.

## Descargar modelos antes de ejecutar (una sola vez)

GitHub no admite cargar `model.bin` (aprox. 145 MB) mediante un repositorio convencional y la voz Piper tiene más de 25 MiB. Para que el repositorio sea fácil de subir desde el navegador, **los dos archivos grandes no se incluyen**. Se descargan una sola vez con conexión y luego las inferencias funcionan localmente sin internet.

Ejecuta los siguientes comandos **desde la raíz del repositorio**, después de instalar las dependencias:

**Whisper Base (formato CTranslate2 empleado por el módulo de Melanie):**

```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Systran/faster-whisper-base', local_dir='Lab7_S2T_Melanie/modelos/whisper-base', allow_patterns=['config.json','model.bin','tokenizer.json','vocabulary.txt'])"
```

**Piper (voz española):**

```bash
python -m piper.download_voices es_ES-davefx-medium
```

**Qwen en Ollama:**

```bash
ollama pull qwen2.5:1.5b-instruct-q4_K_M
```

Comprueba que estén `Lab7_S2T_Melanie/modelos/whisper-base/model.bin`, `es_ES-davefx-medium.onnx` y `es_ES-davefx-medium.onnx.json`. La descarga de Qwen se mantiene en el almacenamiento local de Ollama, no dentro de este repositorio. Evita cargar los archivos grandes directamente con **Add file → Upload files**. Si el equipo decide versionar modelos, necesitará configurar Git LFS mediante Git, en vez del procedimiento web.

## Predicción por lote (comando exigido por la guía)

Desde la raíz de la carpeta descomprimida:

```bash
python predecir.py --entrada Lab7_S2T_Melanie/audios_evaluacion/ --salida predicciones.json
```

También puedes usar el comando literal de la guía si creas tu carpeta `audios/`:

```bash
python predecir.py --entrada audios/ --salida predicciones.json
```

El programa procesa los WAV de la carpeta y guarda **una lista JSON** en `predicciones.json`; cada elemento incluye `archivo`, `transcripcion`, `acciones`, `respuesta` y `audio_respuesta`. Los audios sintetizados se guardan en `respuestas_audio/`. Si falla algún audio, se informa por pantalla, se guardan los éxitos y termina con código de error.

## Demostración hablada en vivo

```bash
python demo_microfono.py
```

Presiona **Enter**: se graba del micrófono durante 6 segundos, Whisper transcribe, Qwen extrae acciones, el generador construye la respuesta y Piper la reproduce automáticamente. Escribe `salir` para terminar. La aplicación crea `microfono_temporal.wav`, `prediccion_final.json` y `respuesta_final.wav` en la raíz.

**Limitación:** es una captura temporizada; no usa escucha permanente ni activación por voz. Se puede ampliar el tiempo cambiando `DURACION` en `demo_microfono.py`.

## Estructura

```text
LAB07_Entrega_Organizada/
  README.md
  requirements.txt
  predecir.py
  demo_microfono.py
  comprension.py
  respuestas.py
  tts.py
  es_ES-davefx-medium.onnx (descarga inicial; no en GitHub)
  es_ES-davefx-medium.onnx.json
  Lab7_S2T_Melanie/
    reconocimiento_voz.py
    requirements.txt
    README.md
    modelos/whisper-base/  (model.bin se descarga por separado)
    audios_evaluacion/
    anotaciones_ordenes.json
    *.csv  (resultados y métricas S2T)
  pruebas/ (scripts de prueba de desarrollo)
```

## Evaluación y límites conocidos

- El módulo S2T de Melanie evaluó 10 órdenes. Su README reporta WER 18,03 % con Whisper Base y 21,31 % con Vosk Small en ese experimento; no extrapolar como resultados del sistema completo.
- El JSON depende de que Whisper transcriba bien y de que Qwen extraiga correctamente las entidades. Un error de transcripción puede propagarse a la respuesta hablada.
- El generador de respuestas usa reglas gramaticales aproximadas y no corrige todos los problemas de interpretación del LLM.
- No se garantiza el rendimiento de latencia/RAM solo con esta carpeta: debe medirse con el equipo de referencia.
- **Entregables adicionales pendientes:** informe final de 4 páginas, evidencia de comparación de tres LLM, 30 órdenes nuevas grabadas y anotadas por equipo y demo de 5 minutos. No se incluyeron en el ZIP recibido, salvo los 10 audios y métricas S2T de Melanie.

## Créditos de módulos

Código de cada participante preservado; solamente se agregaron `predecir.py`, este README y un `requirements.txt` unificado. Los scripts `probar_*.py` se movieron a `pruebas/` para referencia (sus rutas de ejecución originales pueden requerir ejecutar desde la raíz del proyecto o ajustarse si se reutilizan). Los archivos de caché y las salidas temporales de desarrollo no se incluyen.

## Nota para el docente

Repositorio: código fuente, guía de instalación, ejemplos de audio y resultados S2T. Los pesos Whisper y Piper no se incluyen por tamaño; se descargan una sola vez antes de realizar inferencia sin conexión. El archivo `predecir.py` y su flujo por lotes deben verificarse en el equipo evaluador. El script `demo_microfono.py` requiere un micrófono en funcionamiento.
