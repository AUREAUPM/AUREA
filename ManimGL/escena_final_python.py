from manimlib import *
import numpy as np
import random
from math import comb
from scipy.stats import norm
from collections import defaultdict


# Número de dados
n_dados = 10
# Número de experimentos 
n_experimentos = 800
# Cada cuántos experimentos renderizar un frame (800 experimentos y salto de 5 → 160 frames animados)
salto_animacion = 5
# Duración de cada frame animado (en segundos)
run_time_animacion = 0.07
# Altura objetivo hasta la cual llega el histograma para la animación (en unidades de Manim)
altura_objetivo = 3


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


# Clase para representar el histograma de sumas de dados
class Histograma(VGroup):
    def __init__(self, x_min=10, x_max=60,):
        super().__init__()

        # Configuracion de las caracteristicas de la escena
        self.x_min       = x_min # Valor mínimo de la suma de los dados (10 para 10 dados)
        self.x_max       = x_max # Valor máximo de la suma de los dados (60 para 10 dados)
        self.base_y      = -3.1 # Coordenada 'y' de la base del histograma
        self.ancho_total = 9.5 # Ancho total del histograma en unidades de Manim
        self.altura_bloque  = altura_objetivo / (0.06 * n_experimentos) # Altura de cada bloque del histograma, calculada para que el histograma alcance la altura objetivo
        self.ancho_bloque   = 0.16 # Ancho de cada bloque del histograma
        self.separacion     = 0.035 # Separación entre bloques del histograma
        self.color_hist     = "#7bc96f" # Color de los bloques del histograma
        self.color_activo   = "#d9a066" # Color del bloque activo 
        self.color_eje      = "#d8d8d8" # Color del eje

        # Diccionario para almacenar los bloques del histograma por cada suma de dados
        self.bloques_por_bin = defaultdict(list) 
        self.ultimo_activo   = None

        # Crear el eje horizontal del histograma
        eje = Line(
            [-self.ancho_total/2, self.base_y, 0], # Punto inicial del eje (izquierda)
            [ self.ancho_total/2, self.base_y, 0], # Punto final del eje (derecha)
            color=self.color_eje, # Color del eje
            stroke_width=1.6 # Grosor del eje
        )
        self.add(eje) # Agregar el eje al grupo del histograma

        # Crear las marcas y números en el eje horizontal
        for k in range(x_min, x_max + 1): 
            x = np.interp(
                k,
                [x_min, x_max],
                [-self.ancho_total/2, self.ancho_total/2]
            )
            # Crear una marca (tick) en el eje para cada valor de suma de dados
            tick = Line(
                [x, self.base_y - 0.07, 0],
                [x, self.base_y + 0.07, 0],
                color=self.color_eje,
                stroke_width=1
            )
            self.add(tick)
            # Agregar números al eje solo para las sumas pares para evitar saturación visual
            if k % 2 == 0:
                numero = Text(
                    str(k),
                    font_size=12,
                    color=self.color_eje
                )
                numero.move_to([x, self.base_y - 0.22, 0])
                self.add(numero) # Agregar los números al grupo del histograma

   
    # Añade un bloque al histograma para la suma dada, actualizando el bloque activo y su color
    def añadir_bloque(self, suma):
        # Cambia el color del bloque que estaba activo anteriormente al color base del histograma
        if self.ultimo_activo is not None:
            self.ultimo_activo.set_fill(self.color_hist)
        # Calcula la posición 'x' del bloque correspondiente al valor de la nueva suma
        x = np.interp(
            suma,
            [self.x_min, self.x_max],
            [-self.ancho_total/2, self.ancho_total/2]
        )
        # Calcula la posición 'y' de la columna donde debe ir colocado el nuevo bloque, teniendo en cuenta cuántos bloques ya hay apilados para esa suma
        j = len(self.bloques_por_bin[suma])
        # Calcula la posición 'y' donde debe colocarsel el nuevo bloque (base + altura de bloque/2 * número de bloques apilados)
        y = (
            self.base_y
            + self.altura_bloque / 2
            + j * self.altura_bloque
        )
        # Crea el nuevo bloque a colocar
        bloque = Rectangle(
            width=self.ancho_bloque,
            height=self.altura_bloque
        )
        bloque.set_fill(self.color_activo, opacity=1) # Color del bloque activo
        bloque.set_stroke(width=0) # Sin borde para los bloques del histograma
        bloque.move_to([x, y, 0]) # Mueve el bloque a la posición calculada

        self.bloques_por_bin[suma].append(bloque) # Guarda el bloque en el diccionario de bloques por suma
        self.ultimo_activo = bloque # Actualiza el bloque activo actual al nuevo bloque
        self.add(bloque) # Agrega el nuevo bloque al grupo del histograma

        # Devuelve el bloque creado para que pueda ser animado en la escena
        return bloque


