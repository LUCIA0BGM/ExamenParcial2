# cliente_caballo/main.py

import tkinter as tk
from cliente_caballo.interfaz import InterfazCaballo

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCaballo(root)
    root.mainloop()
