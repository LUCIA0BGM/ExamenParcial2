# cliente_n_reinas/main.py

import tkinter as tk
from interfaz import InterfazNReinas

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazNReinas(root, tam_tablero=8)
    root.mainloop()
