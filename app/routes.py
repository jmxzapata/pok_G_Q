# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from .forms import RegistrationForm, LoginStep1Form, LoginStep2Form
from .gq_protocol import (
    hash_password,
    compute_public_key,
    compute_proof,
    verify_proof,
    N,
    G
)
import os
import json

main = Blueprint('main', __name__)

# Ruta al archivo JSON que almacena los usuarios
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    """Carga los usuarios desde el archivo JSON."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    """Guarda los usuarios en el archivo JSON."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        users = load_users()

        if username in users:
            return "Usuario ya existe", 400

        # Derivar el secreto x a partir de la contraseña
        x = hash_password(password)

        # Computar la clave pública y
        y = compute_public_key(x)

        # Almacenar en la "base de datos"
        users[username] = {
            'y': y  # Clave pública del usuario
        }

        save_users(users)

        return redirect(url_for('main.login_step1'))
    return render_template('register.html', form=form)

@main.route('/login_step1', methods=['GET', 'POST'])
def login_step1():
    form = LoginStep1Form()
    if form.validate_on_submit():
        username = form.username.data

        users = load_users()
        user = users.get(username)
        if not user:
            return "Usuario no encontrado", 400

        # Generar un desafío c (0 o 1)
        c = int.from_bytes(os.urandom(1), 'big') % 2
        session['c'] = c
        session['username'] = username

        return redirect(url_for('main.login_step2'))
    return render_template('login_step1.html', form=form)

@main.route('/login_step2', methods=['GET', 'POST'])
def login_step2():
    form = LoginStep2Form()
    if 'c' not in session or 'username' not in session:
        return redirect(url_for('main.login_step1'))

    c = session['c']
    username = session['username']

    users = load_users()
    user = users.get(username)
    if not user:
        return "Usuario no encontrado", 400

    y = user['y']

    if form.validate_on_submit():
        try:
            s = int(form.s.data)
        except ValueError:
            return "Prueba inválida", 400

        # Verificar la prueba
        if verify_proof(s, y, c):
            session['authenticated'] = True
            return redirect(url_for('main.dashboard'))
        else:
            return "Inicio de sesión fallido", 400

    return render_template('login_step2.html', form=form, c=c)

@main.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('main.login_step1'))
    username = session.get('username')
    return render_template('dashboard.html', username=username)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
