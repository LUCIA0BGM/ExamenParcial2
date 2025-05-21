# cliente_n_reinas/interfaz.py

import tkinter as tk
from juego import NReinasSolver
from ia.ia_client import solicitar_sugerencia

class InterfazNReinas:
    def __init__(self, master, tam_tablero=8):
        self.master = master
        self.master.title("Juego de N R" \
        "einas")
        self.n = tam_tablero
        self.canvas_size = 480
        self.celda = self.canvas_size // self.n

        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        # NUEVO: Selector de tamaño de N
        self.selector_n = tk.Spinbox(master, from_=4, to=16, width=5, command=self.cambiar_tamano)
        self.selector_n.pack(side=tk.LEFT, padx=10)
        self.selector_n.delete(0, tk.END)
        self.selector_n.insert(0, str(self.n))

        self.boton_resolver = tk.Button(master, text="Resolver", command=self.resolver)
        self.boton_resolver.pack(side=tk.LEFT, padx=10)

        self.boton_enviar = tk.Button(master, text="Enviar resultado", command=self.enviar_resultado)
        self.boton_enviar.pack(side=tk.LEFT, padx=10)

        self.boton_ayuda = tk.Button(master, text="Ayuda IA", command=self.enviar_a_ia)
        self.boton_ayuda.pack(side=tk.LEFT, padx=10)

        self.boton_chatbot = tk.Button(master, text="Abrir Chatbot", command=self.abrir_chatbot)
        self.boton_chatbot.pack(side=tk.LEFT, padx=10)

        self.label_info = tk.Label(master, text="")
        self.label_info.pack(side=tk.LEFT, padx=10)

        self.tablero = None
        self.solucion = []
        self.pasos = 0

        self.dibujar_tablero()

    def cambiar_tamano(self):
        try:
            nuevo_n = int(self.selector_n.get())
            if 4 <= nuevo_n <= 16:
                self.n = nuevo_n
                self.celda = self.canvas_size // self.n
                self.solucion = []
                self.pasos = 0
                self.label_info.config(text=f"Tamaño cambiado a N={self.n}")
                self.dibujar_tablero()
        except ValueError:
            self.label_info.config(text="Valor inválido para N.")

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for fila in range(self.n):
            for col in range(self.n):
                x0 = col * self.celda
                y0 = fila * self.celda
                x1 = x0 + self.celda
                y1 = y0 + self.celda
                color = "white" if (fila + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        for fila, col in enumerate(self.solucion):
            x = col * self.celda + self.celda // 2
            y = fila * self.celda + self.celda // 2
            self.canvas.create_text(x, y, text="♛", font=("Arial", 20), fill="red")
    
    def abrir_chatbot(self):
        from ia.chatbot_panel import ChatbotPanel
        ChatbotPanel(self.master)

    def enviar_a_ia(self):
        try:
            estado = {
                "n": self.n,
                "solucion": self.solucion,
                "pasos": self.pasos
            }
            import json
            sugerencia = solicitar_sugerencia("n_reinas", json.dumps(estado))
            self.label_info.config(text="IA: " + sugerencia[:100])  # corta si es muy largo
        except Exception as e:
            self.label_info.config(text=f"Error IA: {e}")

    def resolver(self):
        solver = NReinasSolver(self.n)
        soluciones, pasos = solver.resolver()
        if soluciones:
            self.solucion = soluciones[0]
            self.pasos = pasos
            self.label_info.config(text=f"Resuelto en {pasos} pasos.")
            self.dibujar_tablero()
        else:
            self.label_info.config(text="Sin solución encontrada.")

    def enviar_resultado(self):
        import socket, json
        try:
            mensaje = {
                "juego": "n_reinas",
                "resultado": {
                    "n": self.n,
                    "resuelto": True if self.solucion else False,
                    "pasos": self.pasos
                }
            }

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 5000))
                s.sendall(json.dumps(mensaje).encode())
                respuesta = s.recv(1024).decode()
                self.label_info.config(text=f"Servidor: {respuesta}")
        except Exception as e:
            self.label_info.config(text=f"Error de conexión: {e}")
