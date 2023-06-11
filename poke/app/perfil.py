from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)

import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import mysql.connector

from werkzeug.exceptions import abort
from app.poke import login_required
from app.db import get_db
from werkzeug.utils import secure_filename

import base64

import re
import functools

import base64
from flask import send_file

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import path
import os


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar si la carpeta de carga existe, si no, crearla
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

bpp = Blueprint('perfil', __name__, url_prefix='/perfil', static_folder='static')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
@bpp.route('/', methods=["GET", "POST"])
@login_required
def perfil():
    db, c = get_db()
    error = None

    # Obtener el nombre del usuario de la base de datos
    user_id = g.user['id_user']
    c.execute('SELECT name FROM users WHERE id_user = %s', (user_id,))
    user = c.fetchone()
    nombre_usuario = user['name'] if user else None
    
    last_id = g.user['id_user']
    c.execute('SELECT last_name FROM users WHERE id_user = %s', (last_id,))
    last = c.fetchone()
    apellido_usuario = last['last_name'] if last else None

    c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
    image_data = c.fetchone()
    imagen_path = image_data['imagen'] if image_data else None

    if request.method == 'POST':
        new_name = request.form['new_name']
        new_lastname = request.form['new_lastname']
        file = request.files['file']

        if not file:
            error = 'File es requerido'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, imagen_path=imagen_path, error=error)

        if not new_name:
            error = 'El nombre es requerido'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, imagen_path=imagen_path, error=error)

        if not new_lastname:
            error = 'El apellido es requerido'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, imagen_path=imagen_path, error=error)

        # Validar que name y lastname no contengan números ni caracteres especiales
        if not re.match("^[a-zA-Z\s]+$", new_name):
            error = 'El nombre solo debe contener letras'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, imagen_path=imagen_path, error=error)
        
        if not re.match("^[a-zA-Z\s]+$", new_lastname):
            error = 'El apellido solo debe contener letras'
          
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, imagen_path=imagen_path, error=error)
        
        if file and allowed_file(file.filename):
            image_data = file.read()

            # Guardar la imagen en la base de datos
            cursor = db.cursor()
            cursor.execute("UPDATE users SET imagen = %s WHERE id_user = %s", (image_data, user_id))
            db.commit()


            c.execute("UPDATE users SET name = %s, last_name = %s WHERE id_user = %s", (new_name, new_lastname, user_id))
            db.commit()


        flash('Se ha actualizado el nombre correctamente')

        return redirect(url_for('perfil.perfil'))

    # Convertir los datos de la imagen a una cadena base64
    imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

    return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, imagen_base64=imagen_base64, error=error)

# ...


@bpp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    db, c = get_db()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No se seleccionó ningún archivo')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Guardar la información del archivo en la base de datos
            cursor = db.cursor()
            with open(file_path, 'rb') as f:
                file_data = f.read()
                cursor.execute("INSERT INTO users (imagen) VALUES (%s)", (file_data,))
                db.commit()
            
            flash('Archivo subido exitosamente')
            return redirect(url_for('perfil.perfil'))
        
        flash('Tipo de archivo no permitido')
        return redirect(request.url)
    
    return render_template('perfil/perfil.html')



def hola():
        if request.method == 'POST':
            file = request.files['file']
            db, c = get_db()

        if not file:
            error = 'Archivo requerido'
            return render_template('perfil/perfil.html', error=error)

        else:
            redirect(url_for('perfil.upload'))

@bpp.route('/imagen')
@login_required
def mostrar_imagen():
    user_id = g.user['id_user']
    db, c = get_db()
    c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
    image_data = c.fetchone()
    imagen_path = image_data['imagen'] if image_data else None

    if imagen_path:
        return send_file(imagen_path)

    return abort(404)

