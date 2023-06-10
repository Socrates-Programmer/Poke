from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from app.poke import login_required
from app.db import get_db

bppoke = Blueprint('pokedex', __name__, url_prefix='/pokedex')

@bppoke.route('/')
def index():
    return render_template('menu/menu.html')

@bppoke.route('/pokemones')
@login_required
def pokemones():
    return render_template('menu/pokemones.html')

