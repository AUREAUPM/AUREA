from manimlib import *
import numpy as np

class ElipseInteractiva(Scene):
    def construct(self):

        # Parámetros iniciales
        self.a = 3
        self.b = 2

        # Creación de los ejes
        self.axes = Axes(
            x_range=[-6, 6],
            y_range=[-6, 6],
            width=8,
            height=8,
        )
        self.axes.shift(UP * 1.2)
        self.add(self.axes)

        # Creación de la elipse
        self.ellipse = self.get_ellipse()
        self.add(self.ellipse)

        # Creación del slider
        self.slider = Line(
            LEFT * 2.5 + DOWN * 4,
            RIGHT * 2.5 + DOWN * 4,
            color=WHITE
        )
        self.slider_dot = Dot(color=BLUE) # Punto que se moverá a lo largo del slider
        self.add(self.slider)
        self.add(self.slider_dot)

        self.ellipse.add_updater(self.update_ellipse) # Agregamos un updater para la elipse que actualiza su forma cuando cambian los parámetros
        self.slider_dot.add_updater(self.update_slider) # Agregamos un updater para el punto del slider que actualiza su posición cuando cambia el parámetro b
        self.embed() # Inicia la interacción con el usuario

    # Define la función que genera la elipse basada en los parámetros a y b según la ecuación paramétrica x = a * cos(t), y = b * sin(t)
    def get_ellipse(self):
        return ParametricCurve(
            lambda t: self.axes.c2p(
                self.a * np.cos(t),
                self.b * np.sin(t)
            ),
            t_range=(0, TAU, 0.08),
            color=YELLOW,
        )

    # Define el updater para la elipse que redibuja la elipse si el parámetro b cambia
    def update_ellipse(self, mob, dt):
        # Si no ha cambiado el valor de b, no hacemos nada
        if not hasattr(self, "_last_b"):
            self._last_b = self.b
        # Si el valor de b ha cambiado significativamente, actualizamos la elipse
        if abs(self.b - self._last_b) > 0.001:
            mob.become(self.get_ellipse())
            self._last_b = self.b

    # Define el updater para el punto del slider que actualiza su posición a lo largo del slider según el valor de b
    def update_slider(self, mob, dt):
        self.b = np.clip(self.b, 0.5, 5) # Limitamos el valor de b entre 0.5 y 5
        start = self.slider.get_start() # Obtenemos el punto inicial del slider
        end = self.slider.get_end() # Obtenemos el punto final del slider
        alpha = (self.b - 0.5) / 4.5 # Calculamos el valor de alpha que representa la posición del punto a lo largo del slider
        mob.move_to(interpolate(start, end, alpha)) # Movemos el punto a la posición correspondiente en el slider

    # Define la función que maneja el arrastre del mouse para actualizar el valor de b según la posición del mouse
    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        x, y = point[:2]
        if abs(y + 4) < 0.3:
            alpha = np.clip((x + 2.5) / 5, 0, 1)
            self.b = 0.5 + alpha * 4.5