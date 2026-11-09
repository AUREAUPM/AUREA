from manimlib import *
import random

from dado import GrupoDados


class PanelDados(VGroup):

    def __init__(self):

        super().__init__()

        self.marco = Rectangle(
            width=5,
            height=3,
            stroke_opacity=0,
        )

        self.grupo = GrupoDados([1])
        self.grupo.set_opacity(0)

        self.add(
            self.marco,
            self.grupo,
        )



    def crear_grupo(self, valores):

        grupo = GrupoDados(valores)

        grupo.move_to(
            self.marco.get_center()
        )

        return grupo


    def mostrar_valores(
        self,
        scene,
        valores,
    ):

        nuevo_grupo = self.crear_grupo(
            valores
        )

        scene.remove(
            self.grupo
        )

        self.remove(
            self.grupo
        )

        self.grupo = nuevo_grupo

        self.add(
            self.grupo
        )

        scene.add(
            self.grupo
        )

        scene.play(
            AnimationGroup(
                *[
                    GrowFromCenter(dado)
                    for dado
                    in self.grupo.lista_dados
                ],
                lag_ratio=0.02,
            ),
            run_time=0.20,
        )

    def actualizar_valores(
            self,
            valores,
        ):
    
            nuevo_grupo = self.crear_grupo(
                valores
            )
    
            self.grupo.become(
                nuevo_grupo
            )

    def cambiar_grupo(
        self,
        scene,
        n,
    ):

        valores = [
            random.randint(1, 6)
            for _ in range(n)
        ]

        self.mostrar_valores(
            scene,
            valores,
        )

        