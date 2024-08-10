from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

# Diccionario para almacenar las fechas importantes
eventos_importantes = {}

# Función para agregar eventos
def agregar_evento(nombre_evento, fecha):
    if fecha:
        eventos_importantes[nombre_evento] = datetime.strptime(fecha, '%Y-%m-%d')

# Función para actualizar las fechas al próximo año
def actualizar_fechas():
    hoy = datetime.today()
    for evento, fecha in eventos_importantes.items():
        if fecha < hoy:
            while fecha < hoy:
                fecha = fecha.replace(year=fecha.year + 1)
            eventos_importantes[evento] = fecha

# Función para verificar eventos que vencen pronto
def verificar_proximos_eventos(dias_anticipacion=5):
    hoy = datetime.today()
    actualizar_fechas()
    proximos_eventos = []
    for evento, fecha in eventos_importantes.items():
        if hoy <= fecha <= hoy + timedelta(days=dias_anticipacion):
            proximos_eventos.append((evento, fecha.strftime('%Y-%m-%d')))
    
    if proximos_eventos:
        return proximos_eventos
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar_fechas', methods=['POST'])
def procesar_fechas():
    agregar_evento('examen_medico', request.form.get('examen_medico'))
    agregar_evento('fotocheck', request.form.get('fotocheck'))
    agregar_evento('cumpleaños', request.form.get('cumpleaños'))
    agregar_evento('revision_tecnica', request.form.get('revision_tecnica'))
    agregar_evento('soat', request.form.get('soat'))
    agregar_evento('seguro_contra_dano_terceros', request.form.get('seguro_contra_dano_terceros'))
    
    proximos_eventos = verificar_proximos_eventos()
    
    if proximos_eventos:
        return f"Los siguientes eventos vencen pronto: {proximos_eventos}"
    else:
        return "No hay eventos que venzan en los próximos 5 días."

if __name__ == '__main__':
    app.run(debug=True)
