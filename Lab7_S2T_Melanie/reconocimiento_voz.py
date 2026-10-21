
from pathlib import Path
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from faster_whisper import WhisperModel


class ReconocimientoVoz:
    """
    Módulo de reconocimiento de órdenes en español.

    Modelo: Whisper Base
    Hardware: CPU
    Cuantización: INT8
    Beam size: 3
    Inferencia: local, sin descargas automáticas
    """

    def __init__(self, ruta_modelo=None, beam_size=3):

        if ruta_modelo is None:
            ruta_modelo = (
                Path(__file__).resolve().parent
                / "modelos"
                / "whisper-base"
            )

        ruta_modelo = Path(ruta_modelo).resolve()

        if not ruta_modelo.is_dir():
            raise FileNotFoundError(
                f"No se encontró el modelo: {ruta_modelo}"
            )

        self.beam_size = beam_size

        self.modelo = WhisperModel(
            str(ruta_modelo),
            device="cpu",
            compute_type="int8",
            cpu_threads=2,
            local_files_only=True
        )

    def preparar_audio(self, ruta_audio):

        audio, frecuencia = sf.read(str(ruta_audio))

        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)

        if frecuencia != 16000:
            divisor = gcd(frecuencia, 16000)

            audio = resample_poly(
                audio,
                16000 // divisor,
                frecuencia // divisor
            )

        return np.asarray(audio, dtype=np.float32)

    def transcribir(self, ruta_audio):

        audio = self.preparar_audio(ruta_audio)

        segmentos, _ = self.modelo.transcribe(
            audio,
            language="es",
            beam_size=self.beam_size,
            vad_filter=True
        )

        return " ".join(
            segmento.text.strip()
            for segmento in segmentos
        ).strip()


_reconocedor = None


def transcribir(ruta_audio):
    """
    Recibe la ruta de un archivo WAV y devuelve
    su transcripción en español.
    """

    global _reconocedor

    if _reconocedor is None:
        _reconocedor = ReconocimientoVoz()

    return _reconocedor.transcribir(ruta_audio)
