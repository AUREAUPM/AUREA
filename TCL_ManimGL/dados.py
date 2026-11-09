from manimlib import *

from panel_dados import PanelDados
from panel_controles import PanelControles
from panel_distribucion import PanelDistribucion
from panel_distribuciones import PanelDistribuciones
from slider import Slider
from boton import Boton
import numpy as np
import time
from histograma import HistogramaSuma

SALTO_ANIMACION = 5
TIEMPO_ANIMACION = 0.07
Y_INFO_CENTRAL = -0.15


class DemoInterfaz(Scene):

    def construct(self):

        self.panel = PanelDados()

        self.panel_distribucion = PanelDistribucion()

        self.panel_distribuciones = PanelDistribuciones()
        self.add(self.panel_distribuciones)

        self.controles = PanelControles()

        x_dados = (
            self.controles.boton6.get_center()[0]
            + self.controles.boton10.get_center()[0]
        ) / 2

        self.add(self.controles)
        self.add(self.panel)
        self.add(self.panel_distribucion)

        self.panel.move_to(
            [x_dados, 0.85, 0]
        )

        self.slider = Slider(
            valores=[10] + list(range(100, 5001, 100)),
            ancho=2.3,
            etiqueta="Nº lanzamientos",
        )

        self.slider.move_to(
            LEFT * 0.6
            + UP * 2.7
        )

        self.slider.shift(
            UP * (
                self.controles.titulo.get_center()[1]
                - self.slider.etiqueta.get_center()[1]
            )
        )

        self.add(self.slider)

        # Estado del slider
        self.arrastrando_slider = False

        self.boton_simular = Boton(
            "Simular",
            "simular",
            ancho=1.65,
            color=GREEN_D,
            color_activo=GREEN,
        )

        self.boton_simular.fondo.set_stroke(
            WHITE,
            width=4,
        )

        self.boton_simular.move_to(
            RIGHT * 6.1
            + UP * 2.65
        )

        self.boton_simular.set_y(
            self.controles.grupo.get_center()[1]
        )

        self.add(
        self.boton_simular
        )

        self.histograma_suma = None

        self.texto_lanzamientos = None

        self.simulando = False


        self.texto_parametros = None

        self.subtitulo_suma = None


        self.wait()

    def limpiar_resultado(self):

        if self.histograma_suma is not None:

            self.remove(
                self.histograma_suma
            )

        self.histograma_suma = None

        if self.texto_lanzamientos is not None:

            self.remove(
                self.texto_lanzamientos
            )

            self.texto_lanzamientos = None

        if self.texto_parametros is not None:

            self.remove(
                self.texto_parametros
            )
            

            self.texto_parametros = None

        self.wait()

    def ocultar_resultado(self):

        self.simulando = False

        if self.histograma_suma is not None:
            self.histograma_suma.set_opacity(0)

        if self.texto_lanzamientos is not None:
            self.texto_lanzamientos.set_opacity(0)

        if self.texto_parametros is not None:
            self.texto_parametros.set_opacity(0)

    def obtener_n_dados(self):

        n = self.controles.grupo.clave_seleccionada

        if n is None:
            n = 2

        return n


    def simular_tirada(self):

        inicio = time.perf_counter()

        if self.simulando:
            return

        self.simulando = True

        n_dados = self.obtener_n_dados()

        n_experimentos = self.slider.valor()

        if n_experimentos <= 500:
            salto_animacion = 5

        elif n_experimentos <= 1000:
            salto_animacion = 10

        elif n_experimentos <= 2000:
            salto_animacion = 20

        else:
            salto_animacion = 75

        # Eliminamos los parámetros teóricos
        # de la simulación anterior
        if self.texto_parametros is not None:

            self.remove(
                self.texto_parametros
            )

            self.texto_parametros = None    

        # Eliminamos el contador de la simulación anterior
        if self.texto_lanzamientos is not None:

            self.remove(
                self.texto_lanzamientos
            )

        self.texto_progreso = Text(
            f"Progreso: 0/{n_experimentos}",
            font_size=24,
        )

        self.texto_suma = Text(
            "Suma: -",
            font_size=24,
        )

        self.texto_progreso.set_x(
            self.panel.get_center()[0] - 0.90
        )

        self.texto_suma.set_x(
            self.panel.get_center()[0] + 0.90
        )

        self.texto_progreso.set_y(
            Y_INFO_CENTRAL
        )       

        self.texto_suma.align_to(
            self.texto_progreso,
            UP
        )

        self.texto_lanzamientos = VGroup(
            self.texto_progreso,
            self.texto_suma,
        )

        self.add(
            self.texto_lanzamientos
        )

        distribucion = self.panel_distribucion.distribucion


        # Si aún no se ha elegido distribución,
        # utilizamos uniforme.
        if not hasattr(
            distribucion,
            "probabilidades_lista",
        ):

            self.panel_distribuciones.grupo.seleccionar(
                "uniforme"
            )

            self.panel_distribucion.mostrar(
                self,
                "uniforme",
                x_centro=(
                    self.panel_distribuciones
                    .grupo
                    .get_center()[0]
                ),
            )

            distribucion = (
                self.panel_distribucion.distribucion
            )

        probabilidades = (
            distribucion.probabilidades_lista
        )

        # Quitamos el histograma anterior
        if self.histograma_suma is not None:

            self.remove(
                self.histograma_suma
            )

        if self.subtitulo_suma is not None:

            self.remove(
            self.subtitulo_suma
        )

        self.subtitulo_suma = None

        # Creamos el histograma correspondiente
        # al nº de dados actual
        self.histograma_suma = HistogramaSuma(
            n_dados=n_dados,
            n_experimentos=n_experimentos,
        )

    

        # Zona inferior
        self.histograma_suma.move_to(
            DOWN * 3.10
            + LEFT * 0.85
        )

        self.add(
            self.histograma_suma
        )

        self.subtitulo_suma = Text(
            "Distribución de la suma",
            font_size=24,
        )

        self.subtitulo_suma.set_color(
            WHITE
        )

        self.subtitulo_suma.move_to(
           [
                self.histograma_suma.get_center()[0],
                -3.560,
                0,
            ]
        )

        self.add(
        self.subtitulo_suma
        )

        # Generamos TODAS las tiradas de una vez
        tiradas = np.random.choice(
            [1, 2, 3, 4, 5, 6],
            size=(
                n_experimentos,
                n_dados,
            ),
            p=probabilidades,
        )

        sumas = tiradas.sum(axis=1)

        # Ajustamos la escala vertical del histograma
        # a la frecuencia máxima de esta simulación
        valores_unicos, frecuencias = np.unique(
            sumas,
            return_counts=True,
        )

        frecuencia_maxima = frecuencias.max()

        self.histograma_suma.altura_bloque = (
            self.histograma_suma.altura_objetivo
            / (frecuencia_maxima*1.10)
        )

        inicio_lote = 0

        for i in range(n_experimentos):

            renderizar = (
                (i + 1) % salto_animacion == 0
                or i == n_experimentos - 1
            )

            if renderizar:

                # ------------------------------------------
                # Actualizamos el histograma con todo
                # lo ocurrido desde el último refresco
                # ------------------------------------------

                self.histograma_suma.añadir_lote(
                    sumas[
                        inicio_lote:i + 1
                    ]
                )

                # La tirada visible es la última
                # del lote
                tirada = tiradas[i]
                suma = int(sumas[i])

                valores = tirada.tolist()

                # Actualización rápida de los dados
                self.panel.actualizar_valores(
                    valores
                )

                # Flechas de la tirada actual
                conteos = [
                    valores.count(k)
                    for k in range(1, 7)
                ]

                distribucion.mostrar_flechas(
                    conteos
                )

                nuevo_progreso = Text(
                    f"Progreso: {i+1}/{n_experimentos}",
                    font_size=24,
                )

                nueva_suma = Text(
                    f"Suma: {suma}",
                    font_size=24,
                    t2c={
                        str(suma): "#d7ff00"
                    },
                )

                nuevo_progreso.move_to(
                    self.texto_progreso
                )

                nueva_suma.move_to(
                    self.texto_suma
                )

                self.texto_progreso.become(
                    nuevo_progreso
                )

                self.texto_suma.become(
                    nueva_suma
                )

                # El próximo lote empieza
                # después de este lanzamiento
                inicio_lote = i + 1

                self.wait(
                    TIEMPO_ANIMACION
                )


        
       

        if self.histograma_suma.ultimo_activo is not None:

            self.histograma_suma.ultimo_activo.set_fill(
                self.histograma_suma.color_hist,
                opacity=1,
            )



     
   
        # Parámetros teóricos de un dado
        caras = np.array(
            [1, 2, 3, 4, 5, 6]
        )

        probabilidades_np = np.array(
            probabilidades
        )

        media_dado = np.sum(
            caras
            * probabilidades_np
        )

        varianza_dado = np.sum(
            (
                caras
                - media_dado
            ) ** 2
            * probabilidades_np
        )

        # Parámetros de la suma de n dados
        media_suma = (
            n_dados
            * media_dado
        )

        desviacion_suma = np.sqrt(
            n_dados
            * varianza_dado
        )

        # Curva normal teórica
        curva_normal = self.histograma_suma.añadir_curva_normal(
            media=media_suma,
            desviacion=desviacion_suma,
            n_experimentos=n_experimentos,
        )

        titulo_normal = Text(
            "Aproximación normal",
            font_size=28,
        )

        texto_mu = Text(
            f"μ = {media_suma:.2f}",
            font_size=24,
        )

        texto_sigma = Text(
            f"σ = {desviacion_suma:.2f}",
            font_size=24,
        )

        self.texto_parametros = VGroup(
            titulo_normal,
            texto_mu,
            texto_sigma,
        )

        self.texto_parametros.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.12,
        )

        texto_mu.shift(
            RIGHT * 0.50
        )

        texto_sigma.shift(
            RIGHT * 0.50
        )

        self.texto_parametros.set_color(
         "#ffe45c"
        )

        self.texto_parametros.next_to(
            curva_normal,
            RIGHT,
            buff=0.80,
        )


        # Primero aparece suavemente la normal
        self.play(
            FadeIn(curva_normal),
            run_time=0.8,
        )

        # Después aparecen μ y σ
        self.play(
            FadeIn(self.texto_parametros),
            run_time=0.6,
        )

        

        # La simulación ha terminado
        self.simulando = False

    def invalidar_resultado(self):

        if self.histograma_suma is not None:
            self.remove(self.histograma_suma)
            self.histograma_suma = None

        if self.subtitulo_suma is not None:
            self.remove(self.subtitulo_suma)
            self.subtitulo_suma = None

        if self.texto_lanzamientos is not None:
            self.remove(self.texto_lanzamientos)
            self.texto_lanzamientos = None
            self.texto_progreso = None
            self.texto_suma = None

        if self.texto_parametros is not None:
            self.remove(self.texto_parametros)
            self.texto_parametros = None
        


        

        
      


       





    def on_mouse_press(
        self,
        point,
        button,
        mods,
    ):

       
    
        if self.simulando:
            return

        # 1. Slider
        izquierda = self.slider.linea.get_left()[0]
        derecha = self.slider.linea.get_right()[0]

        y_linea = self.slider.linea.get_center()[1]

        dentro_x = (
            izquierda
            <= point[0]
            <= derecha
        )

        cerca_y = (
            abs(
                point[1] - y_linea
            ) < 0.25
        )

        if dentro_x and cerca_y:

            self.arrastrando_slider = True

            self.slider.mover_a(
                point[0]
            )

            return

        # 2. Botón Simular
        if self.boton_simular.contiene_punto(
            point
        ):

            self.simular_tirada()

            return

        # 3. Botones de distribución
        for boton in self.panel_distribuciones.grupo.botones:

            if boton.contiene_punto(point):

                self.invalidar_resultado()

                self.panel_distribuciones.grupo.seleccionar(
                    boton.clave
                )

                self.panel_distribucion.mostrar(
                    self,
                    boton.clave,
                    x_centro=(
                        self.panel_distribuciones
                        .grupo
                        .get_center()[0]
                    ),      
                )

                return

        # 4. Botones del número de dados
        for boton in self.controles.grupo.botones:

            if boton.contiene_punto(point):

                self.invalidar_resultado()

                self.controles.grupo.seleccionar(
                    boton.clave
                )

                self.panel.cambiar_grupo(
                    self,
                    boton.clave
                )
            
                return


    def on_mouse_motion(
        self,
        point,
        d_point,
    ):

        if self.arrastrando_slider:

            self.slider.mover_a(
                point[0]
            )


    def on_mouse_release(
        self,
        point,
        button,
         mods,
    ):

        if self.arrastrando_slider:

            self.invalidar_resultado()

            self.arrastrando_slider = False

    