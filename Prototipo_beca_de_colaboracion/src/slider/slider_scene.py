from manimlib import *

class SliderExample(Scene):
    def construct(self):
        # =========================
        # OBJETO PRINCIPAL
        # =========================
        self.circle = Circle().scale(0.6)
        self.add(self.circle)

        # =========================
        # SLIDER (más compacto)
        # =========================
        self.line = Line(LEFT * 2, RIGHT * 2)
        self.dot = Dot(self.line.get_start(), color=YELLOW)

        self.line.shift(DOWN * 2)
        self.dot.shift(DOWN * 2)

        self.add(self.line, self.dot)

        # valor del slider
        self.value = 0

        # =========================
        # TEXTO NUMÉRICO
        # =========================
        self.value_text = Text("0.00").scale(0.6)
        self.value_text.to_corner(UP + LEFT)
        self.add(self.value_text)

        # =========================
        # UPDATERS (correctos en ManimGL)
        # =========================
        self.circle.add_updater(self.update_circle)
        self.dot.add_updater(self.update_slider)
        self.value_text.add_updater(self.update_text)

        self.embed()

    # =========================
    # CÍRCULO (COLOR DINÁMICO)
    # =========================
    def update_circle(self, mobject, dt):
        # tamaño dinámico
        scale = 0.4 + self.value * 2
        mobject.set_width(scale)

        # color dinámico (azul → rojo)
        color = interpolate_color(BLUE, RED, self.value)
        mobject.set_color(color)

    # =========================
    # SLIDER
    # =========================
    def update_slider(self, mobject, dt):
        start = self.line.get_start()
        end = self.line.get_end()
        mobject.move_to(interpolate(start, end, self.value))

    # =========================
    # TEXTO NUMÉRICO
    # =========================
    def update_text(self, mobject, dt):
        mobject.text = f"{self.value:.2f}"

    # =========================
    # CONTROL MOUSE
    # =========================
    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        x = point[0]

        # mapa [-2, 2] → [0, 1]
        self.value = np.clip((x + 2) / 4, 0, 1)