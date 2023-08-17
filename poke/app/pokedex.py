from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from werkzeug.exceptions import abort
import requests
from app.poke import login_required
from app.db import get_db
import base64
import requests


bppoke = Blueprint('pokedex', __name__, url_prefix='/pokedex')

class Pokemon:
    def __init__(self, name, attact):
        self.name = name
        self.attact = attact

@bppoke.route('/')
def index():
    if g.user:
        db, c = get_db()
        #Obtener el nombre del usuario de la base de datos
        user_id = g.user['id_user']
        c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
        image_data = c.fetchone()
        imagen_path = image_data['imagen'] if image_data else None
        #Obtener el nombre del usuario de la base de datos////
    # Antes del bloque if request.method == 'POST'
        imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

    class Pokemon:
        def __init__(self, name, image_url):
            self.name = name
            self.image_url = image_url

    url = 'https://pokeapi.co/api/v2/pokemon?limit=12'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])
        pokemons = []
        for result in results:
            name = result['name']
            pokemon_url = result['url']
            pokemon_data = requests.get(pokemon_url).json()
            image_url = pokemon_data['sprites']['front_default']
            pokemons.append(Pokemon(name, image_url))
            print(name)
        return render_template('menus/pokedex.html', pokemons=pokemons, imagen_base64=imagen_base64 if session else None)
    except requests.exceptions.RequestException as e:
        return f'Error en la solicitud: {e}'


@bppoke.route('/friends')
@login_required
def pokemones():
    db, c = get_db()

    if g.user:
        user_id = g.user['id_user']
        # Obtener la imagen del usuario de la base de datos
        c.execute("SELECT imagen FROM users WHERE id_user = %s", (user_id,))
        image_data = c.fetchone()
        imagen_path = image_data['imagen'] if image_data else None

        #Obtener el nombre del usuario de la base de datos////
    # Antes del bloque if request.method == 'POST'
        imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

        # Obtener el nombre y el apellido de todos los usuarios de la base de datos
        c.execute("SELECT name, last_name, imagen FROM users")
        all_users = c.fetchall()
        users_list = [{'name': user['name'], 'last_name': user['last_name']} for user in all_users]

        # Obtener la imagen de cada usuario y codificarla en base64
        imagen_users_base64 = []
        for user in all_users:
            imagen_path = user['imagen']
            if imagen_path:
                imagen_base64 = base64.b64encode(imagen_path).decode('utf-8')
                imagen_users_base64.append(imagen_base64)
            else:
                imagen_users_base64.append(None)
    else:
        abort(401)

    return render_template('menus/friends.html', imagen_base64=imagen_base64 if session else None, friends = users_list, imagen_users_base64 = imagen_users_base64 )


@bppoke.route('/posts')
@login_required
def post():
    db, c = get_db()

    # Obtener el nombre del usuario de la base de datos

    if g.user:
        user_id = g.user['id_user']

        c.execute("SELECT name, imagen FROM users WHERE id_user = %s", (user_id,))
        user_data = c.fetchone()
        imagen_path = user_data['imagen'] if user_data else None
        user_name = user_data['name']
    else:
        return abort(401)

    # Antes del bloque if request.method == 'POST':
    imagen_base64 = base64.b64encode(imagen_path).decode('utf-8') if imagen_path else None

    return render_template('contenido/posts.html', imagen_base64=imagen_base64, username = user_name)


# pokemon_name = "pikachu"
# url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

# response = requests.get(url)
# if response.status_code == 200:
#     pokemon_data = response.json()
#     image_url = pokemon_data["sprites"]["front_default"]
#     print(f"URL de la imagen de {pokemon_name}: {image_url}")
# else:
#     print(f"No se pudo obtener la información de {pokemon_name}")
