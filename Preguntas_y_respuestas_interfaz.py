import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QStackedLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

preguntas_trivia = [
    {
        "categoria": "Ciencias",
        "pregunta": "¿Cuál es el planeta más\ngrande del sistema solar?",
        "opciones": ["Marte", "Júpiter", "Saturno", "Venus"],
        "respuesta": "Júpiter"
    },
    {
        "categoria": "Historia",
        "pregunta": "¿En qué año comenzó la\nSegunda Guerra Mundial?",
        "opciones": ["1939", "1945", "1914", "1929"],
        "respuesta": "1939"
    },
    {
        "categoria": "Entretenimiento",
        "pregunta": "¿Quién protagoniza\nla saga Indiana Jones?",
        "opciones": ["Brad Pitt", "Harrison Ford", "Tom Cruise", "Johnny Depp"],
        "respuesta": "Harrison Ford"
    },
    {
        "categoria": "Ciencias",
        "pregunta": "¿Cuál es el elemento\nquímico con símbolo Au?",
        "opciones": ["Plata", "Oro", "Aluminio", "Cobre"],
        "respuesta": "Oro"
    },
    {
        "categoria": "Historia",
        "pregunta": "¿Quién fue el primer\npresidente de EE.UU.?",
        "opciones": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"],
        "respuesta": "George Washington"
    },
    {
        "categoria": "Entretenimiento",
        "pregunta": "¿En qué país se produjo\n'La Casa de Papel'?",
        "opciones": ["México", "Argentina", "España", "Colombia"],
        "respuesta": "España"
    },
    {
        "categoria": "Cultura General",
        "pregunta": "¿Cuántos continentes\nhay en la Tierra?",
        "opciones": ["5", "6", "7", "8"],
        "respuesta": "7"
    },
    {
        "categoria": "Ciencias",
        "pregunta": "¿Cuántos huesos tiene\nel cuerpo humano adulto?",
        "opciones": ["206", "312", "180", "250"],
        "respuesta": "206"
    },
    {
        "categoria": "Historia",
        "pregunta": "¿En qué ciudad fue\nasesinado Julius Caesar?",
        "opciones": ["Atenas", "Roma", "Cartago", "Alejandría"],
        "respuesta": "Roma"
    },
    {
        "categoria": "Cultura General",
        "pregunta": "¿Qué idioma\nse habla en Brasil?",
        "opciones": ["Español", "Francés", "Portugués", "Italiano"],
        "respuesta": "Portugués"
    }
]


