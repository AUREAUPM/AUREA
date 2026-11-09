from manimlib import *

from boton import Boton, GrupoBotones


class PanelControles(VGroup):

    def __init__(self):

        super().__init__()

        self.titulo = Text(
            "Dados por lanzamiento",
            font_size=28,
        )

        self.boton2 = Boton(
            "2",
            2,
            ancho=0.85,
        )

        self.boton6 = Boton(
            "6",
            6,
            ancho=0.85,
        )

        self.boton10 = Boton(
            "10",
            10,
            ancho=0.85,
        )

        self.boton16 = Boton(
            "16",
            16,
            ancho=0.85,
        )

        self.grupo = GrupoBotones()

        self.grupo.agregar(self.boton2)
        self.grupo.agregar(self.boton6)
        self.grupo.agregar(self.boton10)
        self.grupo.agregar(self.boton16)

        self.grupo.organizar(
            separacion=0.15
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
            RIGHT * 2.9
            + UP * 2.8
        )