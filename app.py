from flask import Flask, request, render_template_string, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "entradas.json"

def cargar_entradas():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_entradas(entradas):
    with open(DATA_FILE, "w") as f:
        json.dump(entradas, f)

@app.route("/", methods=["GET", "POST"])
def registrarte():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")

        if not nombre or not apellido:
            return "Faltan datos", 400

        entradas = cargar_entradas()
        numero = f"{len(entradas) + 1:03}"

        nuevas_entradas = {
            "numero": numero,
            "nombre": nombre,
            "apellido": apellido
        }

        entradas.append(nuevas_entradas)
        guardar_entradas(entradas)

        return f"Entrada {numero} registrada para {nombre} {apellido}"

    formulario_html = """
    <h2>Registro de entrada</h2>
    <form method="post">
        Nombre: <input type="text" name="nombre"><br><br>
        Apellido: <input type="text" name="apellido"><br><br>
        <input type="submit" value="Registrarse">
    </form>
    """
    return render_template_string(formulario_html)

@app.route("/panel")
def panel():
    entradas = cargar_entradas()

    html = "<h2>Entradas registradas</h2><ul>"

    for e in entradas:
        html += f"<li>{e['numero']} - {e['nombre']} - {e['apellido']}</li>"

    html += "</ul>"
    return html

@app.route("/api/entradas")
def api_entradas():
    return jsonify(cargar_entradas())

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
