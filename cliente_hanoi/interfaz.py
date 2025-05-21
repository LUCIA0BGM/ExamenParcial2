# cliente_hanoi/interfaz.py

import tkinter as tk
from juego import HanoiSolver
import time

class InterfazHanoi:
    def __init__(self, master, discos=4):
        self.master = master
        self.master.title("Torres de Hanói")
        self.num_discos = discos
        self.canvas = tk.Canvas(master, width=480, height=300)
        self.canvas.pack()

        self.boton_resolver = tk.Button(master, text="Resolver", command=self.resolver)
        self.boton_resolver.pack(side=tk.LEFT, padx=5)

        self.boton_enviar = tk.Button(master, text="Enviar resultado", command=self.enviar_resultado)
        self.boton_enviar.pack(side=tk.LEFT, padx=5)

        self.label_info = tk.Label(master, text="")
        self.label_info.pack(side=tk.LEFT)

        self.torres = {'A': [], 'B': [], 'C': []}
        self.movimientos = []
        self._inicializar_torres()
        self.dibujar()

    def _inicializar_torres(self):
        self.torres = {'A': list(reversed(range(1, self.num_discos + 1))), 'B': [], 'C': []}

    def dibujar(self):
        self.canvas.delete("all")
        ancho_canvas = 480
        altura = 200
        base_y = 250
        poste_x = [80, 240, 400]
        colores = ["red", "green", "blue", "orange", "purple", "cyan", "yellow"]

        for i, torre in enumerate(['A', 'B', 'C']):
            self.canvas.create_rectangle(poste_x[i] - 5, 100, poste_x[i] + 5, base_y, fill="black")
            discos = self.torres[torre]
            for j, disco in enumerate(discos):
                ancho = disco * 15
                x0 = poste_x[i] - ancho
                x1 = poste_x[i] + ancho
                y1 = base_y - j * 20
                y0 = y1 - 20
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colores[disco % len(colores)])

    def resolver(self):
        solver = HanoiSolver(self.num_discos)
        self.movimientos = solver.resolver()
        self._inicializar_torres()
        self.dibujar()
        self.master.after(500, self._animar, 0)

    def _animar(self, i):
        if i < len(self.movimientos):
            origen, destino = self.movimientos[i]
            disco = self.torres[origen].pop()
            self.torres[destino].append(disco)
            self.dibujar()
            self.master.after(300, self._animar, i + 1)
        else:
            self.label_info.config(text=f"Resuelto con {len(self.movimientos)} movimientos.")

    def enviar_resultado(self):
        import socket, json
        try:
            mensaje = {
                "juego": "hanoi",
                "resultado": {
                    "discos": self.num_discos,
                    "movimientos": len(self.movimientos),
                    "resuelto": True
                }
            }
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 5000))
                s.sendall(json.dumps(mensaje).encode())
                respuesta = s.recv(1024).decode()
                self.label_info.config(text=f"Servidor: {respuesta}")
        except Exception as e:
            self.label_info.config(text=f"Error conexión: {e}")
