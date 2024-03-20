from flask import request, jsonify, Blueprint
from src.config import db
from src.models.short_links import Links
from src.utils import generate_short_code

api = Blueprint('api', __name__)


@api.route('/create', methods=['POST'])
def create_link():
    path = request.json.get("path")
    utm_source = request.json.get("utm_source")
    utm_campaign = request.json.get("utm_campaign")
    utm_medium = request.json.get("utm_medium")
    utm_content = request.json.get("utm_content")
    utm_term = request.json.get("utm_term")
    country_code = request.json.get("country_code")

    short_code = generate_short_code(path=path, utm_source=utm_source, utm_campaign=utm_campaign,
                                     utm_medium=utm_medium, utm_content=utm_content, utm_term=utm_term, country_code=country_code)

    if not short_code:
        return jsonify({"message": "Something wrong, Can not generate short link"}), 400

    exist_code = Links.query.filter_by(short_code=short_code).first()
    if exist_code:
        return jsonify({"message": "short code is exist", "short code": exist_code.short_code}), 422

    new_short_link = Links(path=path, short_code=short_code, utm_source=utm_source, utm_campaign=utm_campaign,
                           utm_medium=utm_medium, utm_content=utm_content, utm_term=utm_term, country_code=country_code)

    try:
        db.session.add(new_short_link)
        db.session.commit()
        return jsonify({"short code:": short_code}), 201
    except Exception as error:
        return jsonify({"message": str(error)}), 400


@api.route('/', methods=["GET"])
def get_all_links():
    links = Links.query.all()
    return jsonify({"links": links})

