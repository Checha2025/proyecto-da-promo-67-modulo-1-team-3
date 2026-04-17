import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QStackedLayout, QGridLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class VentanaTicTacToe(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RETRO TIC-TAC-TOE")
        self.setFixedSize(500, 850)

        # 🎨 ESTILO RETRO (Basado en tu Ahorcado)
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
                font-size: 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff3b30;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
                border: 4px solid #333;
            }
        """)

        # ⚙️ Lógica original
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.turno = "X"
        self.movimientos = 0
        self.posiciones = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }
        self.botones_teclado = {}

        self.stack = QStackedLayout()
        self.ui_menu()    # 0
        self.ui_juego()   # 1
        self.ui_final()   # 2

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.stack)
        self.setLayout(main_layout)
        self.stack.setCurrentIndex(0)

    def crear_caja(self, layout):
        contenedor = QWidget()
        contenedor.setStyleSheet("background-color: #000; border: 5px solid #fff; border-radius: 15px;")
        contenedor.setLayout(layout)
        return contenedor

    def ui_menu(self):
        l = QVBoxLayout()
        titulo = QLabel("🕹️ TIC-TAC-TOE")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Courier", 30, QFont.Bold))
        
        btn_start = QPushButton("START GAME ▶")
        btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        l.addStretch()
        l.addWidget(titulo)
        l.addSpacing(40)
        l.addWidget(btn_start)
        l.addStretch()
        self.stack.addWidget(self.crear_caja(l))

    # --- 🟢 PANTALLA DE JUEGO (ESTILO AHORCADO) ---
    def ui_juego(self):
        layout_juego = QVBoxLayout()
        layout_juego.setSpacing(15)

        # 1. Indicador de Turno (Arriba)
        self.lbl_turno = QLabel("TURN: X")
        self.lbl_turno.setAlignment(Qt.AlignCenter)
        self.lbl_turno.setFont(QFont("Courier", 25, QFont.Bold))
        self.lbl_turno.setStyleSheet("color: #e52521; border: none;")
        
        caja_turno = self.crear_caja(QVBoxLayout())
        caja_turno.layout().addWidget(self.lbl_turno)
        caja_turno.setFixedHeight(80)

        # 2. Pantalla del Tablero ASCII (Como el dibujo del ahorcado)
        layout_ascii_vertical = QVBoxLayout()
        layout_ascii_vertical.setSpacing(0)      # Sin espacio entre etiquetas
        layout_ascii_vertical.setContentsMargins(0, 0, 0, 0) # Sin márgenes internos
        
        # Añadimos un muelle arriba para empujar el tablero al centro
        layout_ascii_vertical.addStretch()

        self.filas_ascii = []
        for i in range(5):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Courier New", 35, QFont.Bold))
            lbl.setStyleSheet("color: #00FF00; border: none;")
            
            lbl.setFixedHeight(45) # Ajusta este número (40-50) para juntar o separar más
            
            layout_ascii_vertical.addWidget(lbl)
            self.filas_ascii.append(lbl)
            

        layout_ascii_vertical.addStretch()
        caja_ascii = self.crear_caja(layout_ascii_vertical)

        # 3. Teclado de Posiciones (Abajo)
        grid_widget = QWidget()
        grid_teclado = QGridLayout(grid_widget)
        grid_teclado.setSpacing(10)

        for i in range(1, 10):
            btn = QPushButton(str(i))
            btn.setFixedSize(80, 80)
            btn.clicked.connect(lambda ch, n=i: self.procesar_jugada(n))
            
            fila, col = self.posiciones[i]
            grid_teclado.addWidget(btn, fila, col)
            self.botones_teclado[i] = btn

        caja_teclado = self.crear_caja(QVBoxLayout())
        caja_teclado.layout().addWidget(grid_widget)

        layout_juego.addWidget(caja_turno)
        layout_juego.addWidget(caja_ascii, 3) # La pantalla ASCII es más grande
        layout_juego.addWidget(caja_teclado, 2)
        
        container = QWidget()
        container.setLayout(layout_juego)
        self.stack.addWidget(container)

    def ui_final(self):
        l = QVBoxLayout()
        self.msg_final = QLabel("")
        self.msg_final.setAlignment(Qt.AlignCenter)
        self.msg_final.setFont(QFont("Courier", 35, QFont.Bold))

        btn_retry = QPushButton("PLAY AGAIN 🔁")
        btn_retry.setStyleSheet("background-color: #555; border: 4px solid #000;")
        btn_retry.clicked.connect(self.reset_juego)

        l.addStretch()
        l.addWidget(self.msg_final)
        l.addSpacing(40)
        l.addWidget(btn_retry)
        l.addStretch()
        self.stack.addWidget(self.crear_caja(l))

    # --- 🧠 LÓGICA ---

    def actualizar_ascii(self):
        t = self.tablero
        self.filas_ascii[0].setText(f" {t[0][0]} | {t[0][1]} | {t[0][2]} ")
        self.filas_ascii[1].setText("---+---+---")
        self.filas_ascii[2].setText(f" {t[1][0]} | {t[1][1]} | {t[1][2]} ")
        self.filas_ascii[3].setText("---+---+---")
        self.filas_ascii[4].setText(f" {t[2][0]} | {t[2][1]} | {t[2][2]} ")


    def procesar_jugada(self, n):
        fila, col = self.posiciones[n]
        
        if self.tablero[fila][col] == " ":
            self.tablero[fila][col] = self.turno
            self.movimientos += 1
            
            # El botón se deshabilita y se queda gris (según el CSS :disabled)
            self.botones_teclado[n].setEnabled(False)
            
            self.actualizar_ascii()

            if self.verificar_ganador(self.turno):
                self.finalizar(f"WINNER: {self.turno}")
            elif self.movimientos == 9:
                self.finalizar("DRAW! 🤝")
            else:
                self.turno = "O" if self.turno == "X" else "X"
                self.lbl_turno.setText(f"TURN: {self.turno}")
                color = "#e52521" if self.turno == "X" else "#2196F3"
                self.lbl_turno.setStyleSheet(f"color: {color}; border: none;")

    def verificar_ganador(self, jugador):
        t = self.tablero
        if (t[0][0] == t[0][1] == t[0][2] == jugador) or \
           (t[1][0] == t[1][1] == t[1][2] == jugador) or \
           (t[2][0] == t[2][1] == t[2][2] == jugador) or \
           (t[0][0] == t[1][0] == t[2][0] == jugador) or \
           (t[0][1] == t[1][1] == t[2][1] == jugador) or \
           (t[0][2] == t[1][2] == t[2][2] == jugador) or \
           (t[0][0] == t[1][1] == t[2][2] == jugador) or \
           (t[0][2] == t[1][1] == t[2][0] == jugador):
            return True
        return False

    def finalizar(self, msg):
        self.msg_final.setText(msg)
        self.stack.setCurrentIndex(2)

    def reset_juego(self):
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.turno = "X"
        self.movimientos = 0
        self.actualizar_ascii()
        self.lbl_turno.setText("TURN: X")
        self.lbl_turno.setStyleSheet("color: #e52521; border: none;")
        for btn in self.botones_teclado.values():
            btn.setEnabled(True)
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VentanaTicTacToe()
    w.show()
    sys.exit(app.exec_())