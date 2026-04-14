import tkinter as tk
import random

# Variables de puntos
puntos_objetivos = 3
puntos_jugador = 0
puntos_ordenador = 0
opciones = ["piedra", "papel", "tijera"]

# Crear ventana
ventana = tk.Tk()
ventana.title("Piedra, Papel o Tijera")

# Etiquetas para mostrar puntaje y resultado
etiqueta_resultado = tk.Label(ventana, text="¡Elige tu jugada!", font=("Arial", 14))
etiqueta_resultado.pack(pady=10)

etiqueta_puntaje = tk.Label(ventana, text=f"Jugador: {puntos_jugador} - Computadora: {puntos_ordenador}", font=("Arial", 12))
etiqueta_puntaje.pack(pady=5)

# Función principal del juego
def jugar(jugador_1):
    global puntos_jugador, puntos_ordenador
    
    computadora = random.choice(opciones)
    resultado = f"Computadora eligió {computadora}\n"
    
    if jugador_1 == computadora:
        resultado += "¡Empate!"
    elif (jugador_1 == "piedra" and computadora == "tijera") or \
         (jugador_1 == "papel" and computadora == "piedra") or \
         (jugador_1 == "tijera" and computadora == "papel"):
        resultado += "¡Ganaste!"
        puntos_jugador += 1
    else:
        resultado += "Perdiste"
        puntos_ordenador += 1
    
    etiqueta_resultado.config(text=resultado)
    etiqueta_puntaje.config(text=f"Jugador: {puntos_jugador} - Computadora: {puntos_ordenador}")
    
    if puntos_jugador == puntos_objetivos:
        etiqueta_resultado.config(text="¡Ganaste el juego!")
        desactivar_botones()
    elif puntos_ordenador == puntos_objetivos:
        etiqueta_resultado.config(text="La computadora ganó el juego")
        desactivar_botones()

# Desactivar botones al terminar
def desactivar_botones():
    boton_piedra.config(state="disabled")
    boton_papel.config(state="disabled")
    boton_tijera.config(state="disabled")

# Botones de juego
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

boton_piedra = tk.Button(frame_botones, text="Piedra", width=10, command=lambda: jugar("piedra"))
boton_papel = tk.Button(frame_botones, text="Papel", width=10, command=lambda: jugar("papel"))
boton_tijera = tk.Button(frame_botones, text="Tijera", width=10, command=lambda: jugar("tijera"))

boton_piedra.grid(row=0, column=0, padx=5)
boton_papel.grid(row=0, column=1, padx=5)
boton_tijera.grid(row=0, column=2, padx=5)

ventana.mainloop()