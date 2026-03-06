from flask import Flask, request, render_template_string, jsonify, redirect, session, url_for
import json
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_prueba')

ADMIN_USER = os.environ.get('ADMIN_USER', 'ADMIN')
ADMIN_PASS = os.environ.get('ADMIN_PASS', '1234')

DATA_FILE = "entradas.json"

def cargar_entradas():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_entradas(entradas):
    with open(DATA_FILE, "w") as f:
        json.dump(entradas, f)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('logueado'):
        return redirect(url_for("panel"))
    
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        
        if usuario == ADMIN_USER and contraseña == ADMIN_PASS:
            session['logueado'] = True
            return redirect(url_for("panel"))
        else:
            return "Usuario o contraseña no validos"
        
    login_html = """
    <h2>Acceso administrador</h2>
    <form method="Post">
        Usuario: <input type="text" name="usuario"><br><br>
        Contraseña: <input type="password" name="contraseña"><br><br>
        <input type="submit" value="Entrar">
    </form>
    """
    return render_template_string(login_html)

@app.route("/logout")
def logout():
    session.pop('logueado', None)
    return redirect(url_for('login'))

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

        return render_template_string(confirmacion_html, 
                                    numero=numero, 
                                    nombre=nombre, 
                                    apellido=apellido)

    return render_template_string(formulario_html)

@app.route("/panel")
@login_required
def panel():
    entradas = cargar_entradas()
    return render_template_string(panel_html, entradas=entradas)

@app.route("/api/entradas")
@login_required
def api_entradas():
    return jsonify(cargar_entradas())

# ============================================
# HTML PROFESIONAL (todo en variables)
# ============================================

