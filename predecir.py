"""Laboratorio 7: archivo(s) WAV -> transcripción, JSON, respuesta y WAV.

Uso: python predecir.py --entrada audios/ --salida predicciones.json
"""
import argparse
import json
from pathlib import Path

from Lab7_S2T_Melanie.reconocimiento_voz import transcribir
from comprension import extraer_json
from respuestas import generar_respuesta
from tts import sintetizar

BASE = Path(__file__).resolve().parent


def procesar_audio(ruta, carpeta_audios):
    transcripcion = transcribir(str(ruta))
    if not transcripcion.strip():
        raise ValueError('La transcripción está vacía')

    json_texto = extraer_json(transcripcion)
    datos = json.loads(json_texto)
    respuesta = generar_respuesta(datos, transcripcion)
    nombre_audio = f'{ruta.stem}_respuesta.wav'
    archivo_audio = sintetizar(respuesta, f'respuestas_audio/{nombre_audio}')
    return {
        'archivo': ruta.name,
        'transcripcion': transcripcion,
        'acciones': datos['acciones'],
        'respuesta': respuesta,
        'audio_respuesta': str(Path(archivo_audio).relative_to(BASE))
    }


def main():
    parser = argparse.ArgumentParser(description='Predicciones de órdenes habladas en español')
    parser.add_argument('--entrada', required=True, help='Carpeta con archivos WAV o archivo WAV')
    parser.add_argument('--salida', required=True, help='Archivo JSON de salida')
    args = parser.parse_args()

    entrada = Path(args.entrada).expanduser().resolve()
    salida = Path(args.salida).expanduser().resolve()

    if entrada.is_dir():
        archivos = sorted(p for p in entrada.iterdir() if p.is_file() and p.suffix.lower()=='.wav')
    elif entrada.is_file() and entrada.suffix.lower()=='.wav':
        archivos = [entrada]
    else:
        parser.error('La entrada debe ser un archivo WAV o una carpeta existente')

    if not archivos:
        parser.error('No se encontraron archivos WAV en la entrada')

    (BASE/'respuestas_audio').mkdir(exist_ok=True)
    resultados = []
    errores = []

    for i, ruta in enumerate(archivos, 1):
        print(f'[{i}/{len(archivos)}] {ruta.name}', flush=True)
        try:
            pred = procesar_audio(ruta, BASE/'respuestas_audio')
            resultados.append(pred)
            print('  Transcripción:',pred['transcripcion'],flush=True)
            print('  Respuesta:',pred['respuesta'],flush=True)
        except Exception as exc:
            errores.append((ruta.name, str(exc)))
            print(f'  ERROR: {exc}',flush=True)

    salida.parent.mkdir(parents=True,exist_ok=True)
    with salida.open('w',encoding='utf-8') as f:
        json.dump(resultados,f,ensure_ascii=False,indent=2)
    print(f'Guardadas {len(resultados)} predicciones en {salida}')
    if errores:
        print(f'Fallaron {len(errores)} archivos. Revisa los mensajes anteriores.')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
