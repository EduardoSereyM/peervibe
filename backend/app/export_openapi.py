"""Exporta el OpenAPI de la aplicación sin servidor ni HTTP (ARQ-010, SEC-019).

`create_app` no publica el OpenAPI, así que el generador del cliente lo obtiene con
`app.openapi()`. Uso: `python -m app.export_openapi openapi.json`; con `--check` no escribe y
falla si el archivo difiere de lo que genera la aplicación.
"""

import argparse
import json
import pathlib
import sys

from app.main import create_app

REGENERATE_COMMAND = "npm run generate:client"


def render_openapi() -> str:
    """OpenAPI en JSON estable (claves ordenadas), para que el diff sea reproducible."""
    spec = create_app().openapi()
    return json.dumps(spec, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Exporta el OpenAPI de la aplicación.")
    parser.add_argument("output", type=pathlib.Path, help="archivo JSON de destino")
    parser.add_argument(
        "--check",
        action="store_true",
        help="no escribe: sale con código 1 si el archivo no coincide con la aplicación",
    )
    args = parser.parse_args(argv)
    rendered = render_openapi()
    if not args.check:
        args.output.write_text(rendered, encoding="utf-8")
        return 0
    current = args.output.read_text(encoding="utf-8") if args.output.is_file() else None
    if current == rendered:
        return 0
    sys.stderr.write(
        f"{args.output} no coincide con el OpenAPI de la aplicación. "
        f"Ejecuta `{REGENERATE_COMMAND}`.\n"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
