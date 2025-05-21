# ia/chatbot_panel.py

import tkinter as tk
from tkinter import scrolledtext
from ia_client import consultar_chatbot

class ChatbotPanel(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Chatbot IA")
        self.geometry("500x350")
        self.create_widgets()

    def create_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(self, width=60, height=15, state='disabled')
        self.chat_area.pack(pady=10)

        self.input_field = tk.Entry(self, width=40)
        self.input_field.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(self, text="Enviar", command=self.enviar_pregunta)
        self.send_button.pack(side=tk.LEFT)

    def enviar_pregunta(self):
        pregunta = self.input_field.get()
        if pregunta:
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, "Tú: " + pregunta + "\n")
            respuesta = consultar_chatbot(pregunta)
            self.chat_area.insert(tk.END, "IA: " + respuesta + "\n")
            self.chat_area.config(state='disabled')
            self.input_field.delete(0, tk.END)
