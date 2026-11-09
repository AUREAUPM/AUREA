from manimlib import *

from dado import Dado


class DistribucionBase(VGroup):

    def __init__(self, probabilidades):
        super().__init__()

        self.probabilidades_lista = probabilidades

        self.barras = VGroup()
        self.dados = VGroup()
        self.flechas = VGroup()

        # Estética de Iván
        color_eje = "#d8d8d8"
        color_barra = "#2d9cdb"
        self.color_flecha = "#ffe45c"

        ancho_total = 3.5
        altura_max = 0.9
        base_y = 0

        prob_max = max(probabilidades)

        # Ejes
        self.eje_x = Line(
            [0, base_y, 0],
            [ancho_total, base_y, 0],
            color=color_eje,
            stroke_width=1.6,
        )

        self.eje_y = Line(
            [0, base_y, 0],
            [0, altura_max, 0],
            color=color_eje,
            stroke_width=1.6,
        )

        self.add(self.eje_x, self.eje_y)

        # Marca en el eje vertical para la probabilidad máxima
        tick_y = altura_max

        self.tick_superior = Line(
            [-0.045, tick_y, 0],
            [0.045, tick_y, 0],
            color=color_eje,
            stroke_width=1.2,
        )

        self.texto_tick = Text(
            self.formato_probabilidad(prob_max),
            font_size=14,
            color=color_eje,
        )

        self.texto_tick.next_to(
            self.tick_superior,
            LEFT,
            buff=0.04,
        )

        self.add(self.tick_superior, self.texto_tick)

        # Barras + dados
        for i in range(6):

            x = 0.42 + i * 0.56
            p = probabilidades[i]
            h = altura_max * p / prob_max

            barra = Rectangle(
                width=0.48,
                height=h,
            )
            barra.set_fill(color_barra, opacity=0.9)
            barra.set_stroke(width=0)
            barra.move_to([x, base_y + h / 2, 0])

            self.barras.add(barra)

            dado = Dado(
                valor=i + 1,
                size=0.24,
            )
            dado.move_to([x, -0.30, 0])

            self.dados.add(dado)

        self.add(self.barras, self.dados)

    def formato_probabilidad(self, p):

        if abs(p - 1/6) < 1e-6:
            return "1/6"

        if abs(p - 1/4) < 1e-6:
            return "1/4"

        return f"{p:.2f}"

    def limpiar_flechas(self):

        self.remove(self.flechas)
        self.flechas = VGroup()

    def mostrar_flechas(self, conteos):

        self.limpiar_flechas()

        # Quitamos la marca superior al pasar a la simulación
        self.remove(self.tick_superior, self.texto_tick)

        for i in range(6):

            barra = self.barras[i]

            x = barra.get_center()[0]
            y_superior = barra.get_top()[1]

            cantidad = conteos[i]

            for j in range(cantidad):
                flecha = Arrow(
                    start=[0, 0.06, 0],
                    end=[0, 0, 0],
                    buff=0,
                    stroke_width=2.2,
                    max_tip_length_to_length_ratio=0.7,
                    color=self.color_flecha,
                )
                flecha.scale(0.11)
                
                flecha.move_to(
                    [
                        x,
                        y_superior + 0.08 + j * 0.08,
                        0,
                    ]
                )

                self.flechas.add(flecha)

        self.add(self.flechas)


class DistribucionUniforme(DistribucionBase):

    def __init__(self):

        probabilidades = [1/6] * 6
        super().__init__(probabilidades)


class DistribucionSesgada(DistribucionBase):

    def __init__(self):

        pesos = [1, 2, 3, 4, 5, 6]
        total = sum(pesos)

        probabilidades = [
            peso / total
            for peso in pesos
        ]

        super().__init__(probabilidades)


class DistribucionEnV(DistribucionBase):

    def __init__(self):

        pesos = [3, 2, 1, 1, 2, 3]
        total = sum(pesos)

        probabilidades = [
            peso / total
            for peso in pesos
        ]

        super().__init__(probabilidades)