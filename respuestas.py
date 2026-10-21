
import json
import re
import unicodedata


# ======================================
# RECUPERAR ARTÍCULOS
# ======================================

def describir_entidad(entidad, transcripcion):

    nombre = entidad.get("nombre", "").strip()
    adjetivos = entidad.get("adjetivos", [])

    if not nombre:
        return ""

    patron = (
        r"\b(el|la|los|las|un|una|unos|unas)\s+"
        + re.escape(nombre)
        + r"\b"
    )

    coincidencia = re.search(
        patron, transcripcion, re.IGNORECASE
    )

    articulo = (
        coincidencia.group(1).lower()
        if coincidencia else ""
    )

    return " ".join(
        p for p in [articulo, nombre, *adjetivos] if p
    )


# ======================================
# RECUPERAR PREPOSICIONES DE LUGARES
# ======================================

def describir_lugar(lugar, transcripcion):

    descripcion = describir_entidad(
        lugar, transcripcion
    )

    nombre = lugar.get("nombre", "").strip()

    if not descripcion or not nombre:
        return ""

    patron = (
        r"\b(a|en|hacia|hasta|desde|de|sobre)\s+"
        r"(?:(?:el|la|los|las)\s+)?"
        + re.escape(nombre)
        + r"\b"
    )

    coincidencia = re.search(
        patron, transcripcion, re.IGNORECASE
    )

    if coincidencia:
        preposicion = coincidencia.group(1).lower()
        return f"{preposicion} {descripcion}"

    return descripcion


# ======================================
# NUEVO: COMPARAR DOS OBJETOS
# ======================================

def misma_entidad(primera, segunda):

    def normalizar(cadena):
        return unicodedata.normalize(
            "NFC", cadena
        ).strip().casefold()

    nombre_1 = normalizar(primera.get("nombre", ""))
    nombre_2 = normalizar(segunda.get("nombre", ""))

    adjetivos_1 = [
        normalizar(a)
        for a in primera.get("adjetivos", [])
    ]

    adjetivos_2 = [
        normalizar(a)
        for a in segunda.get("adjetivos", [])
    ]

    return (
        nombre_1 == nombre_2
        and adjetivos_1 == adjetivos_2
    )


# ======================================
# NUEVO: OBTENER PRONOMBRE DEL OBJETO
# ======================================

def pronombre_objeto(entidad, transcripcion):

    nombre = entidad.get("nombre", "").strip()

    if not nombre:
        return None

    patron = (
        r"\b(el|la|los|las|un|una|unos|unas)\s+"
        + re.escape(nombre)
        + r"\b"
    )

    coincidencia = re.search(
        patron, transcripcion, re.IGNORECASE
    )

    if not coincidencia:
        return None

    articulos_pronombres = {
        "el": "lo",
        "un": "lo",
        "la": "la",
        "una": "la",
        "los": "los",
        "unos": "los",
        "las": "las",
        "unas": "las"
    }

    articulo = coincidencia.group(1).lower()

    return articulos_pronombres.get(articulo)


# ======================================
# GENERADOR PRINCIPAL DE RESPUESTAS
# ======================================

