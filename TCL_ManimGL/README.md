# Explicación intuitiva del Teorema Central del Límite

Autor: **David Fernández Álvarez**, Universidad Politécnica de Madrid.

Recurso para **Estadística y Optimización**, Grado en Ingeniería Civil y Territorial. Proyecto AUREA: Aprendizaje y Uso del Razonamiento Estadístico y la Aleatoriedad (IE26.0405), financiado por la Universidad Politécnica de Madrid.

- [Usar el simulador en línea](https://blogs.upm.es/pie-aurea/).
- [Leer la guía](documentacion/guia_usuario_tcl.pdf).
- [Editar la guía en LaTeX](documentacion/guia_usuario_tcl.tex).

## Estado y ubicación prevista

Primera incorporación al repositorio: 9 de noviembre de 2026, a partir del paquete preparado el 6 de noviembre. Guía v0.1, borrador para revisión; DOI aún no asignado.

Ubicación: `AUREA/TCL_ManimGL/`, al mismo nivel que la carpeta `AUREA/ManimGL/` que conserva el trabajo de Iván. No sustituir ni renombrar esa carpeta existente.

Los diez módulos Python son copias sin modificaciones de la beta local `TCL_Manim`. Su identidad queda recogida en `MANIFIESTO_SHA256.txt`. Se han comprobado su sintaxis y las importaciones internas por inspección estática; esta preparación documental no incluye una nueva prueba gráfica de ManimGL ni una instalación limpia multiplataforma.

## Ejecutar ManimGL

Entorno de referencia observado: Python 3.11.15 y ManimGL 1.7.2. Instalar los requisitos nativos indicados en la [documentación oficial](https://3b1b.github.io/manim/getting_started/installation.html). Este proyecto utiliza ManimGL, no Manim Community.

Desde esta carpeta, en macOS o Linux:

```sh
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
manimgl dados.py DemoInterfaz
```

En Windows, desde `cmd`:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
manimgl dados.py DemoInterfaz
```

El archivo requirements fija la versión principal de ManimGL; no bloquea todas las dependencias transitivas. Una futura edición reproducible debería conservar un listado completo del entorno probado.

## Compilar la guía

Abrir `documentacion/guia_usuario_tcl.tex` en TeXShop o un editor LaTeX. Mantener la carpeta `recursos` junto al `.tex`. Compilar con pdfLaTeX dos veces para actualizar el índice. No requiere conexión ni paquetes externos de ejecución de código.

## Pendientes editoriales

- Completar el nombre de Iván y describir su contribución con precisión.
- Confirmar la licencia de la guía: propuesta CC BY-NC 4.0.
- Decidir por separado la licencia del código.
- Cerrar una versión definitiva y añadir su identificador de revisión.
- Tramitar el depósito institucional e incorporar el DOI real cuando se asigne.

No se ha aplicado todavía una licencia definitiva a este paquete. La propuesta para la guía no modifica las licencias de ManimGL o de otros componentes.
