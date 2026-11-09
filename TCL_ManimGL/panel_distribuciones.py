from manimlib import *

from boton import Boton, GrupoBotones


class PanelDistribuciones(VGroup):

    def __init__(self):

        super().__init__()

        self.titulo = Text(
            "Distribución de probabilidad",
            font_size=28,
        )

        self.boton_uniforme = Boton(
            "Uniforme",
            "uniforme",
            ancho=1.35,
        )

        self.boton_sesgada = Boton(
            "Sesgada",
            "sesgada",
            ancho=1.35,
        )

        self.boton_v = Boton(
            "En V",
            "v",
            ancho=1.35,
        )

        self.grupo = GrupoBotones()

        self.grupo.agregar(self.boton_uniforme)
        self.grupo.agregar(self.boton_sesgada)
        self.grupo.agregar(self.boton_v)

        self.grupo.organizar(
            separacion=0.18
        )

        self.titulo.next_to(
            self.grupo,
            UP,
            buff=0.25,
        )

        self.add(
            self.titulo,
            self.grupo,
        )

        self.move_to(
            LEFT * 4.4
            + UP * 2.8
        )