# Clase para representar la distribución de probabilidades de los dados
class DistribucionDados(VGroup):
    def __init__(self, conteos):
        super().__init__()

        # Configuración de colores y dimensiones para la representación de la distribución de dados
        color_eje    = "#d8d8d8" # Color del eje
        color_barra  = "#2d9cdb" # Color de las barras 
        color_flecha = "#ffe45c" # Color de las flechas que indican la cantidad de veces que ha salido cada suma
        ancho_total  = 3.5 # Ancho total de la representación de la distribución de dados
        base_y       = 0 # Coordenada 'y' de la base de la representación de la distribución de dados
        altura_max   = 0.9 # Altura máxima de la representación de la distribución de dados (en unidades de Manim)
        probabilidad = 1/6 # Probabilidad de que salga cada suma (1/6 para cada suma de 10 dados)

        # Crear los ejes de la representación de la distribución de dados
        eje_x = Line(
            [0, base_y, 0], # Punto inicial del eje (izquierda)
            [ancho_total, base_y, 0], # Punto final del eje (derecha)
            color=color_eje, # Color del eje
            stroke_width=1.6 # Grosor del eje
        )
        eje_y = Line(
            [0, base_y, 0], # Punto inicial del eje (abajo)
            [0, altura_max, 0], # Punto final del eje (arriba)
            color=color_eje, # Color del eje
            stroke_width=1.6  # Grosor del eje
        )
        # Agregar los ejes al grupo de la distribución de dados
        self.add(eje_x, eje_y)

        # Crear las marcas y números en el eje vertical
        valores_y = [(0,    "0.00"), (0.25, "0.25"), (0.50, "0.50")] # Valores y etiquetas para las marcas en el eje vertical (probabilidades 0.00, 0.25 y 0.50)
        # Agregar las marcas y números al eje vertical
        for valor, texto in valores_y:
            y = valor 
            tick = Line(
                [-0.045, y, 0], 
                [ 0.045, y, 0],
                color=color_eje,
                stroke_width=1.2
            )
            numero = Text(
                texto,
                font_size=13,
                color=color_eje
            )
            # Colocar los números a la izquierda de las marcas del eje vertical con un pequeño espacio
            numero.next_to(tick, LEFT, buff=0.04)
            self.add(tick, numero) # Agregar los ticks y números al grupo de la distribución de dados

        # Crear las barras, dados y flechas para cada suma de dados (de 1 a 6)
        for i in range(6):
            x = 0.42 + i * 0.56 # Posición 'x' de cada barra, dado y flechas para las sumas de dados
            h = probabilidad # Altura de cada barra, proporcional a la probabilidad
           
            barra = Rectangle(width=0.48, height=h) # Crear la barra para la suma de dados correspondiente
            barra.set_fill(color_barra, opacity=0.9) # Color de las barras
            barra.set_stroke(width=0) 
            barra.move_to([x, base_y + h/2, 0]) # Mueve la barra a la posición correcta
            self.add(barra) # Agrega la barra al grupo de la distribución de dados

            dado = Dado(valor=i+1, size=0.24) # Crea un dado haciendo referencia al Vgroup `Dado` 
            dado.move_to([x, -0.30, 0]) # Mueve el dado a una posición debajo de la barra correspondiente
            self.add(dado) # Agrega el dado al grupo de la distribución de dados

            cantidad = conteos[i] # Cantidad de veces que ha salido el dado
            # Para cada vez que ha salido el dado, crear una flecha y apilarlas verticalmente con una separación de 0.07 unidades entre ellas
            for j in range(cantidad):
                flecha = Arrow(
                    start=[0, 0.06, 0], # Punto inicial de la flecha (ligeramente por encima de la barra)
                    end=[0, 0, 0], # Punto final de la flecha (en el borde superior de la barra)
                    buff=0,
                    stroke_width=2.2, # Grosor de la flecha
                    max_tip_length_to_length_ratio=0.7, # Proporción del tamaño de la punta de flecha respecto a la longitud total de la flecha
                    color=color_flecha # Color 
                )
                flecha.scale(0.11) # Escala la flecha para que tenga un tamaño adecuado para la representación
                flecha.move_to([x, h + 0.05 + j * 0.07, 0]) # Mueve la flecha a la posición correcta, apilándolas verticalmente con una separación de 0.07 unidades entre ellas
                self.add(flecha) # Agregar la flecha al grupo de la distribución de dados


