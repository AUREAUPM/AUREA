"""Simulación animada de la suma de dados.

Renderizar desde la raíz: manim -ql Notebooks/escena_final.py EscenaDados
"""

from dataclasses import dataclass

import numpy as np
from manim import *


@dataclass(frozen=True)
class ConfiguracionSimulacion:
    n_dados: int = 10
    n_experimentos: int = 800
    salto_animacion: int = 4
    duracion_frame: float = 0.07
    altura_objetivo: float = 3.0
    semilla: int | None = None
    proporcion_pico_estimada: float = 0.06
    factor_escala_curva: float = 18.0

    base_histograma_y: float = -3.1
    ancho_histograma: float = 9.5
    dados_por_fila: int = 5

    def __post_init__(self):
        if self.n_dados <= 0:
            raise ValueError("n_dados debe ser mayor que cero")
        if self.n_experimentos <= 0:
            raise ValueError("n_experimentos debe ser mayor que cero")
        if self.salto_animacion <= 0:
            raise ValueError("salto_animacion debe ser mayor que cero")
        if self.dados_por_fila <= 0:
            raise ValueError("dados_por_fila debe ser mayor que cero")
        if self.proporcion_pico_estimada <= 0:
            raise ValueError("proporcion_pico_estimada debe ser mayor que cero")

    @property
    def suma_minima(self):
        return self.n_dados

    @property
    def suma_maxima(self):
        return 6 * self.n_dados


CONFIG = ConfiguracionSimulacion()


class Dado(VGroup):
    PATRONES = {
        1: [(0, 0)],
        2: [(-1, -1), (1, 1)],
        3: [(-1, -1), (0, 0), (1, 1)],
        4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
        6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)],
    }

    def __init__(self, valor=1, size=0.42):
        super().__init__()
        if valor not in self.PATRONES:
            raise ValueError("El valor del dado debe estar entre 1 y 6")

        borde = RoundedRectangle(
            corner_radius=0.08,
            width=size,
            height=size,
            stroke_width=1.8,
            stroke_color=WHITE,
            fill_color="#1f1f1f",
            fill_opacity=1,
        )
        separacion = size * 0.24
        puntos = VGroup(
            *[
                Dot(
                    point=[x * separacion, y * separacion, 0],
                    radius=size * 0.06,
                    color="#5dade2",
                )
                for x, y in self.PATRONES[valor]
            ]
        )
        self.add(borde, puntos)


class Histograma(VGroup):
    COLOR_HISTOGRAMA = "#7bc96f"
    COLOR_ACTIVO = "#d9a066"
    COLOR_EJE = "#d8d8d8"

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.x_min = config.suma_minima
        self.x_max = config.suma_maxima
        self.base_y = config.base_histograma_y
        self.ancho_total = config.ancho_histograma
        self.altura_bloque = config.altura_objetivo / (
            config.proporcion_pico_estimada * config.n_experimentos
        )
        self.ancho_bloque = 0.16
        self.bloques_por_suma = {
            suma: [] for suma in range(self.x_min, self.x_max + 1)
        }
        self.ultimo_activo = None

        self.add(
            Line(
                [-self.ancho_total / 2, self.base_y, 0],
                [self.ancho_total / 2, self.base_y, 0],
                color=self.COLOR_EJE,
                stroke_width=1.6,
            )
        )
        self._agregar_marcas()

    def x_para_suma(self, suma):
        return np.interp(
            suma,
            [self.x_min, self.x_max],
            [-self.ancho_total / 2, self.ancho_total / 2],
        )

    def _agregar_marcas(self):
        for suma in range(self.x_min, self.x_max + 1):
            x = self.x_para_suma(suma)
            tick = Line(
                [x, self.base_y - 0.07, 0],
                [x, self.base_y + 0.07, 0],
                color=self.COLOR_EJE,
                stroke_width=1,
            )
            self.add(tick)
            if suma % 2 == 0:
                etiqueta = Text(str(suma), font_size=12, color=self.COLOR_EJE)
                etiqueta.move_to([x, self.base_y - 0.22, 0])
                self.add(etiqueta)

    def añadir_bloque(self, suma):
        if suma not in self.bloques_por_suma:
            raise ValueError(f"La suma {suma} está fuera del rango del histograma")
        if self.ultimo_activo is not None:
            self.ultimo_activo.set_fill(self.COLOR_HISTOGRAMA)

        columna = self.bloques_por_suma[suma]
        y = self.base_y + self.altura_bloque * (len(columna) + 0.5)
        bloque = Rectangle(width=self.ancho_bloque, height=self.altura_bloque)
        bloque.set_fill(self.COLOR_ACTIVO, opacity=1)
        bloque.set_stroke(width=0)
        bloque.move_to([self.x_para_suma(suma), y, 0])

        columna.append(bloque)
        self.ultimo_activo = bloque
        self.add(bloque)
        return bloque