formulario_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro de Entradas</title>
    <!-- Bootstrap 5 para diseño responsive -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome para iconos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .card {
            border: none;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            animation: slideUp 0.5s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px 20px 0 0 !important;
            padding: 2rem;
            border: none;
            text-align: center;
        }
        
        .card-header h2 {
            margin: 0;
            font-weight: 600;
            font-size: 2rem;
        }
        
        .card-header i {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .card-body {
            padding: 2.5rem;
        }
        
        .form-label {
            font-weight: 600;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .form-control {
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            font-size: 1rem;
            transition: all 0.3s;
        }
        
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            outline: none;
        }
        
        .btn-registrar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1rem;
            font-size: 1.2rem;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            margin-top: 1rem;
        }
        
        .btn-registrar:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-registrar i {
            margin-right: 0.5rem;
        }
        
        .footer-links {
            text-align: center;
            margin-top: 2rem;
        }
        
        .footer-links a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            margin: 0 1rem;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: #764ba2;
        }
        
        /* Responsive para móviles */
        @media (max-width: 768px) {
            .card-body {
                padding: 1.5rem;
            }
            
            .card-header h2 {
                font-size: 1.5rem;
            }
            
            .card-header i {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6 col-xl-5">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-ticket-alt"></i>
                        <h2>Registro de Entrada</h2>
                    </div>
                    
                    <div class="card-body">
                        <form method="POST" action="/">
                            <div class="mb-4">
                                <label for="nombre" class="form-label">
                                    <i class="fas fa-user me-2"></i>Nombre
                                </label>
                                <input type="text" class="form-control" 
                                       id="nombre" name="nombre" 
                                       placeholder="Ej: Juan Carlos"
                                       required>
                            </div>
                            
                            <div class="mb-4">
                                <label for="apellido" class="form-label">
                                    <i class="fas fa-user-tag me-2"></i>Apellido
                                </label>
                                <input type="text" class="form-control" 
                                       id="apellido" name="apellido" 
                                       placeholder="Ej: García Pérez"
                                       required>
                            </div>
                            
                            <button type="submit" class="btn-registrar">
                                <i class="fas fa-check-circle"></i>
                                Obtener mi entrada
                            </button>
                        </form>
                        
                        <div class="footer-links">
                            <a href="/panel">
                                <i class="fas fa-chart-bar me-1"></i>Ver panel
                            </a>
                            <a href="/api/entradas">
                                <i class="fas fa-code me-1"></i>API
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

confirmacion_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>¡Registro Exitoso!</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .card {
            border: none;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            background: rgba(255, 255, 255, 0.95);
            animation: scaleIn 0.5s ease;
        }
        
        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .success-header {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            border-radius: 20px 20px 0 0 !important;
            padding: 2rem;
            text-align: center;
        }
        
        .success-header i {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .success-header h2 {
            margin: 0;
            font-weight: 600;
        }
        
        .card-body {
            padding: 2.5rem;
            text-align: center;
        }
        
        .entry-number {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 3rem;
            font-weight: 700;
            padding: 1rem 2rem;
            border-radius: 50px;
            display: inline-block;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .entry-details {
            background: #f7fafc;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 2rem 0;
        }
        
        .entry-details p {
            margin: 0.5rem 0;
            font-size: 1.2rem;
        }
        
        .btn-volver {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .btn-volver:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="card">
                    <div class="success-header">
                        <i class="fas fa-check-circle"></i>
                        <h2>¡Registro Exitoso!</h2>
                    </div>
                    
                    <div class="card-body">
                        <div class="entry-number">
                            #{{ numero }}
                        </div>
                        
                        <div class="entry-details">
                            <p><strong><i class="fas fa-user me-2"></i>Nombre:</strong> {{ nombre }}</p>
                            <p><strong><i class="fas fa-user-tag me-2"></i>Apellido:</strong> {{ apellido }}</p>
                        </div>
                        
                        <p class="text-muted mb-4">
                            <i class="fas fa-info-circle me-2"></i>
                            Guarda tu número de entrada
                        </p>
                        
                        <a href="/" class="btn-volver">
                            <i class="fas fa-home me-2"></i>Volver al inicio
                        </a>
                        
                        <div class="mt-4">
                            <a href="/panel" class="text-decoration-none me-3">
                                <i class="fas fa-chart-bar me-1"></i>Ver panel
                            </a>
                            <a href="/api/entradas" class="text-decoration-none">
                                <i class="fas fa-code me-1"></i>API
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

panel_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Control</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .container {
            max-width: 1000px;
        }
        
        .header-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            animation: slideDown 0.5s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header-card h1 {
            color: #333;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .stats-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .stats-card i {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .stats-card h3 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .stats-card p {
            margin: 0;
            opacity: 0.9;
        }
        
        .table-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            animation: slideUp 0.5s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .table {
            margin-bottom: 0;
        }
        
        .table thead th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem;
            font-weight: 600;
        }
        
        .table tbody tr {
            transition: background 0.3s;
        }
        
        .table tbody tr:hover {
            background: #f8f9fa;
        }
        
        .table td {
            padding: 1rem;
            vertical-align: middle;
        }
        
        .badge-entry {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: 600;
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: #666;
        }
        
        .empty-state i {
            font-size: 4rem;
            color: #ddd;
            margin-bottom: 1rem;
        }
        
        .nav-links {
            text-align: center;
            margin-top: 2rem;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            margin: 0 1rem;
            font-size: 1.1rem;
            transition: opacity 0.3s;
        }
        
        .nav-links a:hover {
            opacity: 0.8;
            color: white;
        }
        
        @media (max-width: 768px) {
            .stats-card {
                margin-bottom: 1rem;
            }
            
            .table {
                font-size: 0.9rem;
            }
            
            .table td, .table th {
                padding: 0.75rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-card">
            <h1 class="text-center">
                <i class="fas fa-chart-line me-3"></i>Panel de Control
            </h1>
            
            <div class="row">
                <div class="col-md-6 mx-auto">
                    <div class="stats-card">
                        <i class="fas fa-users"></i>
                        <h3>{{ entradas|length }}</h3>
                        <p>Entradas Registradas</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="table-card">
            <h3 class="mb-4">
                <i class="fas fa-list me-2"></i>Lista de Entradas
            </h3>
            
            {% if entradas %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Número</th>
                            <th>Nombre</th>
                            <th>Apellido</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for entrada in entradas %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td>
                                <span class="badge-entry">
                                    <i class="fas fa-ticket-alt me-1"></i>{{ entrada.numero }}
                                </span>
                            </td>
                            <td>{{ entrada.nombre }}</td>
                            <td>{{ entrada.apellido }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h4>No hay entradas registradas</h4>
                <p class="text-muted">Las entradas aparecerán aquí cuando alguien se registre</p>
            </div>
            {% endif %}
            
            <div class="nav-links">
                <a href="/">
                    <i class="fas fa-home me-1"></i>Registro
                </a>
                <a href="/api/entradas">
                    <i class="fas fa-code me-1"></i>API
                </a>
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
