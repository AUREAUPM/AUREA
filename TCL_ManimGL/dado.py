
from manimlib import *

# Clase para representar un dado
class Dado(VGroup):
    def __init__(self, valor=1, size=0.42):
        super().__init__()
        # Crear el borde del dado como un rectángulo redondeado con las especificaciones dadas
        borde = RoundedRectangle(
            corner_radius=0.08,
            width=size,
            height=size,
            stroke_width=1.8,
            stroke_color=WHITE,
            fill_color="#1f1f1f",
            fill_opacity=1
        )
         
        # Distancia desde el centro del dado para colocar los puntos (ajustada para que se vea bien)
        s = size * 0.24
        # Define las posiciones de los puntos para cada valor del dado
        posiciones = {
            1: [(0, 0)],
            2: [(-s, -s), (s, s)], 
            3: [(-s, -s), (0, 0), (s, s)],
            4: [(-s, -s), (-s, s), (s, -s), (s, s)],
            5: [(-s, -s), (-s, s), (0, 0), (s, -s), (s, s)],
            6: [(-s, -s), (-s, 0), (-s, s), (s, -s), (s, 0), (s, s)]
        }
        
        # Crea los puntos del dado según el valor dado
        puntos = VGroup(*[
            Dot(
                point=[x, y, 0], # Posición del punto en el dado
                radius=size * 0.06, # Tamaño del punto
                color="#5dade2" #Color
            )
            for x, y in posiciones[valor]
        ])
        
        # Agrega el cuadrado del dado y los puntos al grupo del dado
        self.add(borde, puntos)

class GrupoDados(VGroup):

    def __init__(self, valores):

        # Para heredar las propiedades de VGroup
        super().__init__()

        self.lista_dados = []

        for valor in valores:

            dado = Dado(valor)

            self.lista_dados.append(dado)

            self.add(dado)

        n = len(valores)

        if n == 2:
            self.arrange_in_grid(n_rows=1, n_cols=2, buff=0.22)

        elif n == 4:
            self.arrange_in_grid(n_rows=2, n_cols=2, buff=0.22)

        elif n == 6:
            self.arrange_in_grid(n_rows=2, n_cols=3, buff=0.22)

        elif n == 10:
            self.arrange_in_grid(n_rows=2, n_cols=5, buff=0.22)

        elif n == 16:
            self.arrange_in_grid(n_rows=2, n_cols=8, buff=0.22)