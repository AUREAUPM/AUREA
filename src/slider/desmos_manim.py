from manimlib import *

class MiniDesmos(Scene):
    def construct(self):
        # =========================
        # EJE Y CURVA
        # =========================
        self.axes = Axes(x_range=[-4, 4], y_range=[-3, 3], width=6, height=3)
        self.add(self.axes)

        self.a = 1
        self.b = 1

        self.graph = self.get_graph()
        self.add(self.graph)

        # =========================
        # SLIDERS (compactos)
        # =========================
        self.slider_a_line = Line(LEFT * 2.5 + DOWN * 2.5, RIGHT * 2.5 + DOWN * 2.5)
        self.slider_b_line = Line(LEFT * 2.5 + DOWN * 3.2, RIGHT * 2.5 + DOWN * 3.2)

        self.dot_a = Dot(self.slider_a_line.get_start(), color=RED)
        self.dot_b = Dot(self.slider_b_line.get_start(), color=BLUE)

        self.add(self.slider_a_line, self.slider_b_line)
        self.add(self.dot_a, self.dot_b)

        # =========================
        # TEXTO
        # =========================
        self.text = Text("").scale(0.5).to_corner(UP + LEFT)
        self.add(self.text)

        # =========================
        # UPDATERS
        # =========================
        self.graph.add_updater(self.update_graph)
        self.dot_a.add_updater(self.update_slider_a)
        self.dot_b.add_updater(self.update_slider_b)
        self.text.add_updater(self.update_text)

        self.embed()

    # =========================
    # FUNCIÓN
    # =========================
    def get_graph(self):
        return self.axes.get_graph(
            lambda x: self.a * np.sin(x) + self.b * np.cos(x),
            color=interpolate_color(BLUE, RED, abs(self.a - self.b))
        )

    def update_graph(self, mobject, dt):
        new_graph = self.get_graph()
        mobject.become(new_graph)

    # =========================
    # SLIDER A
    # =========================
    def update_slider_a(self, mobject, dt):
        start = self.slider_a_line.get_start()
        end = self.slider_a_line.get_end()
        self.a = np.clip(self.a, -2, 2)
        mobject.move_to(interpolate(start, end, (self.a + 2) / 4))

    # =========================
    # SLIDER B
    # =========================
    def update_slider_b(self, mobject, dt):
        start = self.slider_b_line.get_start()
        end = self.slider_b_line.get_end()
        self.b = np.clip(self.b, -2, 2)
        mobject.move_to(interpolate(start, end, (self.b + 2) / 4))

    # =========================
    # TEXTO EN PANTALLA
    # =========================
    def update_text(self, mobject, dt):
        mobject.text = f"a = {self.a:.2f} | b = {self.b:.2f}"

    # =========================
    # INTERACCIÓN MOUSE
    # =========================
    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        x, y = point[0], point[1]

        # slider A (arriba)
        if y < -2.2:
            self.a = np.clip((x + 2.5) / 5 * 4 - 2, -2, 2)

        # slider B (abajo)
        if y < -2.9:
            self.b = np.clip((x + 2.5) / 5 * 4 - 2, -2, 2)