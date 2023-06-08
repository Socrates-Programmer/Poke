from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from app.poke import login_required
from app.db import get_db

bp = Blueprint('pokedex', __name__, url_prefix='/pokedex')

@bp.route('/')
@login_required
def index():
    return render_template('menu/menu.html')
