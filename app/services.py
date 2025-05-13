# app/services.py

import json, time, random, requests
import app.sett as sett
from app import db
from app.models import Respuesta

# guarda el estado intermedio por usuario
services_state = {}

def send_whatsapp(payload):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sett.WHATSAPP_TOKEN}"
    }
    r = requests.post(sett.WHATSAPP_URL, headers=headers, json=payload)
    if r.status_code != 200:
        print("❌ Error enviando mensaje:", r.status_code, r.text)

def send_text(to, body):
    send_whatsapp({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body}
    })

def send_reaction(to, message_id, emoji):
    send_whatsapp({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "reaction",
        "reaction": {"message_id": message_id, "emoji": emoji}
    })

def send_button(to, options, body, footer):
    buttons = [
        {"type": "reply", "reply": {"id": f"opt_{i+1}", "title": t}}
        for i, t in enumerate(options)
    ]
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body},
            "footer": {"text": footer},
            "action": {"buttons": buttons}
        }
    }

def send_list(to, options, body, footer):
    rows = [
        {"id": f"row_{i+1}", "title": t, "description": ""}
        for i, t in enumerate(options)
    ]
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body},
            "footer": {"text": footer},
            "action": {"button": "Ver Opciones", "sections": [{"title":"Selecciona una opción.","rows":rows}]}
        }
    }

def parse_text(message):
    t = message.get("type")
    if t == "text":
        return message["text"]["body"]
    if t == "button":
        return message["button"]["text"]
    if t == "interactive":
        inter = message["interactive"]
        if inter["type"] == "list_reply":
            return inter["list_reply"]["title"]
        if inter["type"] == "button_reply":
            return inter["button_reply"]["title"]
    return ""

def administrar_chatbot(text, number, message_id, name):
    text = text.lower().strip()
    time.sleep(1)

    # 1) saludo
    if text == "hola":
        emojis = ["😊","🙌","🫡","👋"]
        send_reaction(number, message_id, random.choice(emojis))
        body   = "Hola! Soy ComunicAcción, tu chatbot ciudadano! ¿En qué te puedo ayudar?😊"
        opts   = ["Encuestas", "Consultas", "Informaciones"]
        send_whatsapp(send_button(number, opts, body, "ComunicAcción"))
        return

    # 2) primer menú
    if text in ["encuestas","consultas","informaciones"]:
        if text != "encuestas":
            send_text(number, f"Has elegido *{text.capitalize()}*. ¿En qué más puedo ayudarte?")
            return
        # submenú encuestas
        tipos = ["Seguridad","Transporte","Comunidad","Otro"]
        send_whatsapp(send_list(number, tipos, "Seleccione el tipo de encuesta", "ComunicAcción"))
        return

    # 3) tipo de encuesta
    tipos_enc = ["seguridad","transporte","comunidad","otro"]
    if text in tipos_enc:
        preguntas = {
            "seguridad":  "¿Qué tan satisfechos están con la seguridad en su barrio?",
            "transporte": "¿Cuáles son las principales preocupaciones de los vecinos respecto al transporte público?",
            "comunidad":  "¿Qué tipo de actividades comunitarias prefieren los vecinos?",
            "otro":       "¿Cuál es tu principal sugerencia o comentario?"
        }
        send_text(number, f"Encuesta ({text.capitalize()}): {preguntas[text]}")
        services_state[number] = text
        return

    # 4) respuesta libre → guardar
    if number in services_state:
        tipo = services_state.pop(number)
        r = Respuesta(tipo_pregunta=tipo, respuesta=text)
        db.session.add(r)
        db.session.commit()
        send_text(number, "¡Gracias! Tu respuesta ha sido registrada.")
        return

    # 5) fallback
    send_text(number, "Por favor escribe “Hola” para comenzar.")
