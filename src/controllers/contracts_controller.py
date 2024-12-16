from flask import jsonify, request, current_app
import os
import pandas as pd 
from utils.traspose_table import trasponseTable

def buscar_carpeta(nombre_carpeta, ruta):
    # Listar todos los elementos en la ruta especificada
    for elemento in os.listdir(ruta):
        # Comprobar si el elemento es una carpeta y coincide con el nombre buscado
        if os.path.isdir(os.path.join(ruta, elemento)) and elemento == nombre_carpeta:
            return True
    return False

# Se debe incluir el nombre del contrato en el body de la peticion en un atributo llamando contract_name
# para realizar la busque en las carpetas
def get_contract_by_name():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'contract_name' not in data or not isinstance(data['contract_name'], str):
        return jsonify({"error": "Invalid or missing 'contract_name'"}), 400

    files_path = current_app.config['UPLOAD_FOLDER']
    flag = buscar_carpeta(nombre_carpeta=data["contract_name"], ruta=files_path)
    
    
    if not flag:
        return jsonify({ "error": "Invalid contract name" }), 400
    
    files_path = os.path.normpath(f"{files_path}/{data['contract_name']}")
    rubro = trasponseTable(path=f"{files_path}/Rubro.csv")
    proemio = trasponseTable(path=f"{files_path}/Proemio.csv")
    definiciones = pd.read_csv(f"{files_path}/Definiciones.csv")
    declaraciones = pd.read_csv(f"{files_path}/Declaraciones.csv")
    clausulas_sugeridas = pd.read_csv(f"{files_path}/Clausulas sugeridas.csv")
    clausulas_adicionales = pd.read_csv(f"{files_path}/Clausulas adicionales.csv")
    clausulas_obligatorias = pd.read_csv(f"{files_path}/Clausulas obligatorias.csv")
    
    return jsonify({
        "rubro": rubro.to_dict(orient="records"),
        "proemio": proemio.to_dict(orient="records"),
        "definiciones": definiciones.to_dict(orient="records"),
        "declaraciones": declaraciones.to_dict(orient="records"),
        "clausulas_sugeridas": clausulas_sugeridas.to_dict(orient="records"),
        "clausulas_adicionales": clausulas_adicionales.to_dict(orient="records"),
        "clausulas_obligatorias": clausulas_obligatorias.to_dict(orient="records"),
    })