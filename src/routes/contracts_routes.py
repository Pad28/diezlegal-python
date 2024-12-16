from flask import Blueprint
from controllers.contracts_controller import get_contract_by_name


bp = Blueprint("contracts_routes", __name__, url_prefix="/contracts")

# Se debe incluir el nombre del contrato en el body de la peticion en un atributo llamando contract_name
# para realizar la busque en las carpetas
@bp.route("/", methods=["GET"])
def get_contract_data():
    return get_contract_by_name()