def generar_respuesta(json_str, transcripcion=""):

    if isinstance(json_str, str):
        datos = json.loads(json_str)
    else:
        datos = json_str

    acciones = datos.get("acciones", [])

    if not acciones:
        return "No he identificado ninguna instrucción."

    respuestas = []

    # Guardar la acción anterior
    anterior = None

    for accion in acciones:

        verbo = accion.get("accion", "").strip().lower()
        objetos = accion.get("objetos", [])
        personas = accion.get("personas", [])
        lugares = accion.get("lugares", [])

        if not verbo:
            continue

        # ======================================
        # MANEJAR ÓRDENES AMBIGUAS
        # ======================================

        if not objetos and not personas and not lugares:

            patron_ambiguo = (
                r"\b(eso|esto|aquello|ese|esa|"
                r"aquel|aquella)\b"
            )

            if re.search(
                patron_ambiguo,
                transcripcion,
                re.IGNORECASE
            ):
                return "¿A qué objeto o lugar te refieres?"

            respuestas.append(verbo)
            anterior = accion
            continue

        partes = []
        reemplazar = False

        # ======================================
        # NUEVO: EVITAR REPETIR OBJETOS
        # ======================================

        if (
            anterior
            and len(objetos) == 1
            and len(anterior.get("objetos", [])) == 1
        ):

            objeto_actual = objetos[0]
            objeto_anterior = anterior["objetos"][0]

            if misma_entidad(
                objeto_anterior, objeto_actual
            ):

                pronombre = pronombre_objeto(
                    objeto_actual, transcripcion
                )

                if pronombre:
                    partes.append(verbo + pronombre)
                    reemplazar = True

        # Si no se pudo reemplazar,
        # escribir el objeto completo
        if not reemplazar:

            partes.append(verbo)

            for objeto in objetos:

                descripcion = describir_entidad(
                    objeto, transcripcion
                )

                if descripcion:
                    partes.append(descripcion)

        # ======================================
        # AGREGAR LUGARES
        # ======================================

        for lugar in lugares:

            descripcion = describir_lugar(
                lugar, transcripcion
            )

            if descripcion:
                partes.append(descripcion)

        # ======================================
        # AGREGAR PERSONAS
        # ======================================

        for persona in personas:

            descripcion = describir_entidad(
                persona, transcripcion
            )

            if descripcion:

                if descripcion.startswith("el "):
                    partes.append(
                        "al " + descripcion[3:]
                    )
                else:
                    partes.append(
                        "a " + descripcion
                    )

        respuestas.append(" ".join(partes))

        # Actualizar la acción anterior
        anterior = accion

    if not respuestas:
        return "No he identificado ninguna instrucción."

    # Unir las acciones naturalmente
    if len(respuestas) == 1:
        return "Voy a " + respuestas[0]

    return "Voy a " + " y después ".join(respuestas)


# ======================================
# PRUEBAS INDEPENDIENTES
# ======================================

if __name__ == "__main__":

    pruebas = [
        (
            "Lleva la taza roja a la cocina "
            "y entrégasela a María",
            [
                {
                    "accion": "llevar",
                    "objetos": [
                        {"nombre": "taza",
                         "adjetivos": ["roja"]}
                    ],
                    "personas": [],
                    "lugares": [
                        {"nombre": "cocina",
                         "adjetivos": []}
                    ]
                },
                {
                    "accion": "entregar",
                    "objetos": [
                        {"nombre": "taza",
                         "adjetivos": ["roja"]}
                    ],
                    "personas": [
                        {"nombre": "María",
                         "adjetivos": []}
                    ],
                    "lugares": []
                }
            ]
        ),
        (
            "Busca el libro y llévalo a la sala",
            [
                {
                    "accion": "buscar",
                    "objetos": [
                        {"nombre": "libro",
                         "adjetivos": []}
                    ],
                    "personas": [],
                    "lugares": []
                },
                {
                    "accion": "llevar",
                    "objetos": [
                        {"nombre": "libro",
                         "adjetivos": []}
                    ],
                    "personas": [],
                    "lugares": [
                        {"nombre": "sala",
                         "adjetivos": []}
                    ]
                }
            ]
        ),
        (
            "Recoge las carpetas y entrégalas a Carlos",
            [
                {
                    "accion": "recoger",
                    "objetos": [
                        {"nombre": "carpetas",
                         "adjetivos": []}
                    ],
                    "personas": [],
                    "lugares": []
                },
                {
                    "accion": "entregar",
                    "objetos": [
                        {"nombre": "carpetas",
                         "adjetivos": []}
                    ],
                    "personas": [
                        {"nombre": "Carlos",
                         "adjetivos": []}
                    ],
                    "lugares": []
                }
            ]
        ),
        (
            "Tráeme eso",
            [
                {
                    "accion": "traer",
                    "objetos": [],
                    "personas": [],
                    "lugares": []
                }
            ]
        ),
        (
            "Espera",
            [
                {
                    "accion": "esperar",
                    "objetos": [],
                    "personas": [],
                    "lugares": []
                }
            ]
        ),
        (
            "Qué demora la de hoy",
            []
        )
    ]

    for numero, (texto, acciones) in enumerate(
        pruebas, 1
    ):

        resultado = generar_respuesta(
            {"acciones": acciones},
            texto
        )

        print(f"\n===== PRUEBA {numero} =====")
        print("ORDEN:", texto)
        print("RESPUESTA:", resultado)
