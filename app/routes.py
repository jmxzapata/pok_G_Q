from flask import Blueprint, render_template, request, redirect, url_for, session
from .forms import RegistrationForm, LoginStep1Form, LoginStep2Form
from .gq_protocol import (
    hash_password,
    compute_public_key,
    compute_commitment,
    verify_proof,
    N,
    G
)
import os
import json

main = Blueprint('main', __name__)

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
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

        # Calcular w desde la contraseña
        w = hash_password(password)
        # Calcular y = g^w mod N
        y = compute_public_key(w)

        users[username] = {
            'y': y
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

        # Generar c (0 o 1) y el compromiso t, u
        c = int.from_bytes(os.urandom(1), 'big') % 2
        t, u = compute_commitment()

        session['c'] = c
        session['t'] = t
        session['u'] = u
        session['username'] = username

        return redirect(url_for('main.login_step2'))
    return render_template('login_step1.html', form=form)

@main.route('/login_step2', methods=['GET', 'POST'])
def login_step2():
    form = LoginStep2Form()
    if 'c' not in session or 'username' not in session or 't' not in session or 'u' not in session:
        return redirect(url_for('main.login_step1'))

    c = session['c']
    t = session['t']
    u = session['u']
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

        # Verificación del protocolo
        if verify_proof(u=u, s=s, y=y, c=c):
            session['authenticated'] = True
            return redirect(url_for('main.dashboard'))
        else:
            return "Inicio de sesión fallido", 400

    # Pasar N, G, c, t al template para que el cliente calcule s = t + c*w
    return render_template('login_step2.html', form=form, c=c, t=t, N=N, G=G)

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
