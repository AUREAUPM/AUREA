from manimlib import *

from distribucion import (
    DistribucionUniforme,
    DistribucionSesgada,
    DistribucionEnV,
)


class PanelDistribucion(VGroup):

    def __init__(self):

        super().__init__()

        self.marco = Rectangle(
            width=3.9,
            height=2.8,
            stroke_opacity=0,
        )

        self.distribucion = VGroup()

        self.subtitulo = Text(
            "Distribución de un dado",
            font_size=24,
        )

        self.subtitulo.set_color(
            WHITE
        )

        self.subtitulo.set_opacity(0)

        self.add(
            self.marco,
            self.distribucion,
            self.subtitulo,
        )

        self.move_to(LEFT * 4 + DOWN * 15)

    def crear_distribucion(self, clave):

        if clave == "uniforme":
            return DistribucionUniforme()

        elif clave == "sesgada":
            return DistribucionSesgada()

        elif clave == "v":
            return DistribucionEnV()

        return VGroup()

    def mostrar(
        self,
        scene,
        clave,
        x_centro=None,
    ):

        # Quitamos la distribución anterior
        # únicamente del PanelDistribucion
        self.remove(
            self.distribucion
        )

        self.distribucion = (
            self.crear_distribucion(clave)
        )

        self.distribucion.scale(
            0.82
        )

        self.distribucion.move_to(
            [x_centro, 0.85, 0]
        )

        # La nueva distribución pasa a ser
        # hija del propio panel
        self.add(
            self.distribucion
        )

        self.subtitulo.next_to(
            self.distribucion,
            DOWN,
            buff=0.25,
        )

        self.subtitulo.set_y(
            -0.15
        )

        self.subtitulo.set_opacity(
            1
        )

        