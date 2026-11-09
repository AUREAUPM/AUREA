# Explicación intuitiva del Teorema Central del Límite

Recurso para **Estadística y Optimización**, Grado en Ingeniería Civil y Territorial. Proyecto AUREA: Aprendizaje y Uso del Razonamiento Estadístico y la Aleatoriedad (IE26.0405), financiado por la Universidad Politécnica de Madrid.

- [Usar el simulador en línea](https://blogs.upm.es/pie-aurea/).

## Estado y ubicación prevista

Primera incorporación al repositorio: 9 de noviembre de 2026, a partir del paquete preparado el 6 de noviembre. Código de la beta local del simulador.

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

## Licencia

La licencia del código está pendiente de definir. Se mantienen las licencias propias de ManimGL y sus dependencias.
