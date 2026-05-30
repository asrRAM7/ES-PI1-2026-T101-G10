import menus
import auditoria
from asciimatics.effects import Print, Scroll
from asciimatics.renderers import ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene
from asciimatics.event import KeyboardEvent

auditoria.criar_log()

def ascii(screen):

    estado = {"cena_atual": 0}
    TOTAL_CENAS = 3

    def verificar_enter(tecla):
        if isinstance(tecla, KeyboardEvent) and tecla.key_code == 13:
            if estado["cena_atual"] < TOTAL_CENAS - 1:
                estado["cena_atual"] += 1
                raise NextScene(f"cena{estado['cena_atual']}")
            else:
                raise StopApplication("ENTER na última cena")
    scenes = []
    effects = [
        Print(screen,
              ColourImageFile(screen, "colour_globe.gif", screen.height-2,
                              uni=screen.unicode_aware,
                              dither=screen.unicode_aware),
              1,
              stop_frame=200),
        Print(screen,
              FigletText("LAD.py",
                         font='banner3' if screen.width > 80 else 'banner'),
              screen.height//2-3,
              colour=7, bg=7 if screen.unicode_aware else 0),
    ]
    scenes.append(Scene(effects, name="cena0"))
    effects = [
        Print(screen,
              FigletText("Grupo - 10\nGabriel Hernandes\nGabriel Lara\nMatthius dhusdjsld\nRamiro Alexander",
                         font='banner'),
              screen.height,
              speed=1,
              stop_frame=(40+screen.height)*3),
        Scroll(screen, 3)
    ]
    scenes.append(Scene(effects, name="cena1"))
    effects = [
        Print(screen,
              ColourImageFile(screen, "colour_globe.gif", screen.height-2,
                              uni=screen.unicode_aware,
                              dither=screen.unicode_aware),
              1,
              stop_frame=200),
        Print(screen,
              FigletText("Pressione ENTER",
                         font='banner'),
              screen.height//2-3,
              colour=7, bg=7 if screen.unicode_aware else 0),
    ]
    scenes.append(Scene(effects, name="cena2"))
    screen.play(scenes, stop_on_resize=True, unhandled_input=verificar_enter)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(ascii)
            break
        except ResizeScreenError:
            estado = {"cena_atual": 0}
    menus.main_menu()
    auditoria.criar_log()
