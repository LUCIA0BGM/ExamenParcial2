# cliente_caballo/interfaz.py

import tkinter as tk
from cliente_caballo.juego import CaballoSolver

class InterfazCaballo:
    def __init__(self, master, tam=8):
        self.master = master
        self.master.title("Recorrido del Caballo")
        self.n = tam
        self.canvas_size = 480
        self.celda = self.canvas_size // self.n

        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.label_inicio = tk.Label(master, text="Inicio (fila,col):")
        self.label_inicio.pack(side=tk.LEFT)

        self.entrada = tk.Entry(master, width=5)
        self.entrada.insert(0, "0,0")
        self.entrada.pack(side=tk.LEFT)

        self.boton_resolver = tk.Button(master, text="Resolver", command=self.resolver)
        self.boton_resolver.pack(side=tk.LEFT, padx=5)

        self.boton_enviar = tk.Button(master, text="Enviar resultado", command=self.enviar_resultado)
        self.boton_enviar.pack(side=tk.LEFT, padx=5)

        self.label_info = tk.Label(master, text="")
        self.label_info.pack(side=tk.LEFT, padx=10)

        self.movimientos = []
        self.dibujar_tablero()

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

        for i, (x, y) in enumerate(self.movimientos):
            cx = y * self.celda + self.celda // 2
            cy = x * self.celda + self.celda // 2
            self.canvas.create_text(cx, cy, text=str(i+1), font=("Arial", 10), fill="blue")

    def resolver(self):
        try:
            entrada = self.entrada.get()
            fila, col = map(int, entrada.split(","))
            solver = CaballoSolver(self.n)
            self.movimientos = solver.resolver(fila, col)
            if self.movimientos:
                self.label_info.config(text=f"Recorrido completo.")
            else:
                self.label_info.config(text="No se encontró recorrido.")
            self.dibujar_tablero()
        except Exception as e:
            self.label_info.config(text=f"Error: {e}")

    def enviar_resultado(self):
        import socket, json
        try:
            mensaje = {
                "juego": "caballo",
                "resultado": {
                    "posicion_inicial": self.entrada.get(),
                    "movimientos": len(self.movimientos),
                    "completado": len(self.movimientos) == self.n * self.n
                }
            }
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 5000))
                s.sendall(json.dumps(mensaje).encode())
                respuesta = s.recv(1024).decode()
                self.label_info.config(text=f"Servidor: {respuesta}")
        except Exception as e:
            self.label_info.config(text=f"Error conexión: {e}")
