from manimlib import *
import numpy as np
import random
from math import comb
from scipy.stats import norm
from collections import defaultdict


# Número de dados
n_dados = 10
# Número de experimentos 
n_experimentos = 2000
# Cada cuántos experimentos renderizar un frame (2000 experimentos y salto de 5 → 400 frames animados)
salto_animacion = 5
# Duración de cada frame animado (en segundos)
run_time_animacion = 0.07
# Altura objetivo hasta la cual llega el histograma para la animación (en unidades de Manim)
altura_objetivo = 2.1


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
    def __init__(self, n_dados, n_experimentos):
        super().__init__()
        # Configuracion de las caracteristicas de la escena
        self.x_min       = n_dados # Valor mínimo de la suma de los dados (10 para 10 dados)
        self.x_max       = 6 * n_dados # Valor máximo de la suma de los dados (60 para 10 dados)
        self.n_barras = self.x_max - self.x_min + 1
        self.base_y      = -3.25 # Coordenada 'y' de la base del histograma
        # Calcula el ancho total del histograma según el número de dados para que se vea proporcionado
        if n_dados == 5:
            self.ancho_total = 6.2
        elif n_dados == 10:
            self.ancho_total = 9.5
        else:  # 20 dados
            self.ancho_total = 12.5
        max_experimentos = 2000 # Número máximo de experimentos para calcular la altura de los bloques del histograma
        if n_dados == 5:
            factor = 0.06
        elif n_dados == 10:
            factor = 0.045
        elif n_dados == 20:
            factor = 0.032
        self.altura_bloque  = altura_objetivo / (factor * max_experimentos) # Altura de cada bloque del histograma, calculada para que el histograma alcance la altura objetivo
        self.ancho_bloque   = self.ancho_total / self.n_barras * 0.82 # Ancho de cada bloque del histograma
        self.separacion     = self.ancho_total / self.n_barras * 0.18 # Separación entre bloques del histograma
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
        for k in range(self.x_min, self.x_max + 1): 
            x = np.interp(
                k,
                [self.x_min, self.x_max],
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
    def __init__(self, conteos, probabilidades=None):
        super().__init__()
        if probabilidades is None:
            probabilidades = [1/6] * 6 # Si no se proporcionan probabilidades, se asume una distribución uniforme para los dados (1/6 para cada cara)
        # Configuración de colores y dimensiones para la representación de la distribución de dados
        color_eje    = "#d8d8d8" # Color del eje
        color_barra  = "#2d9cdb" # Color de las barras 
        color_flecha = "#ffe45c" # Color de las flechas que indican la cantidad de veces que ha salido cada suma
        ancho_total  = 3.5 # Ancho total de la representación de la distribución de dados
        base_y       = 0 # Coordenada 'y' de la base de la representación de la distribución de dados
        altura_max   = 1.2 # Altura máxima de la representación de la distribución de dados (en unidades de Manim)
        probabilidades = [0.35, 0.25, 0.17, 0.12, 0.07, 0.04] # Probabilidad de que salga cada suma 
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
        valores_y = [(0,    "0.00"), (0.25, "0.25"), (0.50, "0.50"), (0.75, "0.75"), (1.00, "1.00")] # Valores y etiquetas para las marcas en el eje vertical (probabilidades 0.00, 0.25, 0.50, 0.75 y 1.00)
        # Agregar las marcas y números al eje vertical
        for valor, texto in valores_y:
            y = valor * altura_max # Calcula la posición 'y' de la marca correspondiente a la probabilidad
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
            h = probabilidades[i] * altura_max # Altura de cada barra, proporcional a la probabilidad
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
                flecha.move_to([x, h + 0.06 + j * 0.08, 0]) # Mueve la flecha a la posición correcta, apilándolas verticalmente con una separación de 0.07 unidades entre ellas
                self.add(flecha) # Agregar la flecha al grupo de la distribución de dados


# Clase para representar un slider interactivo que permite seleccionar el número de experimentos a realizar
class Slider(VGroup):
    def __init__(self, valores, width=3.2, label="Experimentos"):
        super().__init__()
        self.valores = valores # Lista de valores posibles para el slider (entre 10 y 800 en incrementos de 50)
        self.label = label # Etiqueta que se mostrará encima del slider
        self.index = len(valores) - 1 # Índice del valor seleccionado actualmente (inicialmente el último valor de la lista)
        self.linea = Line(LEFT * width / 2, RIGHT * width / 2,stroke_width=3) # Línea que representa el slider
        self.punto = Dot(radius=0.08, color=YELLOW) # Punto que indica la posición actual del slider
        self.punto.move_to(self.linea.get_end()) # Mueve el punto al final de la línea (valor máximo del slider)
        # Crea el texto que muestra el valor seleccionado actualmente en el slider
        self.texto = Text(
            f"{label}: {self.valores[self.index]}",
            font_size=22
        )
        self.texto.next_to(self.linea, UP, buff=0.18) # Posiciona el texto encima de la línea del slider con un pequeño espacio 
        self.add(self.linea, self.punto, self.texto) # Agrega la línea, el punto y el texto al grupo del slider

    # Mueve el punto del slider a una posición específica
    def mover_a(self, x):
        xmin = self.linea.get_start()[0] # Coordenada 'x' mínima de la línea del slider
        xmax = self.linea.get_end()[0] # Coordenada 'x' máxima de la línea del slider
        x = np.clip(x, xmin, xmax) # Limita la posición 'x' del punto para que no se salga de los límites de la línea del slider
        posiciones = np.linspace(xmin, xmax, len(self.valores)) # Calcula las posiciones 'x' correspondientes a cada valor del slider
        self.index = np.argmin(np.abs(posiciones - x)) # Encuentra el índice del valor más cercano a la posición 'x' del punto del slider
        # Mueve el punto del slider a la posición correspondiente al valor seleccionado
        self.punto.move_to([
            posiciones[self.index],
            self.linea.get_center()[1],
            0
        ])
        # Actualiza el texto que muestra el valor seleccionado actualmente en el slider
        nuevo = Text(
            f"{self.label}: {self.valores[self.index]}",
            font_size=22
        )
        nuevo.next_to(self.linea, UP, buff=0.18) # Posiciona el nuevo texto encima de la línea del slider con un pequeño espacio
        self.texto.become(nuevo) # Actualiza el texto del slider con el nuevo texto creado

    # Devuelve el valor seleccionado actualmente en el slider
    def valor(self):
        return self.valores[self.index]
    
    

# Escena principal que muestra la simulación de tirar 10 dados, el histograma de las sumas y la distribución de probabilidades
class EscenaDados(InteractiveScene):
    # Maneja el evento de presionar el mouse para iniciar el arrastre del slider
    def on_mouse_press(self, point, button, mods):
        # Verifica si el punto del mouse está cerca del punto del slider o del slider de dados para iniciar el arrastre
        if np.linalg.norm(point - self.slider.punto.get_center()) < 0.25:
            self.arrastrando = self.slider
        # Verifica si el punto del mouse está cerca del punto del slider de dados para iniciar el arrastre
        elif np.linalg.norm(point - self.slider_dados.punto.get_center()) < 0.25:
            self.arrastrando = self.slider_dados
        # Verifica si el punto del mouse está dentro del área del botón de inicio para comenzar la simulación
        elif self.play_button.get_bounding_box()[0][0] <= point[0] <= self.play_button.get_bounding_box()[2][0] \
            and self.play_button.get_bounding_box()[0][1] <= point[1] <= self.play_button.get_bounding_box()[2][1]:
            self.empezar = True
    # Maneja el evento de soltar el mouse después de arrastrar el slider
    def on_mouse_release(self, point, button, mods):
        self.arrastrando = None
    # Maneja el evento de arrastrar el mouse para mover el punto del slider
    def on_mouse_drag(self, point, d_point, buttons, mods):
        if self.arrastrando is not None:
            self.arrastrando.mover_a(point[0])
    # Método principal que construye la escena
    def construct(self):
        # Representación inicial de la distribución de dados con conteos iniciales de 0 para cada suma escalado y posicionado en la esquina superior izquierda
        probabilidades = [0.35, 0.25, 0.17, 0.12, 0.07, 0.04] # Probabilidades sesgadas para cada cara del dado (1 a 6)
        distribucion = DistribucionDados([0] * 6, probabilidades) # Crea la distribución de dados inicial con conteos de 0 para cada suma y las probabilidades sesgadas
        distribucion.scale(1.3) 
        distribucion.to_corner(UL)
        distribucion.shift(LEFT*0.15 + DOWN*0.02)
        self.empezar = False # Variable que indica si se ha presionado el botón de inicio para comenzar la simulación
        self.n_experimentos = 2000 # Número de experimentos inicial (valor máximo del slider)
        valores = [10] + list(range(100, 2001, 100)) # Lista de valores posibles para el slider (entre 10 y 2000 en incrementos de 100)
        slider = Slider(valores) # Crea el slider interactivo para seleccionar el número de experimentos
        slider.scale(0.8) # Escala el slider para que tenga un tamaño adecuado en la escena
        slider.next_to(distribucion, DOWN, buff=0.6) # Posiciona el slider debajo de la distribución de dados con un pequeño espacio
        self.slider = slider # Guarda el slider en la escena para poder acceder a él en los eventos de mouse 
        self.arrastrando = None # Variable que indica si se está arrastrando el punto del slider
        self.add(slider) # Agrega el slider a la escena
        # Crea un segundo slider para seleccionar el número de dados a lanzar (5, 10 o 20)
        valores_dados = [5, 10, 20]
        slider_dados = Slider(
            valores_dados,
            width=2.0,
            label="Dados"
        )
        slider_dados.scale(0.8) # Escala el slider de dados para que tenga un tamaño adecuado en la escena
        slider_dados.move_to([4.9, 2.15, 0]) # Posiciona el slider de dados en la esquina superior derecha de la escena
        self.add(slider_dados) # Agrega el slider de dados a la escena
        self.slider_dados = slider_dados # Guarda el slider de dados en la escena para poder acceder a él en los eventos de mouse
        
        play_rect = Rectangle(width=2.0, height=0.8) # Crea un rectángulo que representa el botón de inicio (PLAY)
        play_rect.set_fill(GREEN, opacity=0.9) # Color de relleno del botón
        play_rect.set_stroke(WHITE, width=2) # Color del borde del botón
        play_text = Text("PLAY").scale(0.55) # Crea el texto "PLAY" que se mostrará en el botón
        play = VGroup(play_rect, play_text) # Agrupa el rectángulo y el texto en un solo objeto para representar el botón de inicio
        play.move_to([4.9, -0.5, 0]) # Posiciona el botón de inicio en la esquina inferior derecha de la escena
        self.play_button = play # Guarda el botón de inicio en la escena para poder acceder a él en los eventos de mouse
        self.add(play)


        # Espera hasta que se presione el botón de inicio (se arrastre el slider y se suelte) para comenzar la simulación
        while not self.empezar:
            self.wait(1 / 60)
        self.remove(slider)
        self.remove(slider_dados)
        self.remove(self.play_button)

        n_experimentos = self.slider.valor() # Obtiene el número de experimentos seleccionado en el slider
        n_dados = self.slider_dados.valor() # Obtiene el número de dados seleccionado en el slider de dados
        histograma = Histograma(n_dados, n_experimentos) # Crea el histograma 
        self.add(histograma) # Agrega el histograma a la escena

        distribucion = DistribucionDados([0] * 6, probabilidades) # Crea la distribución de dados inicial con conteos de 0 para cada suma y las probabilidades sesgadas
        distribucion.scale(1.3) 
        distribucion.to_corner(UL)
        distribucion.shift(LEFT*0.15 + UP*0.35)

        self.add(distribucion) # Agrega la distribución de dados a la escena

        textos_suma_cache = {} # Diccionario para almacenar los objetos de texto de las sumas
        # Renderiza los textos de las sumas de dados (de n_dados a 6*n_dados) y los almacena en el diccionario `textos_suma_cache` para evitar renderizarlos repetidamente durante la animación
        for s in range(n_dados, 6 * n_dados + 1):
            t = Text(f"Sum = {s}").scale(0.9)
            textos_suma_cache[s] = t
        # Genera las tiradas de dados aleatorias y calcula las sumas correspondientes para todos los experimentos
        caras = np.arange(1, 7)

        probabilidades = [0.35, 0.25, 0.17, 0.12, 0.07, 0.04] # Probabilidades sesgadas para cada cara del dado (1 a 6)
        tiradas = np.random.choice(caras, size=(n_experimentos, n_dados), p=probabilidades) # Genera una matriz de tiradas aleatorias de dados con las probabilidades sesgadas
        sumas = tiradas.sum(axis=1) # Calcula la suma de cada tirada de dados para todos los experimentos

        # Agrega el histograma y la distribución de dados a la escena
        self.add(histograma, distribucion)
        # Representación inicial de la tirada de dados, la suma y el contador de experimentos
        tirada_init = tiradas[0]
        # Crea los dados haciendo referencia al Vgroup `Dado`
        dados = VGroup(*[
            Dado(valor=int(v), size=0.42)
            for v in tirada_init
        ])
        filas = n_dados // 5 + (n_dados % 5 > 0) # Calcula el número de filas necesarias para organizar los dados en una cuadrícula de 5 columnas
        columnas = min(n_dados, 5) # Calcula el número de columnas necesarias
        dados.arrange_in_grid(filas, columnas, buff=0.22) # Organiza los dados en una cuadrícula con el número de filas y columnas calculado, con un espacio de 0.22 unidades entre ellos
        dados.move_to([4.9, 2.15, 0]) # Mueve los dados a la posición inicial en la esquina superior derecha

        suma_init = int(sumas[0]) # Suma inicial de la primera tirada de dados
        texto_suma = textos_suma_cache[suma_init].copy() # Crea el texto suma buscando en el diccionario de etxtos renderizados
        texto_suma.next_to(dados, DOWN, buff=0.35) # Posiciona el texto de la suma debajo de los dados con un espacio de 0.35 unidades

        contador = Integer(0) # Contador para mostrar el número de experimentos realizados
        contador.scale(0.7) # Escala del contador
        contador.move_to([-4.9, -0.25, 0]) # Posición del contador
        titulo_contador = Text("Lanzamientos")
        titulo_contador.scale(0.45)
        titulo_contador.next_to(contador, UP, buff=0.15)
        titulo_contador.shift(RIGHT * 0.1)
        self.add(dados, texto_suma, contador, titulo_contador) # Agrega los dados, el texto de la suma y el contador a la escena

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

                nueva_dist = DistribucionDados(conteos, probabilidades) # Crea una nueva distribución de dados con los conteos actualizados
                nueva_dist.scale(1.3) # Escala
                # Posición
                nueva_dist.to_corner(UL)
                nueva_dist.shift(LEFT*0.15 + UP*0.35)
                distribucion.become(nueva_dist) # Actualiza la distribución de dados en la escena con la nueva distribución creada

                # Crea los nuevos dados haciendo referencia al Vgroup `Dado`
                nuevos_dados = VGroup(*[
                    Dado(valor=int(v), size=0.42)
                    for v in tirada
                ])
                # Organiza los nuevos dados en una cuadrícula con el número de filas y columnas calculado, con un espacio de 0.22 unidades entre ellos
                nuevos_dados.arrange_in_grid(filas, columnas, buff=0.22)
                nuevos_dados.move_to([4.9, 2.15, 0]) # Mueve los nuevos dados a la posición en la esquina superior derecha
                dados.become(nuevos_dados) # Actualiza los dados en la escena con los nuevos dados creados

                nuevo_texto = textos_suma_cache[suma].copy() # Crea un nuevo texto de la suma actual buscando en el diccionario de textos renderizados
                nuevo_texto.next_to(nuevos_dados, DOWN, buff=0.35) # Posiciona el nuevo texto
                texto_suma.become(nuevo_texto) # Actualiza el texto de la suma en la escena con el nuevo texto creado

                # Actualiza el contador de experimentos realizados
                contador.set_value(i + 1)

                # Anima la transición en cada salto de animación y en el último experimento
                self.wait(run_time_animacion)

        ## CURVA DE LA NORMAL TEÓRICA
        # Media de un dado cargado
        media_dado = np.sum(caras * probabilidades)
        # Varianza de un dado cargado
        varianza_dado = np.sum(probabilidades * (caras - media_dado) ** 2)
        # Media y desviación para n dados
        mu = n_dados * media_dado
        sigma = np.sqrt(n_dados * varianza_dado)

        x_min = n_dados # Valor mínimo de la suma de los dados (10 para 10 dados)
        x_max = 6 * n_dados # Valor máximo de la suma de los dados (60 para 10 dados)
        x_vals = np.linspace(n_dados, 6 * n_dados, 150) # Valores de 'x'de la curva, desde la suma mínima (10) hasta la suma máxima (60) con 150 puntos para representarla
        # Valores de 'y' de la curva, con la fórmula de la función de densidad
        y_vals = (
            1 / (sigma * np.sqrt(2 * np.pi))
        ) * np.exp(
            -(x_vals - mu)**2 / (2 * sigma**2)
        )
        # Altura hasta donde llega la curva (altura objetivo)
        if n_dados == 5:
            factor_curva = 18
        elif n_dados == 10:
            factor_curva = 23
        elif n_dados == 20:
            factor_curva = 31
        escala_curva = altura_objetivo * factor_curva
        # Calcula los puntos modelandolos a la altura objetivo y anchura del histograma
        puntos = [
            [
                np.interp(x, [n_dados, 6 * n_dados], [-histograma.ancho_total/2, histograma.ancho_total/2]),
                -3.25 + y * escala_curva,
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

        self.wait(2)