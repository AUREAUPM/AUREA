from manimlib import *
from collections import defaultdict
import numpy as np


class HistogramaSuma(VGroup):

    def __init__(
        self,
        n_dados,
        n_experimentos,
        ancho_total=8.0,
        altura_objetivo=2.2,
    ):

        super().__init__()

        self.n_dados = n_dados
        self.n_experimentos = n_experimentos

        self.x_min = n_dados
        self.x_max = 6 * n_dados

        self.n_barras = (
            self.x_max
            - self.x_min
            + 1
        )

        self.ancho_total = ancho_total
        self.altura_objetivo = altura_objetivo

        # Estética de Iván
        self.color_hist = "#7bc96f"
        self.color_activo = "#d7ff00"
        self.color_eje = "#d8d8d8"

        self.conteos = defaultdict(int)
        self.barras = {}

        self.ultimo_activo = None
        self.suma_activa = None

        # Cada posible suma ocupa una celda
        self.ancho_celda = (
            self.ancho_total
            / self.n_barras
        )

        self.ancho_bloque = (
            self.ancho_celda * 0.82
        )

        # La altura se adapta al nº de experimentos
        self.altura_bloque = (
            self.altura_objetivo
            / max(
                1,
                0.10 * self.n_experimentos,
            )
        )

        # Evitamos bloques absurdamente altos
        self.altura_bloque = min(
            self.altura_bloque,
            0.12,
        )

        # Eje X
        self.eje_x = Line(
            [0, 0, 0],
            [self.ancho_total, 0, 0],
            color=self.color_eje,
            stroke_width=1.6,
        )

        self.add(self.eje_x)

        self.ticks = VGroup()
        self.etiquetas = VGroup()

        # No etiquetamos todas las sumas cuando hay 16 dados.
        if self.n_barras <= 20:
            paso_etiqueta = 2
        elif self.n_barras <= 50:
            paso_etiqueta = 5
        else:
            paso_etiqueta = 10

        for valor in range(
            self.x_min,
            self.x_max + 1,
        ):

            indice = valor - self.x_min

            x = (
                indice + 0.5
            ) * self.ancho_celda

            tick = Line(
                [x, -0.04, 0],
                [x, 0.04, 0],
                color=self.color_eje,
                stroke_width=1.0,
            )

            self.ticks.add(tick)

            if (
                valor == self.x_min
                or valor == self.x_max
                or valor % paso_etiqueta == 0
            ):

                etiqueta = Text(
                    str(valor),
                    font_size=14,
                    color=self.color_eje,
                )

                etiqueta.next_to(
                    tick,
                    DOWN,
                    buff=0.06,
                )

                self.etiquetas.add(etiqueta)

        self.add(
            self.ticks,
            self.etiquetas,
        )


    def añadir_bloque(self, suma):

        # --------------------------------------------------
        # 1. El bloque lima anterior se incorpora
        #    a su barra verde
        # --------------------------------------------------

        if self.suma_activa is not None:

            suma_anterior = self.suma_activa

            self.conteos[suma_anterior] += 1

            indice_anterior = (
                suma_anterior
                - self.x_min
            )

            x_anterior = (
                self.eje_x.get_start()[0]
                + (
                    indice_anterior + 0.5
                )
                * self.ancho_celda
            )

            base_y = (
                self.eje_x.get_start()[1]
            )

            nueva_altura = (
                self.conteos[suma_anterior]
                * self.altura_bloque
            )

            # Primera observación de esa suma:
            # creamos su barra verde
            if suma_anterior not in self.barras:

                barra = Rectangle(
                    width=self.ancho_bloque,
                    height=nueva_altura,
                )

                barra.set_fill(
                    self.color_hist,
                    opacity=1,
                )

                barra.set_stroke(
                    width=0
                )

                barra.move_to(
                    [
                        x_anterior,
                        base_y
                        + nueva_altura / 2,
                        0,
                    ]
                )

                self.barras[suma_anterior] = barra

                self.add(barra)

            # Si ya existe, hacemos crecer
            # la misma barra
            else:

                barra = (
                    self.barras[suma_anterior]
                )

                barra.stretch_to_fit_height(
                    nueva_altura
                )

                barra.move_to(
                    [
                        x_anterior,
                        base_y
                        + nueva_altura / 2,
                        0,
                    ]
                )

        # --------------------------------------------------
        # 2. Colocamos el bloque lima correspondiente
        #    al lanzamiento actual
        # --------------------------------------------------

        indice = (
            suma
            - self.x_min
        )

        x = (
            self.eje_x.get_start()[0]
            + (
            indice + 0.5
            )
            * self.ancho_celda
        )

        base_y = (
            self.eje_x.get_start()[1]
        )

        altura_verde = (
            self.conteos[suma]
            * self.altura_bloque
        )

        altura_activa = max(
            self.altura_bloque,
            0.06,
        )

        y = (
            base_y
            + altura_verde
            + altura_activa / 2
        )

        # El bloque lima se crea una sola vez
        if self.ultimo_activo is None:

            self.ultimo_activo = Rectangle(
                width=self.ancho_bloque,
                height=altura_activa,
            )

            self.ultimo_activo.set_stroke(
                width=0
            )

            self.add(
                self.ultimo_activo
            )

        # Y después simplemente se reutiliza
        self.ultimo_activo.set_fill(
            self.color_activo,
            opacity=1,
        )

        self.ultimo_activo.move_to(
            [x, y, 0]
        )

        self.suma_activa = suma

        return self.ultimo_activo



    def añadir_lote(self, sumas):

        if len(sumas) == 0:
            return

        # --------------------------------------------------
        # 1. Observaciones que pasan a verde
        # --------------------------------------------------

        sumas_verdes = []

        # El lima que quedó de la actualización anterior
        # ahora se integra en su barra verde
        if self.suma_activa is not None:
            sumas_verdes.append(
                self.suma_activa
            )

        # Del lote actual, todas menos la última
        # pasan directamente al histograma verde
        sumas_verdes.extend(
            int(suma)
            for suma in sumas[:-1]
        )

        # --------------------------------------------------
        # 2. Actualizamos los conteos de una vez
        # --------------------------------------------------

        if len(sumas_verdes) > 0:

            valores, frecuencias = np.unique(
                sumas_verdes,
                return_counts=True,
            )

            for valor, frecuencia in zip(
                valores,
                frecuencias,
            ):

                suma = int(valor)

                self.conteos[suma] += int(
                    frecuencia
                )

                indice = (
                    suma
                    - self.x_min
                )

                x = (
                    self.eje_x.get_start()[0]
                    + (
                        indice + 0.5
                    )
                    * self.ancho_celda
                )

                base_y = (
                    self.eje_x.get_start()[1]
                )

                nueva_altura = (
                    self.conteos[suma]
                    * self.altura_bloque
                )

                # Primera vez que aparece esa suma
                if suma not in self.barras:

                    barra = Rectangle(
                        width=self.ancho_bloque,
                        height=nueva_altura,
                    )

                    barra.set_fill(
                        self.color_hist,
                        opacity=1,
                    )

                    barra.set_stroke(
                        width=0
                    )

                    barra.move_to(
                        [
                            x,
                            base_y
                            + nueva_altura / 2,
                            0,
                        ]
                    )

                    self.barras[suma] = barra

                    self.add(barra)

                # La barra ya existe:
                # solo modificamos su altura una vez
                else:

                    barra = self.barras[suma]

                    barra.stretch_to_fit_height(
                        nueva_altura
                    )

                    barra.move_to(
                        [
                            x,
                            base_y
                            + nueva_altura / 2,
                            0,
                        ]
                    )

        # --------------------------------------------------
        # 3. La última observación del lote queda LIMA
        # --------------------------------------------------

        suma_actual = int(
            sumas[-1]
        )

        indice = (
            suma_actual
            - self.x_min
        )

        x = (
            self.eje_x.get_start()[0]
            + (
                indice + 0.5
            )
            * self.ancho_celda
        )

        base_y = (
            self.eje_x.get_start()[1]
        )

        altura_verde = (
            self.conteos[suma_actual]
            * self.altura_bloque
        )

        altura_activa = max(
            self.altura_bloque,
            0.06,
        )

        y = (
            base_y
            + altura_verde
            + altura_activa / 2
        )    

        # El bloque lima sigue siendo uno solo
        if self.ultimo_activo is None:

            self.ultimo_activo = Rectangle(
                width=self.ancho_bloque,
                height=altura_activa,
            )

            self.ultimo_activo.set_stroke(
                width=0
            )

            self.add(
                self.ultimo_activo
            )

        self.ultimo_activo.stretch_to_fit_height(
            altura_activa
        )

        self.ultimo_activo.set_fill(
            self.color_activo,
            opacity=1,
        )

        self.ultimo_activo.move_to(
            [x, y, 0]
        )

        self.suma_activa = suma_actual

        return self.ultimo_activo


    def añadir_curva_normal(
        self,
        media,
        desviacion,
        n_experimentos,
    ):

        if desviacion <= 0:
            return

        puntos = []

        # Recorremos suavemente todo el rango
        # posible de sumas
        valores_x = np.linspace(
            self.x_min,
            self.x_max,
            250,
        )

        for valor in valores_x:

            # Densidad de la normal teórica
            densidad = (
                1
                / (
                    desviacion
                    * np.sqrt(2 * np.pi)
                )
                * np.exp(
                    -0.5
                    * (
                        (valor - media)
                        / desviacion
                    ) ** 2
                )
            )

            # Número esperado de observaciones
            # alrededor de ese valor
            frecuencia_esperada = (
                n_experimentos
                * densidad
            )

            # Coordenada horizontal:
            # misma escala que las barras
            indice = (
                valor
                - self.x_min
            )

            x = (
                self.eje_x.get_start()[0]
                + (
                    indice + 0.5
                )
                * self.ancho_celda
            )

            # Coordenada vertical:
            # cada observación equivale a
            # un bloque del histograma
            y = (
                self.eje_x.get_start()[1]
                + frecuencia_esperada
                * self.altura_bloque
            )

            puntos.append(
                np.array(
                    [x, y, 0]
                )
            )

        curva = VMobject()

        curva.set_points_smoothly(
            puntos
        )

        curva.set_stroke(
            color="#ffe45c",
            width=4,
        )

        self.add(
            curva
        )

        return curva