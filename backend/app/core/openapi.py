"""Convención de `operationId` del OpenAPI (ARQ-010, NOM-001, NOM-002)."""

from fastapi.routing import APIRoute


def operation_id(route: APIRoute) -> str:
    """`{tag}_{función}`: el tag es el módulo y la función, la del endpoint en su `router.py`.

    El prefijo del módulo evita choques entre módulos con funciones del mismo nombre. Las rutas
    sin tag (las de `core`, como `/health`) usan solo la función. Los módulos base van en inglés
    con funciones en inglés y los de dominio en español con funciones en español, para que el
    identificador no mezcle idiomas.
    """
    if route.tags:
        return f"{route.tags[0]}_{route.name}"
    return route.name
