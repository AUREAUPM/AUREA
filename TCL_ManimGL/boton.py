from manimlib import *


class Boton(VGroup):

    def __init__(
        self,
        texto,
        clave,
        ancho=1.2,
        alto=0.6,
        color=BLUE_D,
        color_activo="#d9a066",
    ):

        super().__init__()

        self.texto = texto
        self.clave = clave

        self.seleccionado = False

        self.color_normal = color
        self.color_activo = color_activo

        self.fondo = RoundedRectangle(
            corner_radius=0.12,
            width=ancho,
            height=alto,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )

        self.etiqueta = Text(
            str(texto),
            font_size=30,
        )

        self.etiqueta.move_to(
            self.fondo.get_center()
        )

        self.add(
            self.fondo,
            self.etiqueta,
        )


    def seleccionar(self):

        self.seleccionado = True

        self.fondo.set_fill(
            self.color_activo,
            opacity=1,
        )

        self.fondo.set_stroke(
            WHITE,
            width=3,

        )
        self.etiqueta.set_color(
            "#1f1f1f"
        )


    def deseleccionar(self):

        self.seleccionado = False

        self.fondo.set_fill(
            self.color_normal,
            opacity=1,
        )

        self.fondo.set_stroke(
            WHITE,
            width=2,
        )
          
        self.etiqueta.set_color(
            WHITE
        )


    def contiene_punto(self, punto):

        centro = self.get_center()

        ancho = self.fondo.get_width()
        alto = self.fondo.get_height()

        return (
            abs(punto[0] - centro[0]) <= ancho / 2
            and
            abs(punto[1] - centro[1]) <= alto / 2
        )


class GrupoBotones(VGroup):

    def __init__(self):

        super().__init__()

        self.botones = []

        self.clave_seleccionada = None


    def agregar(self, boton):

        self.botones.append(
            boton
        )

        self.add(
            boton
        )


    def seleccionar(self, clave):

        self.clave_seleccionada = clave

        for boton in self.botones:

            if boton.clave == clave:

                boton.seleccionar()

            else:

                boton.deseleccionar()


    def organizar(
        self,
        separacion=0.4,
    ):

        self.arrange(
            RIGHT,
            buff=separacion,
        )