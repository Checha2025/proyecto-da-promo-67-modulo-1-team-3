import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

# --- ASCII ANIMATIONS ---

ascii_ahorcado = [
r'''
      +
      |
      |
      |
      |
      |
=========''',
r'''
  +---+
  |   |
      |
      |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''',
]

ascii_tictactoe = [
"X | O | X \n---+---+---\nO | X | O \n---+---+---\n X | O | X ",
"|   |   \n---+---+---\n|   |   \n---+---+---\n   |   |   ",
]

ascii_ppt = [
r"""
   _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)""",
r"""
_______
 ---'    ____)____
             ______)
             _______)
          _______)
---.__________)""",
r"""
_______
 ---'   ____)____
            ______)
         __________)
      (____)
---.__(___)""",
]

ascii_trivia = [
r'''
 ____

 / /  \ \
      | |
     / /
  |_|

  |_|
''',r'''
_________
|  _____  |
| |     | |
| |_____| |
|_________|
        ''',
r'''
________
/    |    \
| ~~~~|~~~~ |
| ~~~~|~~~~ |
| ____|____ |
|/        \|
     '''
]


# -------------------------------------------------------
# PANTALLA DE BIENVENIDA
# -------------------------------------------------------

class PantallaBienvenida(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕹️ RETRO GAMES")
        self.setFixedSize(780, 860)

        self.setStyleSheet("""
            QWidget {
                background-color: #000;
                color: #fff;
                font-family: Courier;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        # Decoración superior
        deco = QLabel("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■")
        deco.setAlignment(Qt.AlignCenter)
        deco.setFont(QFont("Courier", 14, QFont.Bold))
        deco.setStyleSheet("color: #e52521; border: none;")
        layout.addWidget(deco)
        layout.addSpacing(18)

        # Título
        titulo = QLabel("► RETRO GAME SA ◄")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Courier", 22, QFont.Bold))
        titulo.setStyleSheet("color: #FFD700; border: none;")
        layout.addWidget(titulo)

        empresa = QLabel("@RetroGameSA")
        empresa.setAlignment(Qt.AlignCenter)
        empresa.setFont(QFont("Courier", 13))
        empresa.setStyleSheet("color: #00FF00; border: none;")
        layout.addWidget(empresa)
        layout.addSpacing(30)

        # Separador
        layout.addWidget(self._separador("#5c94fc"))
        layout.addSpacing(10)

        # Sección equipo
        lbl_equipo = QLabel("◆ EQUIPO DE DESARROLLO")
        lbl_equipo.setFont(QFont("Courier", 10, QFont.Bold))
        lbl_equipo.setStyleSheet("color: #5c94fc; border: none;")
        layout.addWidget(lbl_equipo)
        layout.addSpacing(12)

        integrantes = [
            ("María de Los Ángeles Toro Cabezas", "SCRUM TEAM"),
            ("María Cecilia Martínez",             "SCRUM MASTER"),
            ("Natividad de María Guerrero Opazo",  "SCRUM TEAM"),
            ("Alicia Simancas Fernández",           "SCRUM TEAM"),
        ]
        for nombre, rol in integrantes:
            fila = QHBoxLayout()
            lbl_nombre = QLabel(f"► {nombre}")
            lbl_nombre.setFont(QFont("Courier", 9))
            lbl_nombre.setStyleSheet("color: #fff; border: none;")

            lbl_rol = QLabel(f"[ {rol} ]")
            lbl_rol.setFont(QFont("Courier", 8))
            lbl_rol.setStyleSheet("color: #00FF00; border: none;")
            lbl_rol.setAlignment(Qt.AlignRight)

            fila.addWidget(lbl_nombre)
            fila.addWidget(lbl_rol)
            layout.addLayout(fila)
            layout.addSpacing(6)

        layout.addSpacing(18)
        layout.addWidget(self._separador("#333"))
        layout.addSpacing(12)

        # Sección información
        lbl_info_titulo = QLabel("◆ DESCRIPCIÓN DEL PROYECTO")
        lbl_info_titulo.setFont(QFont("Courier", 10, QFont.Bold))
        lbl_info_titulo.setStyleSheet("color: #5c94fc; border: none;")
        layout.addWidget(lbl_info_titulo)
        layout.addSpacing(10)

        info_box = QLabel(
            "La cliente necesita juegos clásicos\n"
            "programados en Python.\n"
            "Pide creatividad e iniciativa."
        )
        info_box.setFont(QFont("Courier", 10))
        info_box.setStyleSheet(
            "color: #ccc;"
            "background-color: #111;"
            "border: 2px solid #5c94fc;"
            "border-radius: 8px;"
            "padding: 14px;"
        )
        layout.addWidget(info_box)

        layout.addStretch()

        # Botón START con parpadeo
        self.btn_start = QPushButton("►► START ◄◄")
        self.btn_start.setFont(QFont("Courier", 18, QFont.Bold))
        self.btn_start.setFixedHeight(62)
        self._estilo_start_on()
        self.btn_start.clicked.connect(self.iniciar_juego)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

        self.blink_state = True
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._parpadeo)
        self.blink_timer.start(600)

        self.menu = None

    def _separador(self, color):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {color}; border: 1px solid {color};")
        return line

    def _estilo_start_on(self):
        self.btn_start.setStyleSheet(
            "QPushButton {"
            "  background-color: #000;"
            "  border: 4px solid #FFD700;"
            "  border-radius: 10px;"
            "  color: #FFD700;"
            "  font-size: 20px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover { background-color: #222; }"
        )

    def _estilo_start_off(self):
        self.btn_start.setStyleSheet(
            "QPushButton {"
            "  background-color: #000;"
            "  border: 4px solid #555;"
            "  border-radius: 10px;"
            "  color: #555;"
            "  font-size: 20px;"
            "  font-weight: bold;"
            "}"
            "QPushButton:hover { background-color: #222; }"
        )

    def _parpadeo(self):
        self.blink_state = not self.blink_state
        if self.blink_state:
            self._estilo_start_on()
        else:
            self._estilo_start_off()

    def iniciar_juego(self):
        self.blink_timer.stop()
        self.menu = MenuPrincipal()
        self.menu.show()
        self.close()


# -------------------------------------------------------
# TARJETA DE JUEGO (preview animado)
# -------------------------------------------------------

class TarjetaJuego(QWidget):
    """Tarjeta con preview ASCII animado + botón de juego."""
    def __init__(self, titulo, ascii_list, color_ascii, btn_texto, callback):
        super().__init__()
        self.ascii_list = ascii_list
        self.ascii_index = 0

        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(8, 8, 8, 8)

        # ASCII display
        self.lbl_ascii = QLabel(ascii_list[0])
        self.lbl_ascii.setAlignment(Qt.AlignCenter)
        self.lbl_ascii.setFont(QFont("Courier New", 13, QFont.Bold))
        self.lbl_ascii.setStyleSheet(f"color: {color_ascii}; border: none; background-color: #000;")
        self.lbl_ascii.setFixedHeight(220)

        # Botón
        btn = QPushButton(btn_texto)
        btn.setFont(QFont("Courier", 16, QFont.Bold))
        btn.setFixedHeight(55)
        btn.setStyleSheet(
            "QPushButton { background-color: #000; border: 4px solid #fff; border-radius: 10px; color: white; font-weight: bold; font-size: 18px;}"
            "QPushButton:hover { background-color: #333; }"
        )
        btn.clicked.connect(callback)

        layout.addWidget(self.lbl_ascii)
        layout.addWidget(btn)

        contenedor = QWidget()
        contenedor.setStyleSheet(
            "background-color: #000; border: 4px solid #fff; border-radius: 12px;"
        )
        contenedor.setLayout(layout)

        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(contenedor)
        self.setLayout(outer)

        # Timer animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.animar)
        self.timer.start(1000)

    def animar(self):
        self.ascii_index = (self.ascii_index + 1) % len(self.ascii_list)
        self.lbl_ascii.setText(self.ascii_list[self.ascii_index])


# -------------------------------------------------------
# MENÚ PRINCIPAL
# -------------------------------------------------------

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕹️ RETRO GAMES")
        self.setFixedSize(780, 860)

        self.setStyleSheet("""
            QWidget {
                background-color: #5c94fc;
                color: white;
                font-family: Courier;
            }
            QPushButton {
                background-color: #e52521;
                border: 4px solid #000;
                border-radius: 10px;
                padding: 6px;
                font-size: 13px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(22, 22, 22, 22)

        titulo = QLabel("🕹️ RETRO GAMES")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Courier", 28, QFont.Bold))

        # Grid 2x2 de tarjetas
        fila1 = QHBoxLayout()
        fila1.setSpacing(12)
        fila2 = QHBoxLayout()
        fila2.setSpacing(12)

        fila1.addWidget(TarjetaJuego(
            "AHORCADO", ascii_ahorcado, "#00FF00",
            "💀 AHORCADO 🪵", self.abrir_ahorcado
        ))
        fila1.addWidget(TarjetaJuego(
            "TIC-TAC-TOE", ascii_tictactoe, "#00FF00",
            "❌ TIC-TAC-TOE ⭕", self.abrir_tictactoe
        ))
        fila2.addWidget(TarjetaJuego(
            "PIEDRA PAPEL TIJERA", ascii_ppt, "#00FF00",
            "✊ PIEDRA PAPEL TIJERA", self.abrir_ppt
        ))
        fila2.addWidget(TarjetaJuego(
            "TRIVIA", ascii_trivia, "#00FF00",
            "🧠 TRIVIA", self.abrir_trivia
        ))

        layout.addWidget(titulo)
        layout.addLayout(fila1)
        layout.addLayout(fila2)
        self.setLayout(layout)

        self.ventanas = []

    def abrir_ahorcado(self):
        from Ahorcado_interfaz_py5 import VentanaAhorcado
        w = VentanaAhorcado()
        w.show()
        self.ventanas.append(w)

    def abrir_tictactoe(self):
        from Tictactoe_interfaz import VentanaTicTacToe
        w = VentanaTicTacToe()
        w.show()
        self.ventanas.append(w)

    def abrir_ppt(self):
        from juego_piedra_papel_tijera import JuegoPPT
        w = JuegoPPT()
        w.show()
        self.ventanas.append(w)

    def abrir_trivia(self):
        from Preguntas_y_respuestas_interfaz import JuegoTrivia
        w = JuegoTrivia()
        w.show()
        self.ventanas.append(w)


# -------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = PantallaBienvenida()
    splash.show()
    sys.exit(app.exec_())