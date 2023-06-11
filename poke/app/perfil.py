from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from app.poke import login_required
from app.db import get_db
from werkzeug.utils import secure_filename

import re
import functools


from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

    if request.method == 'POST':
        new_name = request.form['new_name']
        new_lastname = request.form['new_lastname']

        if not new_name:
            error = 'El nombre es requerido'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, error=error)

        if not new_lastname:
            error = 'El apellido es requerido'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, error=error)

        # Validar que name y lastname no contengan números ni caracteres especiales
        if not re.match("^[a-zA-Z\s]+$", new_name):
            error = 'El nombre solo debe contener letras'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, error=error)
        
        if not re.match("^[a-zA-Z\s]+$", new_lastname):
            error = 'El apellido solo debe contener letras'
            return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, error=error)

        # Actualizar el nombre y apellido en la base de datos
        db, c = get_db()
        c.execute("UPDATE users SET name = %s, last_name = %s WHERE id_user = %s", (new_name, new_lastname, user_id))
        db.commit()

        flash('Se ha actualizado el nombre correctamente')
        return redirect(url_for('perfil.perfil'))

    return render_template('perfil/perfil.html', nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, error=error)



@bpp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

#/////////////////////////////////////////////
    upload_folder = bpp.static_folder
    filename = None  # Valor por defecto

#////////////////////////////////////////////


    if request.method == 'POST':
        file = request.files['file']
        db, c = get_db()
        file.save(os.path.join(upload_folder, filename))

        if not file:
            error = 'Archivo requerido'
            return render_template('perfil/perfil.html', error=error)

        # Convertir el objeto FileStorage en una representación binaria
        file_data = file.read()

        # Revisar si la imagen ya existe en la base de datos
        c.execute('SELECT imagen FROM imagen WHERE imagen = %s', (file_data,))
        imagen = c.fetchone()

        if imagen is not None:
            error = 'La imagen ya está registrada.'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(bpp.config['UPLOAD_FOLDER'], filename))
            # Aquí puedes guardar la información del archivo en la base de datos relacionada con el usuario actual
            # user_id = g.user['id']
            # Guardar la representación binaria en la base de datos junto con el user_id
            c.execute('INSERT INTO imagen (imagen) VALUES (%s)', (file_data,))
            db.commit()

            flash('Archivo subido exitosamente')
            return redirect(url_for('perfil.perfil'))

    flash(error)
    return render_template('perfil/perfil.html', error=error)



def hola():
        if request.method == 'POST':
            file = request.files['file']
            db, c = get_db()

        if not file:
            error = 'Archivo requerido'
            return render_template('perfil/perfil.html', error=error)

        else:
            redirect(url_for('perfil.upload'))

