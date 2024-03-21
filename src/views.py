from flask import request, jsonify, Blueprint
from src.config import db
from src.models.short_links import Links
from src.utils import generate_short_code

api = Blueprint('api', __name__)


@api.route('/create', methods=['POST'])
def create_link():
    data = request.get_json()
    path = data.get("path")
    utm_source = data.get("utm_source")
    utm_campaign = data.get("utm_campaign")
    utm_medium = data.get("utm_medium")
    utm_content = data.get("utm_content")
    utm_term = data.get("utm_term")
    country_code = data.get("country_code")

    if (not path or not country_code):
        return jsonify({"message": "Path and Country Code are required"}), 400

    short_code = generate_short_code(path=path, utm_source=utm_source, utm_campaign=utm_campaign,
                                     utm_medium=utm_medium, utm_content=utm_content, utm_term=utm_term)
    if not short_code:
        return jsonify({"message": "Something wrong, Can not generate short link"}), 400

    exist_code = Links.query.filter_by(short_code=short_code).first()
    if exist_code:
        campaign_params = exist_code.campaign_params()
        return jsonify({"message": "Short code has already generated", "short_code": exist_code.short_code, "country_code": exist_code.country_code, "campaign_params": campaign_params}), 422

    new_short_link = Links(path=path, short_code=short_code, utm_source=utm_source, utm_campaign=utm_campaign,
                           utm_medium=utm_medium, utm_content=utm_content, utm_term=utm_term, country_code=country_code)

    try:
        db.session.add(new_short_link)
        db.session.commit()
        return jsonify({"short_code": short_code, "country_code": country_code, "campaign_params": new_short_link.campaign_params()}), 201
    except Exception as error:
        return jsonify({"message": str(error)}), 400


@api.route('/get_all', methods=["GET"])
def get_all_links():
    links = Links.query.all()
    json_links = [{"short_code": link.short_code,
                   "country_code": link.country_code,
                   "campaign_params": link.campaign_params()} for link in links]
    return jsonify({"result": json_links})
