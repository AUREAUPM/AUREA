# TCL: aplicación web de AUREA

Simulador interactivo del Teorema Central del Límite. Proyecto AUREA, Universidad Politécnica de Madrid.

## Archivos

- `index.html`: aplicación completa lista para abrir en un navegador o alojar en un servidor estático. Incluye JavaScript y CSS; no necesita Python ni ManimGL.
- `fuentes/`: proyecto editable en TypeScript, HTML y CSS, con Vite y archivo de bloqueo de dependencias.

## Usar y publicar

La aplicación puede abrirse directamente con `index.html`. Para insertarla en WordPress se debe alojar en una URL HTTPS y usar esa URL en el bloque de inserción autorizado. Añadir `?embed=1` oculta la cabecera propia cuando la página de WordPress ya aporta el título.

La mera incorporación de esta carpeta al repositorio no activa GitHub Pages ni cambia la inserción actual de WordPress. Si Pages sirve la raíz de este repositorio, la ruta del recurso será `/AUREA/TCL_Web/`; debe comprobarse el alojamiento antes de actualizar el enlace de WordPress.

Accesos existentes:
- https://blogs.upm.es/pie-aurea/
- https://davidfernandezalv.github.io/aurea-tcl/

## Editar y reconstruir

Instalar Node.js compatible con Vite 8 y pnpm. Desde `fuentes/`:

```sh
pnpm install --frozen-lockfile
pnpm dev
```

Para comprobar TypeScript y generar la versión completa:

```sh
pnpm build:standalone
```

Esto regenera `TCL_Web/index.html`. Conservar ese archivo junto con sus fuentes al publicar los cambios. No editar el HTML empaquetado para cambiar la lógica: modificar `fuentes/src/main.ts` o `fuentes/src/style.css` y reconstruirlo.

La copia procede del proyecto local usado para la publicación personal. No se incluyen dependencias instaladas, datos personales ni la guía de usuario. La licencia del código está pendiente de definir; las dependencias conservan sus propias licencias.
