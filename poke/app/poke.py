from flask import Blueprint, render_template, url_for, request, redirect, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
import re
import functools


""" 
//////

session para crear session del usuario y tenga cosas personalizadas

Check_password_hash es para encriptar la contraseña

tambien tenenmos a {from app.db import get_db}, esto es importando 

/////

"""

bp = Blueprint('pokedex', __name__, url_prefix='/')


@bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('menu/index.html')

"""

Arriba es la pagina principal donde entra usuario al iniciar la pagina.

"""

@bp.route('/signup', methods=['POST', 'GET'])
def signup():#REQUEST DE LOS INPUTS START/////////////////////////////////////////////////////////
    error = None

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        db, c = get_db()

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
#REQUEST DE LOS INPUTS END/////////////////////////////////////////////////////////

# Validar que name y lastname no contengan números ni caracteres especiales
        if not re.match("^[a-zA-Z\s]+$", name):
            error = 'name solo debe contener letras'
            return render_template('registros/signup.html', error=error)
        
        elif not re.match("^[a-zA-Z\s]+$", lastname):
            error = 'lastname solo debe contener letras'
            return render_template('registros/signup.html', error=error)
        
        elif not re.match(r'^[^\'"=]*$', password):
            error = 'lastname solo debe contener letras'
            return render_template('registros/signup.html', error=error)

#//////////////////////////////////////////////////////////////////////////////
        #VALIDACION DE RESGISTROS, PARA QUE NO SE TREPITAN
        #START
        c.execute('SELECT id_user FROM users WHERE name = %s', (name,))
        user = c.fetchone()

        # Leer y descartar los resultados de la consulta anterior
        c.fetchall()

        c.execute('SELECT id_user FROM users WHERE email = %s', (email,))
        email_user = c.fetchone()


        if user is not None:
            error = 'El usuario {} ya está registrado.'.format(name)
        elif email_user is not None:
            error = 'El correo electrónico {} ya está registrado.'.format(email)

        #VALIDACION DE REGISTRO END
#////////////////////////////////////////////////////////////////////////////////////

#INSERTAR TADOS A LA BASE DE DATOS START///////////////////////////////////////////////////
        else:
            c.execute('INSERT INTO users (name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                      (name, lastname, email, generate_password_hash(password)))
            db.commit()
            
            flash('¡Registro exitoso! Por favor, inicia sesión.')
            return redirect(url_for('pokedex.index'))


        flash(error)
#INSERTAR TADOS A LA BASE DE DATOS END/////////////////////////////////////////////////////////

    return render_template('registros/signup.html', error=error)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db, c = get_db()

        if not email:
            error = 'El correo electrónico es requerido'
            return render_template('registros/login.html', error=error)

        if not password:
            error = 'La contraseña es requerida'
            return render_template('registros/login.html', error=error)
        
        # Validar que name y lastname no contengan números ni caracteres especiales
        
        if not re.match(r'^[^\'"=]*$', password):
            error = 'lastname solo debe contener letras'
            return render_template('registros/signup.html', error=error)
        
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

    return render_template('registros/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT * FROM users WHERE id_user = %s', (user_id,))
        g.user = c.fetchone()

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