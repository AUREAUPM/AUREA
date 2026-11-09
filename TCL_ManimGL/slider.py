from manimlib import *
import numpy as np


class Slider(VGroup):

    def __init__(
        self,
        valores,
        ancho=3.2,
        etiqueta="Nº experimentos",
    ):

        super().__init__()

        self.valores = valores
        self.ancho = ancho

        self.indice = 0

        # Título
        self.etiqueta = Text(
            etiqueta,
            font_size=28,
        )

        # Línea
        self.linea = Line(
            LEFT * ancho / 2,
            RIGHT * ancho / 2,
            color="#d8d8d8",
            stroke_width=3,
        )

        # Punto móvil
        self.punto = Dot(
            radius=0.09,
            color="#ffe45c",
        )

        self.punto.move_to(
            self.linea.get_left()
        )

        # Valor mostrado
        self.texto_valor = Text(
            str(self.valores[0]),
            font_size=22,
        )

        self.texto_valor.next_to(
            self.linea,
            DOWN,
            buff=0.15,
        )

        self.etiqueta.next_to(
            self.linea,
            UP,
            buff=0.47,
        )

        self.add(
            self.etiqueta,
            self.linea,
            self.punto,
            self.texto_valor,
        )


    def mover_a(self, x):

        izquierda = self.linea.get_left()[0]
        derecha = self.linea.get_right()[0]

        x = np.clip(
            x,
            izquierda,
            derecha,
        )

        proporcion = (
            (x - izquierda)
            / (derecha - izquierda)
        )

        indice = round(
            proporcion
            * (len(self.valores) - 1)
        )

        self.indice = indice

        nueva_x = np.interp(
            indice,
            [0, len(self.valores) - 1],
            [izquierda, derecha],
        )

        self.punto.move_to([
            nueva_x,
            self.linea.get_center()[1],
            0,
        ])

        nuevo_texto = Text(
            str(self.valores[indice]),
            font_size=22,
        )

        nuevo_texto.move_to(
            self.texto_valor
        )

        self.texto_valor.become(
            nuevo_texto
        )


    def valor(self):

        return self.valores[self.indice]