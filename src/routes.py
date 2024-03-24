from flask import request, jsonify, Blueprint
from src.models.short_link import ShortLink
from src.controllers import get_all, create_short_link, get_link_by_code, get_link_by_country


api = Blueprint('api', __name__)


api.route('/get', methods=['GET'])(get_all)
api.route('/create', methods=['POST'])(create_short_link)
api.route('/<short_code>', methods=['GET'])(get_link_by_code)
api.route('/country/<country_code>', methods=['GET'])(get_link_by_country)