class JuegoTrivia(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RETRO TRIVIA")
        self.setFixedSize(480, 650)

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
                padding: 10px;
                font-size: 18px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff3b30;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #666;
                border: 4px solid #666;
            }
        """)

        self.preguntas = preguntas_trivia[:]
        random.shuffle(self.preguntas)
        self.indice = 0
        self.puntuacion = 0
        self.incorrectas = 0
        self.respondida = False

        self.stack = QStackedLayout()
        self.ui_menu()       # 0
        self.ui_pregunta()   # 1
        self.ui_resultado()  # 2
        self.ui_final()      # 3

        main = QVBoxLayout()
        main.addLayout(self.stack)
        self.setLayout(main)
        self.stack.setCurrentIndex(0)

    def caja(self, layout):
        contenedor = QWidget()
        contenedor.setStyleSheet(
            "background-color: #000; border: 5px solid #fff; border-radius: 15px;"
        )
        contenedor.setLayout(layout)
        return contenedor

    # --- MENÚ ---
    def ui_menu(self):
        l = QVBoxLayout()
        l.setSpacing(15)

        title = QLabel("🧠 TRIVIA")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Courier", 35, QFont.Bold))

        info = QLabel(
            f"\n▶ {len(preguntas_trivia)} preguntas\n"
            "▶ 4 opciones por pregunta\n"
            "▶ ¡Solo una es correcta!\n\n"
            "  🏆 ¿Cuántas acertarás?\n"
        )
        info.setAlignment(Qt.AlignLeft)
        info.setFont(QFont("Courier", 12))
        info.setContentsMargins(35, 15, 0, 15)

        btn = QPushButton("START ▶")
        btn.setFont(QFont("Courier", 18, QFont.Bold))
        btn.clicked.connect(self.iniciar_juego)

        l.addStretch()
        l.addWidget(title)
        l.addSpacing(10)
        l.addWidget(info)
        l.addSpacing(20)
        l.addWidget(btn)
        l.addStretch()
        self.stack.addWidget(self.caja(l))

    # --- PREGUNTA ---
    def ui_pregunta(self):
        l = QVBoxLayout()
        l.setSpacing(12)

        # Cabecera: categoría + progreso
        cabecera = QHBoxLayout()
        self.lbl_categoria = QLabel("CATEGORÍA")
        self.lbl_categoria.setFont(QFont("Courier", 11, QFont.Bold))
        self.lbl_categoria.setStyleSheet("color: #FFD700; border: none;")

        self.lbl_progreso = QLabel("1 / 10")
        self.lbl_progreso.setFont(QFont("Courier", 11, QFont.Bold))
        self.lbl_progreso.setStyleSheet("color: #aaa; border: none;")
        self.lbl_progreso.setAlignment(Qt.AlignRight)

        cabecera.addWidget(self.lbl_categoria)
        cabecera.addWidget(self.lbl_progreso)

        # Puntuación en vivo
        self.lbl_score_live = QLabel("✅ 0   ❌ 0")
        self.lbl_score_live.setAlignment(Qt.AlignCenter)
        self.lbl_score_live.setFont(QFont("Courier", 13, QFont.Bold))
        self.lbl_score_live.setStyleSheet("color: white; border: none;")

        # Caja de pregunta
        caja_pregunta_layout = QVBoxLayout()
        self.lbl_pregunta = QLabel("¿Pregunta?")
        self.lbl_pregunta.setAlignment(Qt.AlignCenter)
        self.lbl_pregunta.setFont(QFont("Courier", 15, QFont.Bold))
        self.lbl_pregunta.setStyleSheet("color: #00FF00; border: none;")
        self.lbl_pregunta.setWordWrap(True)
        caja_pregunta_layout.addWidget(self.lbl_pregunta)
        caja_pregunta = self.caja(caja_pregunta_layout)
        caja_pregunta.setFixedHeight(130)

        # Botones A B C D — uno debajo de otro, alineados a la izquierda
        self.botones_opciones = []
        letras = ["A", "B", "C", "D"]
        col_opciones = QVBoxLayout()
        col_opciones.setSpacing(8)

        for i in range(4):
            btn = QPushButton(f"{letras[i]}. ---")
            btn.setFixedHeight(55)
            btn.setFont(QFont("Courier", 13, QFont.Bold))
            btn.setStyleSheet(
                "QPushButton { text-align: left; padding-left: 14px; }"
                "QPushButton:hover { background-color: #ff3b30; }"
            )
            btn.clicked.connect(lambda ch, idx=i: self.responder(idx))
            self.botones_opciones.append(btn)
            col_opciones.addWidget(btn)

        caja_opciones_layout = QVBoxLayout()
        caja_opciones_layout.addLayout(col_opciones)
        caja_opciones = self.caja(caja_opciones_layout)

        # Caja cabecera: categoría + progreso + score
        caja_cab_layout = QVBoxLayout()
        caja_cab_layout.setSpacing(4)
        caja_cab_layout.addLayout(cabecera)
        caja_cab_layout.addWidget(self.lbl_score_live)
        caja_cabecera = self.caja(caja_cab_layout)
        caja_cabecera.setFixedHeight(80)

        l.addWidget(caja_cabecera)
        l.addWidget(caja_pregunta, 2)
        l.addWidget(caja_opciones, 3)

        container = QWidget()
        container.setLayout(l)
        self.stack.addWidget(container)

    # --- RESULTADO DE CADA RONDA ---
    def ui_resultado(self):
        l = QVBoxLayout()
        l.setSpacing(20)

        self.lbl_resultado_icono = QLabel("✅")
        self.lbl_resultado_icono.setAlignment(Qt.AlignCenter)
        self.lbl_resultado_icono.setFont(QFont("Courier", 60))
        self.lbl_resultado_icono.setStyleSheet("border: none;")

        self.lbl_resultado_texto = QLabel("")
        self.lbl_resultado_texto.setAlignment(Qt.AlignCenter)
        self.lbl_resultado_texto.setFont(QFont("Courier", 18, QFont.Bold))
        self.lbl_resultado_texto.setStyleSheet("border: none;")
        self.lbl_resultado_texto.setWordWrap(True)

        self.lbl_respuesta_correcta = QLabel("")
        self.lbl_respuesta_correcta.setAlignment(Qt.AlignCenter)
        self.lbl_respuesta_correcta.setFont(QFont("Courier", 13))
        self.lbl_respuesta_correcta.setStyleSheet("color: #aaa; border: none;")
        self.lbl_respuesta_correcta.setWordWrap(True)

        l.addStretch()
        l.addWidget(self.lbl_resultado_icono)
        l.addWidget(self.lbl_resultado_texto)
        l.addWidget(self.lbl_respuesta_correcta)
        l.addStretch()

        self.stack.addWidget(self.caja(l))

    # --- FINAL ---
    def ui_final(self):
        l = QVBoxLayout()
        l.setSpacing(15)

        self.lbl_final_titulo = QLabel("GAME OVER")
        self.lbl_final_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_final_titulo.setFont(QFont("Courier", 28, QFont.Bold))
        self.lbl_final_titulo.setStyleSheet("border: none;")

        self.lbl_final_score = QLabel("")
        self.lbl_final_score.setAlignment(Qt.AlignCenter)
        self.lbl_final_score.setFont(QFont("Courier", 18, QFont.Bold))
        self.lbl_final_score.setStyleSheet("color: #FFD700; border: none;")

        self.lbl_final_detalle = QLabel("")
        self.lbl_final_detalle.setAlignment(Qt.AlignCenter)
        self.lbl_final_detalle.setFont(QFont("Courier", 13))
        self.lbl_final_detalle.setStyleSheet("color: #aaa; border: none;")

        btn = QPushButton("PLAY AGAIN 🔁")
        btn.setFont(QFont("Courier", 16, QFont.Bold))
        btn.setStyleSheet(
            "QPushButton { background-color: #555; border: 4px solid #000; color: white; }"
            "QPushButton:hover { background-color: #777; }"
        )
        btn.clicked.connect(self.reset)

        l.addStretch()
        l.addWidget(self.lbl_final_titulo)
        l.addSpacing(10)
        l.addWidget(self.lbl_final_score)
        l.addWidget(self.lbl_final_detalle)
        l.addSpacing(20)
        l.addWidget(btn)
        l.addStretch()

        self.stack.addWidget(self.caja(l))

    # --- LÓGICA ---

    def iniciar_juego(self):
        self.preguntas = preguntas_trivia[:]
        random.shuffle(self.preguntas)
        self.indice = 0
        self.puntuacion = 0
        self.incorrectas = 0
        self.cargar_pregunta()
        self.stack.setCurrentIndex(1)

    def cargar_pregunta(self):
        self.respondida = False
        p = self.preguntas[self.indice]

        self.lbl_categoria.setText(f"📂 {p['categoria'].upper()}")
        self.lbl_progreso.setText(f"{self.indice + 1} / {len(self.preguntas)}")
        self.lbl_score_live.setText(f"✅ {self.puntuacion}   ❌ {self.incorrectas}")
        self.lbl_pregunta.setText(p["pregunta"])

        opciones = p["opciones"][:]
        random.shuffle(opciones)
        self.opciones_actuales = opciones

        letras = ["A", "B", "C", "D"]
        for i, btn in enumerate(self.botones_opciones):
            btn.setText(f"{letras[i]}. {opciones[i]}")
            btn.setEnabled(True)
            btn.setStyleSheet(
                "QPushButton { text-align: left; padding-left: 20px; }"
                "QPushButton:hover { background-color: #222; }"
            )

    def responder(self, idx):
        if self.respondida:
            return
        self.respondida = True

        p = self.preguntas[self.indice]
        elegida = self.opciones_actuales[idx]
        correcta = p["respuesta"]

        # Colorear botones
        letras = ["A", "B", "C", "D"]
        for i, btn in enumerate(self.botones_opciones):
            btn.setEnabled(False)
            if self.opciones_actuales[i] == correcta:
                btn.setStyleSheet(
                    "background-color: #00AA00; color: white; border: 4px solid #00FF00;"
                    "border-radius: 10px; font-size: 13px; font-weight: bold;"
                    "text-align: left; padding-left: 14px;"
                )
            elif i == idx:
                btn.setStyleSheet(
                    "background-color: #AA0000; color: white; border: 4px solid #FF0000;"
                    "border-radius: 10px; font-size: 13px; font-weight: bold;"
                    "text-align: left; padding-left: 14px;"
                )
            else:
                btn.setStyleSheet(
                    "background-color: #000; color: #555; border: 4px solid #555;"
                    "border-radius: 10px; font-size: 13px; font-weight: bold;"
                    "text-align: left; padding-left: 14px;"
                )

        if elegida.lower() == correcta.lower():
            self.puntuacion += 1
            self.lbl_resultado_icono.setText("✅")
            self.lbl_resultado_texto.setText("¡CORRECTO!")
            self.lbl_resultado_texto.setStyleSheet("color: #00FF00; border: none;")
            self.lbl_respuesta_correcta.setText(f"Respuesta: {correcta}")
        else:
            self.incorrectas += 1
            self.lbl_resultado_icono.setText("❌")
            self.lbl_resultado_texto.setText("¡INCORRECTO!")
            self.lbl_resultado_texto.setStyleSheet("color: #e52521; border: none;")
            self.lbl_respuesta_correcta.setText(
                f"Tu respuesta: {elegida}\nRespuesta correcta: {correcta}"
            )

        # Mostrar resultado brevemente y pasar
        QTimer.singleShot(600, self.mostrar_resultado)

    def mostrar_resultado(self):
        self.stack.setCurrentIndex(2)
        QTimer.singleShot(2000, self.siguiente_pregunta)

    def siguiente_pregunta(self):
        self.indice += 1
        if self.indice >= len(self.preguntas):
            self.mostrar_final()
        else:
            self.cargar_pregunta()
            self.stack.setCurrentIndex(1)

    def mostrar_final(self):
        total = len(self.preguntas)
        pct = int((self.puntuacion / total) * 100)

        if pct == 100:
            titulo = "🏆 PERFECTO!"
            color = "#FFD700"
        elif pct >= 70:
            titulo = "⭐ BIEN HECHO!"
            color = "#00FF00"
        elif pct >= 40:
            titulo = "😅 PUEDES MEJORAR"
            color = "white"
        else:
            titulo = "💀 GAME OVER"
            color = "#e52521"

        self.lbl_final_titulo.setText(titulo)
        self.lbl_final_titulo.setStyleSheet(f"color: {color}; border: none;")
        self.lbl_final_score.setText(f"✅ {self.puntuacion} / {total}")
        self.lbl_final_detalle.setText(f"Correctas: {self.puntuacion}   Incorrectas: {self.incorrectas}\n{pct}% de acierto")
        self.stack.setCurrentIndex(3)

    def reset(self):
        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = JuegoTrivia()
    w.show()
    sys.exit(app.exec_())