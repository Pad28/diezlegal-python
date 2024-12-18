from flask import jsonify, request, current_app
import os
import pandas as pd 
from utils.traspose_table import trasponseTable
import json

def buscar_carpeta(nombre_carpeta, ruta):
    # Listar todos los elementos en la ruta especificada
    for elemento in os.listdir(ruta):
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
    
    definiciones = pd.read_csv(f"{files_path}/Definiciones.csv", encoding="utf-8")
    definiciones = definiciones.dropna(subset=["Definiciones"])
    definiciones = definiciones[["Definiciones"]].to_dict(orient="records")
    
    try:
        declaraciones = pd.read_csv(f"{files_path}/Declaraciones.csv", encoding="utf-8")
    except UnicodeDecodeError:
        print("Error con utf-8. Intentando con latin1...")
        declaraciones = pd.read_csv(f"{files_path}/Declaraciones.csv", encoding="latin1")
    
    current_case = None
    for index, row in declaraciones.iterrows():
        if pd.notna(row['Caso']):
            current_case = row['Caso']
        else:
            declaraciones.at[index, 'Caso'] = current_case

    declaraciones = declaraciones.dropna(subset=["Instrucciones para el usuario"])
    declaraciones = declaraciones.groupby("Caso")["Instrucciones para el usuario"].apply(list).to_dict()

   # Cargar cláusulas sugeridas
    try:
        clausulas_sugeridas = pd.read_csv(f"{files_path}/Clausulas sugeridas.csv", encoding="utf-8")
        # Reemplazar NaN por None
        clausulas_sugeridas = clausulas_sugeridas.where(pd.notnull(clausulas_sugeridas), None)
        clausulas_sugeridas = clausulas_sugeridas.to_dict(orient="records")
    except FileNotFoundError:
        return jsonify({"error": "Clausulas sugeridas file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error loading Clausulas sugeridas: {str(e)}"}), 500

   # Cargar cláusulas adicionales
    # try:
    #     clausulas_adicionales = pd.read_csv(f"{files_path}/Clausulas adicionales.csv", encoding="utf-8")
    #     clausulas_adicionales = clausulas_adicionales.where(pd.notnull(clausulas_adicionales), None)
    #     clausulas_adicionales = clausulas_adicionales.to_dict(orient="records")
    #     clausulas_adicionales = [clausula for clausula in clausulas_adicionales if clausula['Nombre'] is not None]
    # except FileNotFoundError:
    #     return jsonify({"error": "Clausulas adicionales file not found"}), 404
    # except Exception as e:
    #     return jsonify({"error": f"Error loading Clausulas adicionales: {str(e)}"}), 500

    # Cargar cláusulas obligatorias
    try:
        clausulas_obligatorias = pd.read_csv(f"{files_path}/Clausulas obligatorias.csv", encoding="utf-8")
        clausulas_obligatorias = clausulas_sugeridas.where(pd.notnull(clausulas_obligatorias), None)
        clausulas_obligatorias = clausulas_obligatorias.to_dict(orient="records")
    except FileNotFoundError:
        return jsonify({"error": "Clausulas clausulas_obligatorias file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error loading Clausulas clausulas_obligatorias: {str(e)}"}), 500

    return jsonify({
        "ok": True,
        "data": {
            "rubro": rubro.to_dict(orient="records"),
            "proemio": proemio.to_dict(orient="records")[0],
            "definiciones": definiciones,
            "declaraciones": declaraciones,
            "clausulas_sugeridas": clausulas_sugeridas,
            # "clausulas_adicionales": clausulas_adicionales,
            "clausulas_obligatorias": clausulas_obligatorias,
        } 
    })
    
def clean_dataframe_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y escapa strings en un DataFrame.
    """
    # Itera sobre cada celda del DataFrame y limpia strings
    return df.applymap(lambda x: str(x).replace('"', '\\"').replace("\\", "\\\\") if isinstance(x, str) else x)

