#!/usr/bin/env python

from flask import Flask, jsonify
import pandas as pd
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

# Cargar datos desde los archivos CSV
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Realizar alguna manipulación de datos si es necesario

@app.route("/")
def index():
    # Devolver mensaje de uso
    return "Link a usar : http://<hostname>[:<prt>]/api/movies"

@app.route("/api/movies")
def get_movies():
    # Comprobar si los datos están en la caché
    cached_data = redis.get('movies_data')
    if cached_data:
        # Si está en caché, devolver los datos en caché
        return jsonify(eval(cached_data))

    # Si no está en caché, convertir los datos a formato JSON
    data = movies.to_dict(orient='records')

    # Almacenar los datos en la caché con un tiempo de espera de 60 segundos 
    redis.setex('movies_data', 60, str(data))

    return jsonify(data)

@app.route("/api/ratings")
def get_ratings():
    # Comprobar si los datos están en la caché
    cached_data = redis.get('ratings_data')
    if cached_data:
        # Si está en caché, devolver los datos en caché
        return jsonify(eval(cached_data))

    # Si no está en caché, convertir los datos a formato JSON
    data = ratings.to_dict(orient='records')

    # Almacenar los datos en la caché con un tiempo de espera de 60 segundos (ajustar según sea necesario)
    redis.setex('ratings_data', 60, str(data))

    return jsonify(data)

if __name__ == "__main__":
    # Ejecutar la aplicación Flask en el host 0.0.0.0
    app.run(host="0.0.0.0")
