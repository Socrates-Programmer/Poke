
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from app.poke import login_required
from app.db import get_db


bpp = Blueprint('perfil', __name__, url_prefix='perfil')


@bpp.route('mi_perfil')
@login_required
def perfil():
    return 'Hola, este es mi perfil.'

