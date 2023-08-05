from flask import Blueprint, render_template, url_for, request, redirect, flash, session, g, abort
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
import re
import functools

import base64
from flask import send_file


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import path
import os

""" 
//////

session para crear session del usuario y tenga cosas personalizadas

Check_password_hash es para encriptar la contraseña

tambien tenenmos a {from app.db import get_db}, esto es importando 

/////

"""

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar si la carpeta de carga existe, si no, crearla
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

bp = Blueprint('pokedex', __name__, url_prefix='/')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=['POST', 'GET'])
def index():
    db, c = get_db()

    # Obtener el nombre del usuario de la base de datos
    if 'user' in g and g.user is not None:
        user_id = g.user['id_user']
        c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
        image_data = c.fetchone()
        imagen_path = image_data['imagen'] if image_data else None
    else:
        imagen_path = None

    # Antes del bloque if request.method == 'POST':
    imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

    return render_template('menus/index.html', imagen_base64=imagen_base64 if 'user' in g and g.user else None)

"""

Arriba es la pagina principal donde entra usuario al iniciar la pagina.

"""

@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    db, c = get_db()
    error = None

    if 'user' in g and g.user is not None:
        db, c = get_db()
        #Obtener el nombre del usuario de la base de datos
        user_id = g.user['id_user']
        c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
        image_data = c.fetchone()
        imagen_path = image_data['imagen'] if image_data else None
        #Obtener el nombre del usuario de la base de datos////
    # Antes del bloque if request.method == 'POST'
        imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

        return render_template('menus/index.html', imagen_base64=imagen_base64 if session else None)

    #////////////REQUEST DE LOS INPUTS START////////

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
    #////////////REQUEST DE LOS INPUTS START////////ENDS

    #funcion de campos requeridos
        if not name:
            error = 'name es requerido'
            return render_template('registros/signup.html', error=error)

        if not lastname:
            error = 'lastname es requerido'
            return render_template('registros/signup.html', error=error)

        if not email:
            error = 'email es requerido'
            return render_template('registros/signup.html', error=error)

        if not password:
            error = 'password es requerido'
            return render_template('registros/signup.html', error=error)
          #funcion de campos requeridos ENDS

    #////////NO ACEPTAR CARECTERES ESPECIALES/////////////
        if not re.match("^[a-zA-Z\s]+$", name):
            error = 'name solo debe contener letras.'
            return redirect(url_for('pokedex.signup'))
        
        elif not re.match("^[a-zA-Z\s]+$", lastname):
            error = 'lastname solo debe contener letras.'
            return redirect(url_for('pokedex.signup'))
        
        elif not re.match(r'^[^\'"=]*$', password):
            error = 'Password no puede contener: Guiones, comullas y signo de igual.'
            return redirect(url_for('pokedex.signup'))
    #////////NO ACEPTAR CARECTERES ESPECIALES/////////////ENDS

    #////Esto revisa si el correo ya esta registrado/////////
        c.execute('SELECT id_user FROM users WHERE email = %s', (email,))
        email_user = c.fetchone()

        if email_user is not None:
            error = 'El correo electrónico {} ya está registrado.'.format(email)
    #////Esto revisa si el correo ya esta registrado/////////EMDS

    #INSERTAR TADOS A LA BASE DE DATOS START///////////////////////////////////////////////////
        else:
            c.execute('INSERT INTO users (name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                      (name, lastname, email, generate_password_hash(password)))
            db.commit()
            
            flash('¡Registro exitoso! Por favor, inicia sesión.')
            return redirect(url_for('pokedex.login'))


        flash(error)
    #INSERTAR TADOS A LA BASE DE DATOS END/////////////////////////////////////////////////////////

    return render_template('registros/signup.html', error=error)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in g and g.user is not None:
        db, c = get_db()
        #Obtener el nombre del usuario de la base de datos
        user_id = g.user['id_user']
        c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
        image_data = c.fetchone()
        imagen_path = image_data['imagen'] if image_data else None
        #Obtener el nombre del usuario de la base de datos////
    # Antes del bloque if request.method == 'POST'
        imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

        return render_template('menus/index.html', imagen_base64=imagen_base64 if session else None)

    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db, c = get_db()
    # Validar que name y lastname no contengan números ni caracteres especiales
        if not email:
            error = 'email es requerido'
            return render_template('registros/login.html', error=error)

        if not password:
            error = 'password es requerido'
            return render_template('registros/login.html', error=error)
    # Validar que name y lastname no contengan números ni caracteres especiales ENDS

        c.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = c.fetchone()
        if user is None:
            error = 'Usuario y/o contraseña inválidos'
            return render_template('registros/login.html', error=error)
        
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválidos'
            return render_template('registros/login.html', error=error)

        if error is None:
            session['user_id'] = user['id_user']
            return redirect(url_for('pokedex.index'))
        
        flash(error)

    return render_template('registros/login.html', error=error)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        db, c = get_db()
        c.execute('SELECT * FROM users WHERE id_user = %s', (user_id,))
        g.user = c.fetchone()

#el decorador login_required se utiliza para proteger 
# ciertas vistas o funciones de una aplicación web para 
# asegurarse de que el usuario haya iniciado sesión antes de acceder a ellas.



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('pokedex.login'))
    
        return view(**kwargs)
    
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pokedex.index'))

def mostrar_imagen():
    db, c = get_db()
    error = None
    #Obtener el nombre del usuario de la base de datos
    user_id = g.user['id_user']
    c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
    image_data = c.fetchone()
    imagen_path = image_data['imagen'] if image_data else None
    #Obtener el nombre del usuario de la base de datos////
# Antes del bloque if request.method == 'POST'
    imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

    return render_template('menus/index.html', imagen_base64=imagen_base64 if session else None)



#def validacion_nombre():
#    if user is not None:
#       error = 'El usuario {} ya está registrado.'.format(name)
        #VALIDACION DE RESGISTROS, PARA QUE NO SE TREPITAN
        #START
#        c.execute('SELECT id_user FROM users WHERE name = %s', (name,))
#        user = c.fetchone()
        # Leer y descartar los resultados de la consulta anterior
#       c.fetchall()



#//////////////////////////FUNCION DE REQUERIMIENTOS DE CAMPOS////////////////////
def campos_requeridos(name, lastname, email, password):

        if not name:
            error = 'name es requerido'
            return redirect(url_for('pokedex.signup'))

        if not lastname:
            error = 'lastname es requerido'
            return redirect(url_for('pokedex.signup'))

        if not email:
            error = 'email es requerido'
            return redirect(url_for('pokedex.signup'))

        if not password:
            error = 'password es requerido'
            return redirect(url_for('pokedex.signup'))
#//////////////////////////FUNCION DE REQUERIMIENTOS DE CAMPOS////////////////////ENDS



#///////////////////////////FUNCION DE VALIDACION DE CARACTERES ESPACIALES///////////////////
def validacion_de_caracteres(name, lastname, password): 
    if not re.match("^[a-zA-Z\s]+$", name):
        error = 'name solo debe contener letras.'
        return redirect(url_for('pokedex.signup'))
    
    elif not re.match("^[a-zA-Z\s]+$", lastname):
        error = 'lastname solo debe contener letras.'
        return redirect(url_for('pokedex.signup'))
    
    elif not re.match(r'^[^\'"=]*$', password):
        error = 'Password no puede contener: Guiones, comullas y signo de igual.'
        return redirect(url_for('pokedex.signup'))
#///////////////////////////FUNCION DE VALIDACION DE CARACTERES ESPACIALES///////////////////ENDS


