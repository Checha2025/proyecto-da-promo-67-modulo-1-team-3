import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QStackedLayout, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


class JuegoPPT(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Piedra Papel Tijera - Retro")
        self.setFixedSize(480, 650)

        # 🎮 ESTILO MARIO BROS
        self.setStyleSheet("""
            QWidget {
                background-color: #5c94fc; /* cielo Mario */
                color: white;
                font-family: Courier;
            }

            QPushButton {
                background-color: #e52521; /* rojo Mario */
                border: 4px solid #000;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;
                color: white;
            }

            QPushButton:hover {
                background-color: #ff3b30;
            }

            QFrame {
                background-color: #1c1c1c;
                border: 5px solid #000;
                border-radius: 15px;
            }
        """)

        # 🎮 lógica
        self.opciones = ["piedra", "papel", "tijera"]
        self.pj = 0
        self.pc = 0
        self.objetivo = 3

        # 🎰 animación CPU
        self.timer_anim = QTimer()
        self.timer_anim.timeout.connect(self.animar_cpu)
        self.anim_index = 0

        # stack
        self.stack = QStackedLayout()

        self.ui_reglas()
        self.ui_jugador()
        self.ui_cpu()
        self.ui_vs()        
        self.ui_final()

        main = QVBoxLayout()
        main.addLayout(self.stack)
        self.setLayout(main)

        self.stack.setCurrentIndex(0)

    # 🍄 caja tipo juego retro
    def caja(self, layout):
        contenedor = QWidget()
        contenedor.setStyleSheet("""
            background-color: #000;
            border: 5px solid #fff;
            border-radius: 15px;
        """)
        contenedor.setLayout(layout)
        return contenedor

    # 📜 reglas
    def ui_reglas(self):
        l = QVBoxLayout()

        title = QLabel("PIEDRA PAPEL TIJERA")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Courier", 25, QFont.Bold))

        reglas = QLabel(
            "▶ Tijera vence Papel\n"
            "▶ Papel vence Piedra\n"
            " ▶ Piedra vence Tijera\n\n"
            "🏆 Gana quien llegue a 3"
        )
        reglas.setAlignment(Qt.AlignCenter)

        reglas.setFont(QFont("Courier", 12)) 

        btn = QPushButton("START ▶")

        btn.setFont(QFont("Courier", 18, QFont.Bold)) 
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        l.addWidget(title)
        l.addWidget(reglas)
        l.addWidget(btn)

        self.stack.addWidget(self.caja(l))

    # 🟢 jugador
    def ui_jugador(self):
        l = QVBoxLayout()

        title = QLabel("👾 PLAYER")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Courier", 30, QFont.Bold))

        self.score_live = QLabel("0 - 0")
        self.score_live.setAlignment(Qt.AlignCenter)
        self.score_live.setFont(QFont("Courier", 25, QFont.Bold))

        self.info = QLabel("SELECT YOUR MOVE")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setFont(QFont("Courier", 16, QFont.Bold))

        btns = QHBoxLayout()

        b1 = QPushButton("✊")
        b2 = QPushButton("✋")
        b3 = QPushButton("✂")

        b1.clicked.connect(lambda: self.jugar("piedra"))
        b2.clicked.connect(lambda: self.jugar("papel"))
        b3.clicked.connect(lambda: self.jugar("tijera"))

        btns.addWidget(b1)
        btns.addWidget(b2)
        btns.addWidget(b3)

        l.addWidget(title)
        l.addWidget(self.score_live)
        l.addWidget(self.info)
        l.addLayout(btns)

        self.stack.addWidget(self.caja(l))

    # 🤖 CPU
    def ui_cpu(self):
        l = QVBoxLayout()

        title = QLabel("👾 BOWSER CPU")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Courier", 16, QFont.Bold))

        self.cpu_text = QLabel("❔")
        self.cpu_text.setAlignment(Qt.AlignCenter)
        self.cpu_text.setFont(QFont("Courier", 60))

        l.addWidget(title)
        l.addWidget(self.cpu_text)

        self.stack.addWidget(self.caja(l))

    # ⚔️ VS SCREEN
    def ui_vs(self):
        l = QVBoxLayout()
        
        title = QLabel("PLAYER vs BOWSER CPU")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Courier", 18, QFont.Bold))

        vs_layout = QHBoxLayout()
        
        self.vs_player = QLabel("")
        self.vs_player.setAlignment(Qt.AlignCenter)
        self.vs_player.setFont(QFont("Courier", 60))
        
        vs_txt = QLabel("VS")
        vs_txt.setAlignment(Qt.AlignCenter)
        vs_txt.setFont(QFont("Courier", 20, QFont.Bold))

        self.vs_cpu = QLabel("")
        self.vs_cpu.setAlignment(Qt.AlignCenter)
        self.vs_cpu.setFont(QFont("Courier", 60))

        vs_layout.addWidget(self.vs_player)
        vs_layout.addWidget(vs_txt)
        vs_layout.addWidget(self.vs_cpu)

        self.vs_resultado = QLabel("") 
        self.vs_resultado.setAlignment(Qt.AlignCenter)
        self.vs_resultado.setFont(QFont("Courier", 22, QFont.Bold))

        l.addWidget(title)
        l.addLayout(vs_layout)
        l.addWidget(self.vs_resultado)
        self.stack.addWidget(self.caja(l))

    # 🏁 final
    def ui_final(self):
        l = QVBoxLayout()

        self.final_text = QLabel("")
        self.final_text.setAlignment(Qt.AlignCenter)
        self.final_text.setFont(QFont("Courier", 20))

        self.score = QLabel("")
        self.score.setAlignment(Qt.AlignCenter)

        btn = QPushButton("RESTART 🔁")
        btn.clicked.connect(self.reset)
        btn.setFont(QFont("Courier", 18, QFont.Bold))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #555; 
                border: 4px solid #000;
                color: white;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)

        l.addWidget(self.final_text)
        l.addWidget(self.score)
        l.addWidget(btn)

        self.stack.addWidget(self.caja(l))

    # 🎮 jugar
    def jugar(self, eleccion):
        self.eleccion = eleccion
        self.cpu_choice = random.choice(self.opciones)

        self.stack.setCurrentIndex(2)

        self.anim_index = 0
        self.timer_anim.start(120)

        QTimer.singleShot(1200, self.parar_animacion)

    # 🎰 animación
    def animar_cpu(self):
        emojis = ["✊", "✋", "✂"]
        self.cpu_text.setText(emojis[self.anim_index % 3])
        self.anim_index += 1

    # 🛑 parar
    def parar_animacion(self):
        self.timer_anim.stop()
        mapa = {"piedra": "✊", "papel": "✋", "tijera": "✂"}
        self.cpu_text.setText(mapa[self.cpu_choice])
        
        # Esperamos 1 segundo viendo la elección de Bowser antes del VS
        QTimer.singleShot(1000, self.mostrar_vs)

    def mostrar_vs(self):
        mapa = {"piedra": "✊", "papel": "✋", "tijera": "✂"}
        # Seteamos los iconos elegidos
        self.vs_player.setText(mapa[self.eleccion])
        self.vs_cpu.setText(mapa[self.cpu_choice])
        
        if self.eleccion == self.cpu_choice:
            texto = "DRAW! 🤝"
            color = "white"
        elif (self.eleccion == "piedra" and self.cpu_choice == "tijera") or \
             (self.eleccion == "papel" and self.cpu_choice == "piedra") or \
             (self.eleccion == "tijera" and self.cpu_choice == "papel"):
            texto = "POINT FOR PLAYER! ⭐"
            color = "#00FF00" # Verde
        else:
            texto = "POINT FOR BOWSER! 💀"
            color = "#e52521" # Rojo

        self.vs_resultado.setText(texto)
        self.vs_resultado.setStyleSheet(f"color: {color};")

        self.stack.setCurrentIndex(3)
        QTimer.singleShot(2500, self.resolver)
    

    # 🧠 lógica
    def resolver(self):
        if (self.eleccion == "piedra" and self.cpu_choice == "tijera") or \
           (self.eleccion == "papel" and self.cpu_choice == "piedra") or \
           (self.eleccion == "tijera" and self.cpu_choice == "papel"):
            self.pj += 1
        elif self.eleccion != self.cpu_choice:
            self.pc += 1

        self.score_live.setText(f"{self.pj} - {self.pc}")

        if self.pj == self.objetivo or self.pc == self.objetivo:
            self.mostrar_final()
        else:
            self.stack.setCurrentIndex(1)

    # 🏁 final
    def mostrar_final(self):
        self.final_text.setText("🏆 YOU WIN!" if self.pj > self.pc else "💀 GAME OVER")
        self.final_text.setFont(QFont("Courier", 20, QFont.Bold))
        self.score.setText(f"{self.pj} - {self.pc}")
        self.score.setFont(QFont("Courier", 20, QFont.Bold))
        self.stack.setCurrentIndex(4)

    # 🔄 reset
    def reset(self):
        self.pj = 0
        self.pc = 0
        self.score_live.setText("0 - 0")
        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = JuegoPPT()
    w.show()
    sys.exit(app.exec_())