# Escena principal que muestra la simulación de tirar 10 dados, el histograma de las sumas y la distribución de probabilidades
class EscenaDados(Scene):
    def construct(self):
        tiradas = np.random.randint(1, 7, size=(n_experimentos, n_dados)) # Genera una matriz de tiradas de dados con valores entre 1 y 6, con dimensiones (n_experimentos, n_dados)
        sumas = tiradas.sum(axis=1) # Calcula la suma de cada tirada de dados
        textos_suma_cache = {} # Diccionario para almacenar los objetos de texto de las sumas
        # Renderiza el texto de cada suma una sola vez y los guarda para evitar renderizarlos cada vez que salgan
        for s in range(10, 61):
            t = Text(f"Sum = {s}").scale(0.9)
            textos_suma_cache[s] = t

        histograma = Histograma() # Crea el histograma 
        
        # Representación inicial de la distribución de dados con conteos iniciales de 0 para cada suma escalado y posicionado en la esquina superior izquierda
        distribucion = DistribucionDados([0] * 6)
        distribucion.scale(1.3) 
        distribucion.to_corner(UL)
        distribucion.shift(LEFT*0.15 + DOWN*0.02)

        ## CURVA DE LA NORMAL TEÓRICA
        mu = n_dados * 3.5 # Media de la distribución  (número de dados * valor medio de cada dado)
        sigma = np.sqrt(n_dados * 35 / 12) # Desviación estándar de la distribución  (raíz cuadrada de n_dados * varianza de un dado)
        x_vals = np.linspace(10, 60, 150) # Valores de 'x'de la curva, desde la suma mínima (10) hasta la suma máxima (60) con 150 puntos para representarla
        # Valores de 'y' de la curva, con la fórmula de la función de densidad
        y_vals = (
            1 / (sigma * np.sqrt(2 * np.pi))
        ) * np.exp(
            -(x_vals - mu)**2 / (2 * sigma**2)
        )
        # Altura hasta donde llega la curva (altura objetivo)
        escala_curva = altura_objetivo * 18
        # Calcula los puntos modelandolos a la altura objetivo y anchura del histograma
        puntos = [
            [
                np.interp(x, [10, 60], [-4.75, 4.75]),
                -3.1 + y * escala_curva,
                0
            ]
            for x, y in zip(x_vals, y_vals)
        ]

        curva = VMobject() # Crea un objeto VMobject para representar la curva de la distribución normal teórica
        curva.set_points_smoothly(puntos) # Define los puntos de la curva suavemente para que se vea como una curva continua
        curva.set_color(YELLOW) # Color
        curva.set_stroke(width=2.2) # Anchura
        # Anima la creación de la curva de la distribución normal teórica al inicio de la escena
        self.play(ShowCreation(curva), run_time=1.5)

        # Agrega el histograma y la distribución de dados a la escena
        self.add(histograma, distribucion)
        # Representación inicial de la tirada de dados, la suma y el contador de experimentos
        tirada_init = tiradas[0]
        # Crea los dados haciendo referencia al Vgroup `Dado`
        dados = VGroup(*[
            Dado(valor=int(v), size=0.42)
            for v in tirada_init
        ])
        dados.arrange_in_grid(2, 5, buff=0.22) # Organiza los dados en una cuadrícula de 2 filas y 5 columnas con un espacio de 0.22 unidades entre ellos
        dados.move_to([4.9, 2.15, 0]) # Mueve los dados a la posición inicial en la esquina superior derecha

        suma_init = int(sumas[0]) # Suma inicial de la primera tirada de dados
        texto_suma = textos_suma_cache[suma_init].copy() # Crea el texto suma buscando en el diccionario de etxtos renderizados
        texto_suma.next_to(dados, DOWN, buff=0.35) # Posiciona el texto de la suma debajo de los dados con un espacio de 0.35 unidades

        contador = Integer(0) # Contador para mostrar el número de experimentos realizados
        contador.scale(0.7) # Escala del contador
        contador.move_to([-4.9, -0.25, 0]) # Posición del contador
        self.add(dados, texto_suma, contador) # Agrega los dados, el texto de la suma y el contador a la escena

        # Bucle principal para representar cada experimento 
        for i in range(n_experimentos):
            suma  = int(sumas[i]) # Suma de la tirada actual
            tirada = tiradas[i] # Tirada de dados actual
            # Agrega un bloque a la barra correspondiente a la suma obtenida
            histograma.añadir_bloque(suma)
            # Renderiza en los saltos de animación y en el último experimento
            renderizar = (
                i % salto_animacion == salto_animacion - 1
                or i == n_experimentos - 1
            )

            if renderizar:

                # Calcula los conteos de cada valor de dado (1 a 6) en la tirada actual para actualizar la distribución de dados
                conteos = [
                    int(np.sum(tirada == k))
                    for k in range(1, 7)
                ]

                nueva_dist = DistribucionDados(conteos) # Crea una nueva distribución de dados con los conteos actualizados
                nueva_dist.scale(1.3) # Escala
                # Posición
                nueva_dist.to_corner(UL)
                nueva_dist.shift(LEFT*0.15 + DOWN*0.02)
                distribucion.become(nueva_dist) # Actualiza la distribución de dados en la escena con la nueva distribución creada

                # Crea los nuevos dados haciendo referencia al Vgroup `Dado`
                nuevos_dados = VGroup(*[
                    Dado(valor=int(v), size=0.42)
                    for v in tirada
                ])
                # Organiza los nuevos dados en una cuadrícula de 2 filas y 5 columnas con un espacio de 0.22 unidades entre ellos
                nuevos_dados.arrange_in_grid(2, 5, buff=0.22)
                nuevos_dados.move_to([4.9, 2.15, 0]) # Mueve los nuevos dados a la posición en la esquina superior derecha
                dados.become(nuevos_dados) # Actualiza los dados en la escena con los nuevos dados creados

                nuevo_texto = textos_suma_cache[suma].copy() # Crea un nuevo texto de la suma actual buscando en el diccionario de textos renderizados
                nuevo_texto.next_to(nuevos_dados, DOWN, buff=0.35) # Posiciona el nuevo texto
                texto_suma.become(nuevo_texto) # Actualiza el texto de la suma en la escena con el nuevo texto creado

                # Actualiza el contador de experimentos realizados
                contador.set_value(i + 1)

                # Anima la transición en cada salto de animación y en el último experimento
                self.wait(run_time_animacion)

        self.wait(2)