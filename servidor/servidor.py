# servidor/servidor.py
import socket
import threading
import json
from modelos import inicializar_bd, Session, ResultadoNReinas, ResultadoCaballo, ResultadoHanoi

HOST = 'localhost'
PORT = 5000

def manejar_cliente(conn, addr):
    print(f"[+] Conexión establecida desde {addr}")
    session = Session()

    try:
        datos = conn.recv(4096).decode()
        mensaje = json.loads(datos)
        juego = mensaje.get("juego")
        resultado = mensaje.get("resultado")

        if juego == "n_reinas":
            entrada = ResultadoNReinas(
                n=resultado["n"],
                resuelto=resultado["resuelto"],
                pasos=resultado["pasos"]
            )
            session.add(entrada)

        elif juego == "caballo":
            entrada = ResultadoCaballo(
                posicion_inicial=resultado["posicion_inicial"],
                movimientos=resultado["movimientos"],
                completado=resultado["completado"]
            )
            session.add(entrada)

        elif juego == "hanoi":
            entrada = ResultadoHanoi(
                discos=resultado["discos"],
                movimientos=resultado["movimientos"],
                resuelto=resultado["resuelto"]
            )
            session.add(entrada)

        else:
            print(f"[!] Juego desconocido: {juego}")
            conn.sendall(b"ERROR: Juego no reconocido")
            return

        session.commit()
        conn.sendall(b"OK: Resultado guardado")
        print(f"[✓] Resultado de {juego} guardado para {addr}")

    except Exception as e:
        print(f"[!] Error procesando datos de {addr}: {e}")
        conn.sendall(b"ERROR: Fallo en el servidor")
    finally:
        session.close()
        conn.close()

def iniciar_servidor():
    inicializar_bd()
    print("[*] Base de datos inicializada")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
