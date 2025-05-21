# test_cliente.py
import socket
import json

HOST = 'localhost'
PORT = 5000

mensaje = {
    "juego": "n_reinas",
    "resultado": {
        "n": 8,
        "resuelto": True,
        "pasos": 22
    }
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json.dumps(mensaje).encode())
    respuesta = s.recv(1024)
    print(respuesta.decode())
