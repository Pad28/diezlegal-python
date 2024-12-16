from flask import Blueprint
from controllers.uploads_controller import upload_excel_controller

bp = Blueprint("uploads_routes", __name__, url_prefix="/uploads")

@bp.route("/", methods=["POST"])
def upload_excel():
    return upload_excel_controller()