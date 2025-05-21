# ia/ia_client.py

import requests
import json

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
API_KEY = "TU_API_KEY_AQUI"  # ← Pega aquí tu API KEY

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def solicitar_sugerencia(juego, estado_json):
    mensaje = f"Dame una sugerencia para el juego {juego} con el estado: {estado_json}"
    payload = {"inputs": mensaje}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and 'generated_text' in data[0]:
            return data[0]['generated_text']
        elif isinstance(data, dict) and 'generated_text' in data:
            return data['generated_text']
        else:
            return "No se pudo interpretar la respuesta."
    except Exception as e:
        return f"Error al conectar con la IA: {e}"

def consultar_chatbot(pregunta):
    payload = {"inputs": pregunta}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and 'generated_text' in data[0]:
            return data[0]['generated_text']
        elif isinstance(data, dict) and 'generated_text' in data:
            return data['generated_text']
        else:
            return "No se pudo interpretar la respuesta."
    except Exception as e:
        return f"Error al conectar con la IA: {e}"