class DistribucionDados(VGroup):
    COLOR_EJE = "#d8d8d8"
    COLOR_BARRA = "#2d9cdb"
    COLOR_FLECHA = "#ffe45c"
    PROBABILIDAD = 1 / 6

    def __init__(self, conteos):
        super().__init__()
        if len(conteos) != 6:
            raise ValueError("conteos debe contener seis valores")

        self._agregar_ejes()
        for cara, cantidad in enumerate(conteos, start=1):
            self._agregar_columna(cara, cantidad)

    def _agregar_ejes(self):
        ancho_total = 3.5
        altura_maxima = 0.9
        self.add(
            Line(
                [0, 0, 0],
                [ancho_total, 0, 0],
                color=self.COLOR_EJE,
                stroke_width=1.6,
            ),
            Line(
                [0, 0, 0],
                [0, altura_maxima, 0],
                color=self.COLOR_EJE,
                stroke_width=1.6,
            ),
        )
        for valor, texto in [(0, "0.00"), (0.25, "0.25"), (0.50, "0.50")]:
            tick = Line(
                [-0.045, valor, 0],
                [0.045, valor, 0],
                color=self.COLOR_EJE,
                stroke_width=1.2,
            )
            etiqueta = Text(texto, font_size=13, color=self.COLOR_EJE)
            etiqueta.next_to(tick, LEFT, buff=0.04)
            self.add(tick, etiqueta)

    def _agregar_columna(self, cara, cantidad):
        x = 0.42 + (cara - 1) * 0.56
        altura = self.PROBABILIDAD
        barra = Rectangle(width=0.48, height=altura)
        barra.set_fill(self.COLOR_BARRA, opacity=0.9)
        barra.set_stroke(width=0)
        barra.move_to([x, altura / 2, 0])

        dado = Dado(valor=cara, size=0.24)
        dado.move_to([x, -0.30, 0])
        self.add(barra, dado)

        for indice in range(cantidad):
            flecha = Arrow(
                start=[0, 0.06, 0],
                end=[0, 0, 0],
                buff=0,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.7,
                color=self.COLOR_FLECHA,
            )
            flecha.scale(0.11)
            flecha.move_to([x, altura + 0.05 + indice * 0.07, 0])
            self.add(flecha)


def generar_tiradas(config):
    rng = np.random.default_rng(config.semilla)
    tiradas = rng.integers(
        1,
        7,
        size=(config.n_experimentos, config.n_dados),
    )
    return tiradas, tiradas.sum(axis=1)


def crear_dados(valores, config):
    dados = VGroup(*[Dado(valor=int(valor), size=0.42) for valor in valores])
    dados.arrange_in_grid(
        cols=min(config.dados_por_fila, len(valores)),
        buff=0.22,
    )
    dados.move_to([4.9, 2.15, 0])
    return dados


def crear_distribucion(conteos):
    distribucion = DistribucionDados(conteos)
    distribucion.scale(1.3)
    distribucion.to_corner(UL)
    distribucion.shift(LEFT * 0.15 + DOWN * 0.02)
    return distribucion


def crear_curva_normal(config, histograma):
    media = config.n_dados * 3.5
    desviacion = np.sqrt(config.n_dados * 35 / 12)
    valores_x = np.linspace(config.suma_minima, config.suma_maxima, 150)
    densidades = (
        np.exp(-((valores_x - media) ** 2) / (2 * desviacion**2))
        / (desviacion * np.sqrt(2 * np.pi))
    )
    escala = config.altura_objetivo * config.factor_escala_curva
    puntos = [
        [
            histograma.x_para_suma(x),
            histograma.base_y + densidad * escala,
            0,
        ]
        for x, densidad in zip(valores_x, densidades)
    ]
    curva = VMobject()
    curva.set_points_smoothly(puntos)
    curva.set_color(YELLOW)
    curva.set_stroke(width=2.2)
    return curva


class EscenaDados(Scene):
    config = CONFIG

    def construct(self):
        tiradas, sumas = generar_tiradas(self.config)
        textos_suma = {
            suma: Tex(f"Sum = {suma}").scale(0.9)
            for suma in range(self.config.suma_minima, self.config.suma_maxima + 1)
        }

        histograma = Histograma(self.config)
        distribucion = crear_distribucion([0] * 6)
        curva = crear_curva_normal(self.config, histograma)

        self.play(Create(curva), run_time=1.5)
        self.add(histograma, distribucion)

        dados = crear_dados(tiradas[0], self.config)
        texto_suma = textos_suma[int(sumas[0])].copy()
        texto_suma.next_to(dados, DOWN, buff=0.35)
        contador = Integer(0).scale(0.7)
        contador.move_to([-4.9, -0.25, 0])
        self.add(dados, texto_suma, contador)

        for indice, (tirada, suma) in enumerate(zip(tiradas, sumas)):
            suma = int(suma)
            histograma.añadir_bloque(suma)
            if not self._debe_renderizar(indice):
                continue

            conteos = np.bincount(tirada, minlength=7)[1:].tolist()
            distribucion.become(crear_distribucion(conteos))

            nuevos_dados = crear_dados(tirada, self.config)
            dados.become(nuevos_dados)
            nuevo_texto = textos_suma[suma].copy()
            nuevo_texto.next_to(nuevos_dados, DOWN, buff=0.35)
            texto_suma.become(nuevo_texto)

            contador.set_value(indice + 1)
            self.wait(self.config.duracion_frame)

        self.wait(2)

    def _debe_renderizar(self, indice):
        return (
            indice % self.config.salto_animacion
            == self.config.salto_animacion - 1
            or indice == self.config.n_experimentos - 1
        )
