from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
import requests
from app.poke import login_required
from app.db import get_db

bppoke = Blueprint('pokedex', __name__, url_prefix='/pokedex')

class Pokemon:
    def __init__(self, name, attact):
        self.name = name
        self.attact = attact

@bppoke.route('/')
def index():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=10'
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
            pokemons.append(Pokemon(name, image_url))
            print(name)

        return render_template('menu/menu.html', pokemons=pokemons)
    except requests.exceptions.RequestException as e:
        return f'Error en la solicitud: {e}'


@bppoke.route('/pokemones')
@login_required
def pokemones():
    return render_template('menu/pokemones.html')



pokemon_name = "pikachu"
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

response = requests.get(url)
if response.status_code == 200:
    pokemon_data = response.json()
    image_url = pokemon_data["sprites"]["front_default"]
    print(f"URL de la imagen de {pokemon_name}: {image_url}")
else:
    print(f"No se pudo obtener la información de {pokemon_name}")
