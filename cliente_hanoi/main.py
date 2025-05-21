# cliente_hanoi/main.py

import tkinter as tk
from interfaz import InterfazHanoi

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazHanoi(root)
    root.mainloop()
