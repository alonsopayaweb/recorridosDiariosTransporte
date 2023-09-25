import json
import os
import shutil
import urllib.request as req
import requests
import pandas as pd
from google.cloud import storage

#Variables necesarias

directorio = "detallerecorrido/"
nombrebucket = "bucketdt"
credential_path = "./keys.json"
proyecto = "datostransporte-391000"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
os.environ["GCLOUD_PROJECT"] = proyecto 

#Descarga local de JSON

url = "https://www.red.cl/restservice_v2/rest/getservicios/all"
nombre_archivo = "all.json"
ruta_guardado = os.path.join(os.getcwd(), nombre_archivo)

# Realizar la solicitud HTTP GET
response = requests.get(url)
data = response.json()

# Verificar si el archivo JSON es una lista
if isinstance(data, list):
    # Iterar sobre cada valor de la lista para obtener el URL de cada recorrido diario
    for n in data:
        print(n)

        idrecorrido = n

        url2 = f"https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={idrecorrido}"
        nombre_archivo = f"conocerecorrido{idrecorrido}.json"
        ruta_guardado = os.path.join(os.getcwd(), nombre_archivo)

        # Realizar la solicitud HTTP GET
        response = requests.get(url2)

        with open(ruta_guardado, "wb") as archivo:
            archivo.write(response.content)

        #Subida a bucket
        client = storage.Client()
        bucket = client.get_bucket(nombrebucket)

        blob = bucket.blob(f'{directorio}conocerecorridos{idrecorrido}.json')
        blob.upload_from_filename(f'conocerecorrido{idrecorrido}.json')