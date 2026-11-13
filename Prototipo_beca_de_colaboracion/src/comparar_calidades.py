"""Renderiza una escena de Manim en varias calidades y compara resultados."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path
from time import perf_counter


CALIDADES = {
    "baja": {"flag": "l", "resolucion": "854x480", "fps": 15},
    "media": {"flag": "m", "resolucion": "1280x720", "fps": 30},
    "alta": {"flag": "h", "resolucion": "1920x1080", "fps": 60},
    "ultra": {"flag": "k", "resolucion": "3840x2160", "fps": 60},
}


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Renderiza una escena de Manim en varias calidades."
    )
    parser.add_argument(
        "--archivo",
        type=Path,
        default=Path("src/escena_final.py"),
        help="Archivo Python que contiene la escena.",
    )
    parser.add_argument(
        "--escena",
        default="EscenaDados",
        help="Nombre de la clase Scene que se va a renderizar.",
    )
    parser.add_argument(
        "--calidades",
        nargs="+",
        choices=CALIDADES,
        default=["baja", "media", "alta"],
        help="Calidades que se van a generar.",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("media/comparativa_calidades"),
        help="Directorio donde se guardaran videos y resumen CSV.",
    )
    return parser.parse_args()


def localizar_video(directorio, nombre_salida):
    candidatos = list(directorio.rglob(f"{nombre_salida}.mp4"))
    if not candidatos:
        candidatos = list(directorio.rglob("*.mp4"))
    if not candidatos:
        return None
    return max(candidatos, key=lambda ruta: ruta.stat().st_mtime)


def renderizar(archivo, escena, calidad, directorio_salida):
    datos = CALIDADES[calidad]
    directorio_calidad = directorio_salida / calidad
    directorio_calidad.mkdir(parents=True, exist_ok=True)
    nombre_salida = f"{escena}_{calidad}"

    comando = [
        sys.executable,
        "-m",
        "manim",
        f"-q{datos['flag']}",
        "--media_dir",
        str(directorio_calidad),
        "-o",
        nombre_salida,
        str(archivo),
        escena,
    ]

    print(f"\nRenderizando calidad {calidad} ({datos['resolucion']}, {datos['fps']} FPS)")
    inicio = perf_counter()
    resultado = subprocess.run(comando, check=False)
    segundos = perf_counter() - inicio

    video = localizar_video(directorio_calidad, nombre_salida)
    estado = "ok" if resultado.returncode == 0 and video else "error"
    tamano_mib = video.stat().st_size / (1024**2) if video else 0

    return {
        "calidad": calidad,
        "resolucion": datos["resolucion"],
        "fps": datos["fps"],
        "tiempo_segundos": round(segundos, 2),
        "tamano_mib": round(tamano_mib, 2),
        "estado": estado,
        "video": str(video.resolve()) if video else "",
    }


def guardar_resumen(resultados, ruta):
    campos = [
        "calidad",
        "resolucion",
        "fps",
        "tiempo_segundos",
        "tamano_mib",
        "estado",
        "video",
    ]
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)


def imprimir_resumen(resultados, ruta_csv):
    print("\nResumen")
    print(f"{'Calidad':<10} {'Resolucion':<12} {'FPS':>4} {'Tiempo':>12} {'Tamano':>12}")
    print("-" * 56)
    for resultado in resultados:
        print(
            f"{resultado['calidad']:<10} "
            f"{resultado['resolucion']:<12} "
            f"{resultado['fps']:>4} "
            f"{resultado['tiempo_segundos']:>9.2f} s "
            f"{resultado['tamano_mib']:>9.2f} MiB"
        )
        if resultado["video"]:
            print(f"  {resultado['video']}")
        else:
            print("  Render fallido; revisa el error de Manim mostrado arriba.")
    print(f"\nResumen CSV: {ruta_csv.resolve()}")


def main():
    args = parsear_argumentos()
    archivo = args.archivo.resolve()
    salida = args.salida.resolve()

    if not archivo.is_file():
        raise SystemExit(f"No existe el archivo de escena: {archivo}")

    salida.mkdir(parents=True, exist_ok=True)
    resultados = [
        renderizar(archivo, args.escena, calidad, salida)
        for calidad in args.calidades
    ]
    ruta_csv = salida / "resumen.csv"
    guardar_resumen(resultados, ruta_csv)
    imprimir_resumen(resultados, ruta_csv)

    if any(resultado["estado"] != "ok" for resultado in resultados):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
