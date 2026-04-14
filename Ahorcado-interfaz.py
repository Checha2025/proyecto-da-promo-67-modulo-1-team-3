import random
import customtkinter as ctk

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
      
      
      
      
      
      
========='''  ]


class JuegoAhorcado: 
    def __init__(self):
        self.palabra_secreta = ""
        self.espacios = []
        self.vidas = 8
        self.letras_usadas = []
        self.biblioteca = ["canguro", "destino", "filigrana", "ametralladora", "sobremesa", "carruaje", "arrebatar", "pescuezo", "columpiar", "bostezar", "mueca", "titubear", "cuchicheo", "monigote", "arañazo", "peluche", "elefante", "escorpion", "ventana", "biblioteca"]

    def iniciar_juego_maquina(self):
        self.vidas = 8
        self.letras_usadas = []
        self.palabra_secreta = random.choice(self.biblioteca)
        self.espacios = ["_"] * len(self.palabra_secreta)
        return self.espacios

    def verificar_letra(self, letra_recibida):
        acierto = False
        if letra_recibida in self.letras_usadas:
            return "usada"
        
        self.letras_usadas.append(letra_recibida)
        
        for indice, letra in enumerate(self.palabra_secreta):
            if letra == letra_recibida: 
                acierto = True
                self.espacios[indice] = letra_recibida
        
        if not acierto:
            self.vidas -= 1
        
        return acierto

# --- LA INTERFAZ CON CUSTOMTKINTER ---
class AppAhorcado(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.juego = JuegoAhorcado()
        
        self.title("Ahorcado 💀🪵")
        self.geometry("950x650") # Un poco más grande para que quepan bien los botones con borde
        ctk.set_appearance_mode("dark")
        
        # --- Configuración de Estilo Madera Pro ---
        self.madera_fg = "#8B4513"       # Marrón base
        self.madera_hover = "#A0522D"    # Hover más claro
        self.madera_border = "#5D2906"   # Borde oscuro para profundidad
        self.text_color_madera = "#F5DEB3" # Color trigo/crema
        self.corner_radius_madera = 5    # Esquinas redondeadas
        self.border_width_madera = 3      # Ancho del borde
        
        # =========================================================
        # 1. PANTALLA DE MENÚ
        # =========================================================
        self.frame_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_menu.pack(expand=True)

        ctk.CTkLabel(self.frame_menu, text="AHORCADO 💀", font=("Arial", 45, "bold"), text_color=self.text_color_madera).pack(pady=20)
        ctk.CTkLabel(self.frame_menu, text="¿Cómo quieres jugar?", font=("Arial", 20)).pack(pady=10)
        
        # Botones del Menú con el ESTILO MADERA COMPLETO
        ctk.CTkButton(self.frame_menu, text="Solo (Máquina)", 
                      command=self.iniciar_modo_maquina, width=280, height=50, font=("Arial", 16, "bold"),
                      fg_color=self.madera_fg, hover_color=self.madera_hover,
                      border_color=self.madera_border, border_width=self.border_width_madera,
                      corner_radius=self.corner_radius_madera, text_color=self.text_color_madera).pack(pady=15)
                      
        ctk.CTkButton(self.frame_menu, text="Contra un amigo", 
                      command=self.iniciar_modo_amigo, width=280, height=50, font=("Arial", 16, "bold"),
                      fg_color=self.madera_fg, hover_color=self.madera_hover,
                      border_color=self.madera_border, border_width=self.border_width_madera,
                      corner_radius=self.corner_radius_madera, text_color=self.text_color_madera).pack(pady=15)

        # =========================================================
        # 2. PANTALLA DE JUEGO
        # =========================================================
        self.frame_juego = ctk.CTkFrame(self, fg_color="transparent")
        
        self.label_vidas = ctk.CTkLabel(self.frame_juego, text="Vidas restantes: 8", font=("Arial", 22, "bold"), text_color="red")
        self.label_vidas.pack(pady=15)

        self.label_dibujo = ctk.CTkLabel(self.frame_juego, text=imagenes[8], font=("Courier", 22))
        self.label_dibujo.pack(pady=15)
        
        self.label_palabra = ctk.CTkLabel(self.frame_juego, text="", font=("Arial", 40, "bold"), text_color=self.text_color_madera)
        self.label_palabra.pack(pady=25)

        self.frame_teclado = ctk.CTkFrame(self.frame_juego, fg_color="transparent")
        self.frame_teclado.pack(pady=25)
        self.diccionario_botones = {}
        self.crear_teclado()

    def mostrar_juego(self):
        self.frame_menu.pack_forget()
        self.frame_juego.pack(expand=True, fill="both")

    def mostrar_menu(self):
        self.frame_juego.pack_forget()
        self.frame_menu.pack(expand=True)

    def iniciar_modo_maquina(self):
        self.resetear_teclado()
        self.juego.iniciar_juego_maquina()
        self.mostrar_juego()
        self.actualizar_pantalla()

    def iniciar_modo_amigo(self):
        palabra = ctk.CTkInputDialog(text="Jugador 1: Introduce la palabra secreta:", title="Modo Amigo").get_input()
        if palabra and palabra.isalpha():
            self.resetear_teclado()
            self.juego.palabra_secreta = palabra.lower()
            self.juego.espacios = ["_"] * len(palabra)
            self.juego.vidas = 8
            self.juego.letras_usadas = []
            self.mostrar_juego()
            self.actualizar_pantalla()

    def crear_teclado(self):
        filas_qwerty = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
        for fila in filas_qwerty:
            frame_fila = ctk.CTkFrame(self.frame_teclado, fg_color="transparent")
            frame_fila.pack()
            for letra in fila:
                minuscula = letra.lower()
                # Botones del Teclado con el ESTILO MADERA COMPLETO
                btn = ctk.CTkButton(frame_fila, text=letra, width=50, height=50, font=("Courier", 18, "bold"),
                                   fg_color=self.madera_fg, hover_color=self.madera_hover,
                                   border_color=self.madera_border, border_width=self.border_width_madera,
                                   corner_radius=self.corner_radius_madera, text_color=self.text_color_madera,
                                   command=lambda l=minuscula: self.presionar_letra(l))
                btn.pack(side="left", padx=4, pady=4)
                self.diccionario_botones[minuscula] = btn
    
    def resetear_teclado(self):
        # Al resetear, volvemos a poner el color de madera base fg_color=self.madera_fg
        for btn in self.diccionario_botones.values():
            btn.configure(state="normal", fg_color=self.madera_fg, text_color=self.text_color_madera)
            
    def presionar_letra(self, letra):
        self.juego.verificar_letra(letra)
        boton = self.diccionario_botones[letra]
        # Al desactivar, lo ponemos gris oscuro, pero mantenemos el borde para que no pierda la forma
        boton.configure(state="disabled", fg_color="#2B2B2B", text_color="#555555") 

        self.actualizar_pantalla()
        
        if "_" not in self.juego.espacios:
            self.final_juego("¡ENHORABUENA! HAS GANADO")
        elif self.juego.vidas <= 0:
            self.final_juego(f"GAME OVER\nLa palabra era: {self.juego.palabra_secreta.upper()}")

    def actualizar_pantalla(self):
        self.label_palabra.configure(text=" ".join(self.juego.espacios).upper())
        self.label_dibujo.configure(text=imagenes[self.juego.vidas])
        self.label_vidas.configure(text=f"Vidas restantes: {self.juego.vidas}")

    def final_juego(self, mensaje):
        for widget in self.frame_teclado.winfo_children():
            widget.destroy()

        color_final = "red" if "GAME OVER" in mensaje.upper() else "white"


        ctk.CTkLabel(
            self.frame_teclado, 
            text=mensaje, 
            font=("Arial", 25, "bold"), 
            text_color=color_final  # <--- Aquí ocurre la magia
        ).pack(pady=25)

        # Botón final también con el ESTILO MADERA COMPLETO
        ctk.CTkButton(self.frame_teclado, text="Volver al Menú", 
                     width=220, height=45, font=("Arial", 15, "bold"),
                     fg_color=self.madera_fg, hover_color=self.madera_hover,
                     border_color=self.madera_border, border_width=self.border_width_madera,
                     corner_radius=self.corner_radius_madera, text_color=self.text_color_madera,
                     command=self.volver_al_inicio).pack(pady=15)

    def volver_al_inicio(self):
        for widget in self.frame_teclado.winfo_children():
            widget.destroy()
        self.crear_teclado()
        self.mostrar_menu()

        
if __name__ == "__main__":
    app = AppAhorcado()
    app.mainloop()