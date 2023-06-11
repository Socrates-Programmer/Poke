from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.poke import login_required
from app.db import get_db
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bpp = Blueprint('perfil', __name__, url_prefix='/perfil')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bpp.route('/', methods=["GET", "POST"])
@login_required
def perfil():
    error = None
    if request.method == 'POST':
        file = request.form['file']
        db, c = get_db()

        if not file:
            error = 'file es requerido'
            return render_template('perfil/perfil.html', error=error)
        #//////////////////////////////////////////////////////////////////////////////
        #VALIDACION DE RESGISTROS, PARA QUE NO SE TREPITAN
        #START
        c.execute('SELECT id_user FROM perfil WHERE name = %s', (file,))
        file = c.fetchone()
        # Leer y descartar los resultados de la consulta anterior
        c.fetchall()





    flash(error)

    return render_template('perfil/perfil.html', error=error)


@bpp.route('/upload', methods=['GET', 'POST'])
def upload():

    return "Esto es upload"



