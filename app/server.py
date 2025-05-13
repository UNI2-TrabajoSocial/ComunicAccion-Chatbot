# app/server.py

import os
from flask import request, redirect, url_for, current_app, render_template
from app import app, db
from app.models import Respuesta
import app.sett as sett
import app.services as services
from collections import Counter

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return "Hola! Soy ComunicAcción, tu chatbot ciudadano! ¿En qué te puedo ayudar?😊"

@app.route('/webhook', methods=['GET'])
def verify():
    token     = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == sett.VERIFY_TOKEN and challenge:
        return challenge, 200
    return "Token inválido", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    try:
        value    = data["entry"][0]["changes"][0]["value"]
        messages = value.get("messages", [])
        if not messages:
            return "no messages", 200

        msg       = messages[0]
        sender    = msg["from"]
        msg_id    = msg["id"]
        name      = value["contacts"][0]["profile"].get("name", "")
        text      = services.parse_text(msg).strip()

        services.administrar_chatbot(text, sender, msg_id, name)

        return "OK", 200

    except KeyError as e:
        current_app.logger.error(f"KeyError en webhook: {e}")
        return "Bad request", 400
    except Exception as e:
        current_app.logger.error(f"Error en webhook: {e}")
        return "Error interno", 500

@app.route('/dashboard')
def dashboard():
    respuestas = Respuesta.query.order_by(Respuesta.id.desc()).all()
    tipo_counts      = Counter(r.tipo_pregunta or "otro"  for r in respuestas)
    respuesta_counts = Counter(r.respuesta     or "vacío" for r in respuestas)

    chart_data = {
        "labels": list(tipo_counts.keys()),
        "counts": list(tipo_counts.values())
    }
    bar_data = {
        "labels": list(respuesta_counts.keys())[:10],
        "counts": list(respuesta_counts.values())[:10]
    }

    return render_template(
        "dashboard.html",
        respuestas=respuestas,
        chart_data=chart_data,
        bar_data=bar_data
    )
    
#Borra BD
@app.route('/reset-db')
def reset_db():
    db.session.query(Respuesta).delete()
    db.session.commit()
    return "Base de datos reseteada correctamente."
  
  #pegar este enlace: https://chip-sable-balloon.glitch.me/reset-db

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
