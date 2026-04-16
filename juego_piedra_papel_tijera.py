import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QStackedLayout, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


class Juego(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Piedra Papel Tijera")
        self.setFixedSize(420, 650)

        # 🎨 estilo tipo Apple oscuro
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f10;
                color: white;
                font-family: -apple-system;
            }

            QFrame {
                background-color: #1c1c1e;
                border-radius: 20px;
            }

            QPushButton {
                background-color: #2c2c2e;
                border-radius: 14px;
                padding: 14px;
                font-size: 16px;
                color: white;
            }

            QPushButton:hover {
                background-color: #3a3a3c;
            }

            QPushButton:pressed {
                background-color: #48484a;
            }
        """)

        # 🎮 lógica
        self.opciones = ["piedra", "papel", "tijera"]
        self.pj = 0
        self.pc = 0
        self.objetivo = 3

        self.eleccion = None
        self.cpu_choice = None

        # 🧠 stack de pantallas
        self.stack = QStackedLayout()

        self.ui_reglas()
        self.ui_jugador()
        self.ui_cpu()
        self.ui_final()

        main = QVBoxLayout()
        main.addLayout(self.stack)
        self.setLayout(main)

        self.stack.setCurrentIndex(0)

    # 📜 PANTALLA 1 → REGLAS + COPYRIGHT
    def ui_reglas(self):
        w = QFrame()
        l = QVBoxLayout(w)

        title = QLabel("📜 REGLAS DEL JUEGO")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))

        reglas = QLabel(
            "• Piedra gana a Tijera\n"
            "• Tijera gana a Papel\n"
            "• Papel gana a Piedra\n\n"
            "🏆 El primero en llegar a 3 puntos gana"
        )
        reglas.setAlignment(Qt.AlignCenter)
        reglas.setFont(QFont("Arial", 14))

        btn = QPushButton("▶ JUGAR")
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        # © copyright
        copyright = QLabel("© promo-67-modulo-1-team-3")
        copyright.setAlignment(Qt.AlignCenter)
        copyright.setFont(QFont("Arial", 15))
        copyright.setStyleSheet("color: #8e8e93;")

        l.addWidget(title)
        l.addWidget(reglas)
        l.addWidget(btn)
        l.addWidget(copyright)

        self.stack.addWidget(w)

    # 🟢 PANTALLA 2 → JUGADOR
    def ui_jugador(self):
        w = QFrame()
        l = QVBoxLayout(w)

        title = QLabel("🟢 TU TURNO")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))

        self.info = QLabel("Elige una opción")
        self.info.setAlignment(Qt.AlignCenter)

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
        l.addWidget(self.info)
        l.addLayout(btns)

        self.stack.addWidget(w)

    # 🤖 PANTALLA 3 → CPU
    def ui_cpu(self):
        w = QFrame()
        l = QVBoxLayout(w)

        title = QLabel("🤖 CPU ELIGIENDO...")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))

        self.cpu_text = QLabel("")
        self.cpu_text.setAlignment(Qt.AlignCenter)
        self.cpu_text.setFont(QFont("Arial", 22))

        l.addWidget(title)
        l.addWidget(self.cpu_text)

        self.stack.addWidget(w)

    # 🏁 PANTALLA 4 → FINAL
    def ui_final(self):
        w = QFrame()
        l = QVBoxLayout(w)

        self.final_text = QLabel("")
        self.final_text.setAlignment(Qt.AlignCenter)
        self.final_text.setFont(QFont("Arial", 22))

        self.score = QLabel("")
        self.score.setAlignment(Qt.AlignCenter)
        self.score.setFont(QFont("Arial", 18))

        btn = QPushButton("🔄 Jugar de nuevo")
        btn.clicked.connect(self.reset)

        l.addWidget(self.final_text)
        l.addWidget(self.score)
        l.addWidget(btn)

        self.stack.addWidget(w)

    # 🎮 JUEGO
    def jugar(self, eleccion):
        self.eleccion = eleccion
        self.cpu_choice = random.choice(self.opciones)

        self.cpu_text.setText("...")

        self.stack.setCurrentIndex(2)

        QTimer.singleShot(800, self.mostrar_cpu)

    def mostrar_cpu(self):
        self.cpu_text.setText(self.cpu_choice.upper())
        QTimer.singleShot(600, self.resolver)

    def resolver(self):
        if (self.eleccion == "piedra" and self.cpu_choice == "tijera") or \
           (self.eleccion == "papel" and self.cpu_choice == "piedra") or \
           (self.eleccion == "tijera" and self.cpu_choice == "papel"):
            self.pj += 1
        elif self.eleccion != self.cpu_choice:
            self.pc += 1

        if self.pj == self.objetivo or self.pc == self.objetivo:
            self.mostrar_final()
        else:
            self.stack.setCurrentIndex(1)

    def mostrar_final(self):
        if self.pj == self.objetivo:
            self.final_text.setText("🏆 GANASTE")
        else:
            self.final_text.setText("💀 PERDISTE")

        self.score.setText(f"{self.pj} - {self.pc}")
        self.stack.setCurrentIndex(3)

    def reset(self):
        self.pj = 0
        self.pc = 0
        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Juego()
    w.show()
    sys.exit(app.exec_())