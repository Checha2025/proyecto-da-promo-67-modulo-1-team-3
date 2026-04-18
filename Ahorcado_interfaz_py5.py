import sys
import random
import traceback
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QStackedLayout, QHBoxLayout, QGridLayout, QLineEdit, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# --- CONFIGURACIÓN DE ERRORES ---
def exception_hook(exctype, value, tb):
    print(''.join(traceback.format_exception(exctype, value, tb)))
    sys.exit(1)
sys.excepthook = exception_hook

# --- IMÁGENES ---
imagenes = [ r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', r'''
  +---+
  |   |
      |
      |
      |
      |
=========''', r'''
      +
      |
      |
      |
      |
      |
=========''', r'''
      
      
      
      
      
      
=========''' ]

trofeo_ascii = r'''
 ___________
 '._==_==_=_.'
 .-\:      /-.
 | (|:.     |) |
 '-|:.     |-'
 \::.    /
 '::. .'
 ) (
 _.' '._
   `"""""""`  '''

class VentanaAhorcado(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AHORCADO")
        self.setFixedSize(500, 850) # Aumentado ligeramente para el botón nuevo

        # 🎨 ESTILO RETRO STYLE
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
                font-size: 16px;
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
            QLineEdit {
                background-color: white;
                color: black;
                border: 3px solid #e52521;
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
            }
        """)

        # ⚙️ Lógica inicial
        self.biblioteca_facil = ["canguro", "destino", "sobremesa", "carruaje", "arrebatar", "pescuezo", "columpiar", "bostezar", "mueca", "titubear", "monigote", "arañazo", "peluche", "elefante", "escorpion", "ventana", "biblioteca", "cucaracha", "tortuga", "mariposa", "televisor", "paraguas", "telefono", "ordenador", "camiseta", "escritorio"]
        self.biblioteca_dificil = ["kiwi", "vortice", "azahar", "boxeo", "filigrana", "zurdo", "cuchicheo", "jirafa", "ametralladora"]
        
        self.vidas_iniciales = 8
        self.vidas_actuales = 8
        self.palabra_secreta = ""
        self.espacios = []
        self.botones_letras = {}

        # 🧱 Estructura de pantallas
        self.stack = QStackedLayout()
        
        self.ui_menu_dificultad() # Index 0
        self.ui_menu_modo()       # Index 1
        self.ui_entrada_amigo()   # Index 2
        self.ui_juego()           # Index 3
        self.ui_final()           # Index 4

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.stack)
        self.setLayout(main_layout)
        
        self.stack.setCurrentIndex(0)

    def crear_caja(self, layout):
        contenedor = QWidget()
        contenedor.setStyleSheet("background-color: #000; border: 5px solid #fff; border-radius: 15px;")
        contenedor.setLayout(layout)
        return contenedor

    # --- 📜 PANTALLA 0: DIFICULTAD ---
    def ui_menu_dificultad(self):
        l = QVBoxLayout()
        titulo = QLabel("💀 AHORCADO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Courier", 24, QFont.Bold))
        
        btn_facil = QPushButton("EASY (8 LIVES)")
        btn_dificil = QPushButton("HARD (6 LIVES)")
        
        btn_facil.clicked.connect(lambda: self.set_dificultad(8))
        btn_dificil.clicked.connect(lambda: self.set_dificultad(6))

        l.addWidget(titulo)
        l.addSpacing(30)
        l.addWidget(btn_facil)
        l.addWidget(btn_dificil)
        self.stack.addWidget(self.crear_caja(l))

    # --- 📜 PANTALLA 1: MODO DE JUEGO ---
    def ui_menu_modo(self):
        l = QVBoxLayout()
        titulo = QLabel("SELECT MODE")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Courier", 20))

        btn_solo = QPushButton("VS CPU 👾")
        btn_amigo = QPushButton("VS FRIEND 👥")
        btn_volver = QPushButton("BACK ⬅")
        btn_volver.setStyleSheet("background-color: #555; border: 4px solid #000;")
        
        btn_solo.clicked.connect(self.iniciar_modo_solo)
        btn_amigo.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_volver.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        l.addWidget(titulo)
        l.addSpacing(20)
        l.addWidget(btn_solo)
        l.addWidget(btn_amigo)
        l.addSpacing(20)
        l.addWidget(btn_volver)
        self.stack.addWidget(self.crear_caja(l))

    # --- 📜 PANTALLA 2: ENTRADA PALABRA AMIGO ---
    # --- 📜 PANTALLA 2: ENTRADA PALABRA AMIGO (ESTILO CONSOLA TOTAL) ---
    def ui_entrada_amigo(self):
        l = QVBoxLayout()
        l.setSpacing(15)

        titulo = QLabel("🪓 PLAYER 1 🪓")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Courier", 30, QFont.Bold))
        titulo.setStyleSheet("color: white; border: none;")

        # --- CAJA DE "WORD" MÁS PEQUEÑA ---
        layout_pass = QVBoxLayout()
        self.display_password = QLabel("WORD: ")
        self.display_password.setAlignment(Qt.AlignCenter)
        self.display_password.setFont(QFont("Courier", 20, QFont.Bold))
        self.display_password.setStyleSheet("color: white; border: none;")
        layout_pass.addWidget(self.display_password)
        
        caja_pass = self.crear_caja(layout_pass)
        caja_pass.setFixedHeight(80) # Altura reducida para que sea compacta

        # --- TECLADO QWERTY CENTRADO ---
        self.palabra_temporal_amigo = ""
        widget_teclado_amigo = QWidget()
        grid_amigo = QGridLayout(widget_teclado_amigo)
        grid_amigo.setSpacing(5)
        grid_amigo.setAlignment(Qt.AlignCenter)

        letras_qwerty = [
            'Q','W','E','R','T','Y','U','I','O','P',
            'A','S','D','F','G','H','J','K','L','Ñ',
            'Z','X','C','V','B','N','M'
        ]

        for i, letra in enumerate(letras_qwerty):
            btn = QPushButton(letra)
            btn.setFixedSize(42, 45)
            # Estilo igual al teclado de juego (Negro/Blanco)
            btn.setStyleSheet("""
                QPushButton { background-color: #000; color: #FFF; border: 2px solid #FFF; border-radius: 5px; font-weight: bold; }
                QPushButton:hover { background-color: #333; }
            """)
            btn.clicked.connect(lambda ch, l=letra: self.teclear_amigo(l))
            
            if i < 10: grid_amigo.addWidget(btn, 0, i)
            elif i < 20: grid_amigo.addWidget(btn, 1, i-10)
            else: grid_amigo.addWidget(btn, 2, i-18)

        # --- BOTONES DE CONTROL (NEGRO Y BLANCO) ---
        btns_control = QHBoxLayout()
        
        btn_borrar = QPushButton("DELETE ⌫")
        btn_borrar.setFixedSize(140, 50)
        btn_borrar.setStyleSheet("background-color: #555;")
        btn_borrar.clicked.connect(self.borrar_letra_amigo)

        btn_listo = QPushButton("CONFIRM ▶")
        btn_listo.setFixedSize(140, 50)
        btn_listo.setStyleSheet("background-color: #000; color: white; border: 2px solid white;")
        btn_listo.clicked.connect(self.confirmar_palabra_amigo)

        btns_control.addStretch()
        btns_control.addWidget(btn_borrar)
        btns_control.addSpacing(10)
        btns_control.addWidget(btn_listo)
        btns_control.addStretch()

        btn_volver = QPushButton("BACK ⬅")
        btn_volver.setStyleSheet("background-color: #555; border: 4px solid #000;")
        btn_volver.clicked.connect(self.cancelar_amigo)

        l.addWidget(titulo)
        l.addWidget(caja_pass)
        l.addWidget(widget_teclado_amigo)
        l.addLayout(btns_control)
        l.addSpacing(10)
        l.addWidget(btn_volver)
        
        self.stack.addWidget(self.crear_caja(l))

    # --- LÓGICA DE APOYO ---
    def teclear_amigo(self, letra):
        self.palabra_temporal_amigo += letra
        self.display_password.setText("WORD: " + "*" * len(self.palabra_temporal_amigo))

    def borrar_letra_amigo(self):
        self.palabra_temporal_amigo = self.palabra_temporal_amigo[:-1]
        self.display_password.setText("WORD: " + "*" * len(self.palabra_temporal_amigo))

    def confirmar_palabra_amigo(self):
        if len(self.palabra_temporal_amigo) > 0:
            self.palabra_secreta = self.palabra_temporal_amigo.upper()
            self.palabra_temporal_amigo = ""
            self.display_password.setText("WORD: ")
            self.preparar_tablero()

    def cancelar_amigo(self):
        self.palabra_temporal_amigo = ""
        self.display_password.setText("WORD: ")
        self.stack.setCurrentIndex(1)

    # --- 🟢 PANTALLA 3: EL JUEGO ---
    def ui_juego(self):
        self.pantalla_juego_completa = QWidget()
        self.pantalla_juego_completa.setStyleSheet("background-color: #000;")
        
        layout_principal_juego = QVBoxLayout(self.pantalla_juego_completa)
        layout_principal_juego.setSpacing(10)
        
        # 1. Caja para las VIDAS
        layout_vidas = QVBoxLayout()
        self.score_lbl = QLabel("LIVES: 8")
        self.score_lbl.setAlignment(Qt.AlignCenter)
        self.score_lbl.setFont(QFont("Courier", 30, QFont.Bold))
        self.score_lbl.setStyleSheet("color: #e52521; border: none;") 
        layout_vidas.addWidget(self.score_lbl)
        caja_vidas = self.crear_caja(layout_vidas)
        caja_vidas.setFixedHeight(80)

        # 2. Caja para el DIBUJO
        layout_dibujo = QVBoxLayout()
        self.canvas = QLabel(imagenes[8])
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setStyleSheet("""
            color: #00FF00; 
            border: none; 
            font-family: 'Courier New', monospace; 
            font-size: 22pt; 
            line-height: 100%;
        """)
        layout_dibujo.addWidget(self.canvas)
        caja_dibujo = self.crear_caja(layout_dibujo)

        # 3. Caja para la PALABRA
        layout_palabra = QVBoxLayout()
        self.word_lbl = QLabel("_ _ _ _")
        self.word_lbl.setAlignment(Qt.AlignCenter)
        self.word_lbl.setFont(QFont("Courier", 26, QFont.Bold))
        self.word_lbl.setStyleSheet("color: white; border: none;")
        layout_palabra.addWidget(self.word_lbl)
        caja_palabra = self.crear_caja(layout_palabra)
        caja_palabra.setFixedHeight(100)

        # 4. TECLADO
        widget_teclado = QWidget()
        widget_teclado.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: #FFF;
                border: 2px solid #FFF;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333;
            }
            QPushButton:disabled {
                color: #555;
                border: 2px solid #555;
                background-color: #000;
            }
        """)
        
        self.grid_teclado = QGridLayout(widget_teclado)
        self.grid_teclado.setSpacing(8)
        self.grid_teclado.setAlignment(Qt.AlignCenter)

        letras = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Ñ','Z','X','C','V','B','N','M']
        
        for i, letra in enumerate(letras):
            btn = QPushButton(letra)
            btn.setFixedSize(42, 45)
            btn.clicked.connect(lambda ch, l=letra: self.intentar_letra(l))
            
            if i < 10: self.grid_teclado.addWidget(btn, 0, i)
            elif i < 20: self.grid_teclado.addWidget(btn, 1, i-10)
            else: self.grid_teclado.addWidget(btn, 2, i-18)
            
            self.botones_letras[letra] = btn

        # 🏳️ BOTÓN RENDIRSE (SURRENDER)
        btn_rendirse = QPushButton("SURRENDER 🏳️")
        btn_rendirse.setStyleSheet("""
            background-color: #555; 
            color: white; 
            border: 2px solid white; 
            font-size: 14px;
        """)
        btn_rendirse.clicked.connect(lambda: self.mostrar_resultado(False))

        # Montamos todo en el layout principal
        layout_principal_juego.addWidget(caja_vidas, 1)    
        layout_principal_juego.addWidget(caja_dibujo, 4)   
        layout_principal_juego.addWidget(caja_palabra, 1) 
        layout_principal_juego.addWidget(widget_teclado, 2)
        layout_principal_juego.addWidget(btn_rendirse, 0, Qt.AlignCenter) # Añadido aquí abajo
        
        self.stack.addWidget(self.pantalla_juego_completa)

    # --- 🏁 PANTALLA 4: FINAL ---
    def ui_final(self):
        layout_final_completo = QVBoxLayout()
        layout_final_completo.setSpacing(10)

        # 1. Caja para el MENSAJE (Victoria/Derrota)
        layout_msg = QVBoxLayout()
        self.msg_final = QLabel("")
        self.msg_final.setAlignment(Qt.AlignCenter)
        self.msg_final.setFont(QFont("Courier", 24, QFont.Bold))
        layout_msg.addWidget(self.msg_final)
        self.caja_msg_final = self.crear_caja(layout_msg)
        self.caja_msg_final.setFixedHeight(80)

        # 2. Caja para el CANVAS (Trofeo o Ahorcado)
        layout_canvas = QVBoxLayout()
        self.canvas_final = QLabel("")
        self.canvas_final.setAlignment(Qt.AlignCenter)
        self.canvas_final.setStyleSheet("""
            color: #00FF00; 
            font-family: 'Courier New', monospace; 
            font-size: 18pt; 
            font-weight: bold;
        """)
        layout_canvas.addWidget(self.canvas_final)
        self.caja_canvas_final = self.crear_caja(layout_canvas)

        # 3. Caja para la PALABRA REVELADA
        layout_revelar = QVBoxLayout()
        self.revelar_lbl = QLabel("")
        self.revelar_lbl.setAlignment(Qt.AlignCenter)
        self.revelar_lbl.setFont(QFont("Courier", 16, QFont.Bold))
        self.revelar_lbl.setStyleSheet("color: white; border: none;")
        layout_revelar.addWidget(self.revelar_lbl)
        self.caja_revelar = self.crear_caja(layout_revelar)
        self.caja_revelar.setFixedHeight(80)

        # 4. Botón de Reinicio
        btn_retry = QPushButton("PLAY AGAIN 🔁")
        btn_retry.setStyleSheet("background-color: #555; border: 4px solid #000;")
        btn_retry.clicked.connect(self.volver_al_inicio)

        layout_final_completo.addWidget(self.caja_msg_final, 1)
        layout_final_completo.addWidget(self.caja_canvas_final, 4) # Mayor peso al dibujo
        layout_final_completo.addWidget(self.caja_revelar, 1)
        layout_final_completo.addWidget(btn_retry, 0)

        # Contenedor para que el fondo sea negro
        container = QWidget()
        container.setStyleSheet("background-color: #000;")
        container.setLayout(layout_final_completo)
        self.stack.addWidget(container)

    # --- 🧠 LÓGICA ---
    def set_dificultad(self, vidas):
        self.vidas_iniciales = vidas
        self.biblioteca = self.biblioteca_facil if vidas == 8 else self.biblioteca_dificil
        self.stack.setCurrentIndex(1)

    def iniciar_modo_solo(self):
        self.palabra_secreta = random.choice(self.biblioteca).upper()
        self.preparar_tablero()

    def validar_palabra_amigo(self):
        palabra = self.input_palabra.text().strip().upper()
        if palabra.isalpha() and len(palabra) > 0:
            self.palabra_secreta = palabra
            self.input_palabra.clear()
            self.preparar_tablero()
        else:
            self.input_palabra.setPlaceholderText("ONLY LETTERS!")
            self.input_palabra.clear()

    def preparar_tablero(self):
        self.vidas_actuales = self.vidas_iniciales
        self.espacios = ["_"] * len(self.palabra_secreta)
        self.actualizar_ui()
        for btn in self.botones_letras.values():
            btn.setEnabled(True)
        self.stack.setCurrentIndex(3)

    def intentar_letra(self, letra):
        self.botones_letras[letra].setEnabled(False)
        if letra in self.palabra_secreta:
            for i, l in enumerate(self.palabra_secreta):
                if l == letra: self.espacios[i] = letra
        else:
            self.vidas_actuales -= 1
        
        self.actualizar_ui()
        if "_" not in self.espacios: self.mostrar_resultado(True)
        elif self.vidas_actuales <= (8 - self.vidas_iniciales): self.mostrar_resultado(False)

    def actualizar_ui(self):
        indice_imagen = self.vidas_actuales
        self.score_lbl.setText(f"LIVES: {self.vidas_actuales}")
        self.word_lbl.setText(" ".join(self.espacios))
        self.canvas.setText(imagenes[max(0, indice_imagen)])

    def mostrar_resultado(self, victoria):
        if victoria:
            self.msg_final.setText("🏆 YOU WIN!")
            self.msg_final.setStyleSheet("color: yellow; border:none;")
            self.canvas_final.setText(trofeo_ascii)
        else:
            self.msg_final.setText("💀 GAME OVER")
            self.msg_final.setStyleSheet("color: red; border:none;")
            self.canvas_final.setText(imagenes[0])
        
        self.revelar_lbl.setText(f"Word was: {self.palabra_secreta}")
        self.stack.setCurrentIndex(4)

    def volver_al_inicio(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VentanaAhorcado()
    w.show()
    sys.exit(app.exec_())