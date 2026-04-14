import random

#Imágenes del ahorcado: 
# #fuente: chrishorton/hangmanwordbank.py

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
        self.palabra_secreta = "" #Variable donde se introduce la palabra del Jugador1.
        self.espacios = [] #Convertimos a lista de espacios.
        self.vidas = 8 #Vidas máximas por partida.
        self.letras_usadas = [] #Letras ya usadas, para no repetir.
        self.biblioteca = ["canguro", "destino", "filigrana", "ametralladora", "sobremesa", "carruaje", "arrebatar", "pescuezo", "columpiar", "bostezar", "mueca", "titubear", "cuchicheo", "monigote", "arañazo", "peluche", "elefante", "escorpion", "ventana", "biblioteca"]

    #Elige jugar solo o con un amigo. Jugador 1 Introduce la palabra secreta.
    def definir_palabra(self):
        print ("¿Cómo quieres jugar? Solo (1) o contra un amigo (2)?")
        eleccion = input ("Elige 1 para jugar solo o 2 para jugar contra un amigo")
        
        if eleccion == "1":
            print (f"Has elegido solo.")
            self.palabra_secreta = random.choice(self.biblioteca)
            self.espacios = ["_"] * len(self.palabra_secreta)
            print("La máquina ha elegido una palabra. ¡Adivínala!")
        else:
            print (f"Has elegido contra un amigo.")
            while True:
                #Como añado que si pone salir vuelva atras ¿?
                entrada_provisional = input("Jugador 1 introduce palabra secreta.").lower().strip()
                if entrada_provisional.isalpha(): #Solo se admiten letras y palabras sin espacios.
                    self.palabra_secreta = entrada_provisional
                    self.espacios = ["_"] * len(self.palabra_secreta) #Para imprimir durante el juego.
                    print ("Palabra guardada. Turno del Jugador 2.")
                    break #return palabra no funcionó
                else: 
                    print ("Palabra no válida. Por favor introduce solo letras sin espacios o símbolos.")
    
    #Jugador2 Introduce letras para acertar.
    def pedir_letra(self): 
        while True:
            letra = input ("Introduce una letra.").lower().strip()
            if len (letra) != 1: #Validación de solo una letra.
                print ("Por favor, introduce una sola letra.")
            elif not letra.isalpha(): #Validación que no sean símbolos o números.
                print ("Por favor, introduce un caracter válido. Solo letras.")
            elif letra in self.letras_usadas: #Validación para evitar letras ya usadas.
                print ("¡Letra ya usada!. Sigue probando.")
            else:
                self.letras_usadas.append(letra) #Añadimos a lista de usadas.
                return letra #Devolvemos el valor de letras para el siguiente apartado.
            
    #El sistema comprueba si la letra existe en la palabra:
    def verificar_letra(self, letra_recibida):
        acierto = False
        for indice, letra in enumerate(self.palabra_secreta):
            if letra == letra_recibida: 
                acierto = True
                self.espacios[indice] = letra_recibida
        if acierto:
            print (f"¡Has acertado! <{letra_recibida}> está en la palabra.")
        else:
            self.vidas -= 1
            print (f"Lo siento. <{letra_recibida}> no está en la palabra.")
            print (f"A tu ahorcado le quedan {self.vidas} vidas.")

    #Máster que controla el resto de métodos y une todo:
    def jugar (self):
        #--------Restart----------:
        self.vidas = 8
        self.letras_usadas = []
        self.espacios = []
        #-------------------------
        
        #Jugador1 o máquina elige la palabra:
        self.definir_palabra()

        #Bucle para el Jugador2:
        while self.vidas > 0 and "_" in self.espacios: #se tienen que cumplir ambas, por eso and y no or.
            print (imagenes[self.vidas]) #Imprime la imagen que corresponde al número de vidas.
            print (" ".join (self.espacios).capitalize())
            print ("Ya has probado: " + ", ".join(self.letras_usadas))

            letra_recibida = self.pedir_letra ()
            self.verificar_letra (letra_recibida)
        if "_" not in self.espacios:
            print (f"¡Enhorabuena, has acertado la palabra era <{self.palabra_secreta.title()}>.")
        else:
            print (imagenes[0])
            print (f"¡GAME OVER! La palabra era <{self.palabra_secreta.title()}>.")
