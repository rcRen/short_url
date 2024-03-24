from cassandra.cqlengine.query import DoesNotExist
from src.models.short_link import ShortLink
from flask import request, jsonify
from src.utils import generate_short_code

# get all links
def get_all():
    all_links = []
    for link in ShortLink.objects().all():
        filtered_link = link.filtered_json()
        all_links.append(filtered_link)
    return jsonify({"results": all_links})


# generate a new short link and save to database
def create_short_link():
    data = request.get_json()
    path = data.get("path")
    utm_source = data.get("utm_source", None)
    utm_campaign = data.get("utm_campaign", None)
    utm_medium = data.get("utm_medium", None)
    utm_content = data.get("utm_content", None)
    utm_term = data.get("utm_term", None)
    country_code = data.get("country_code")

    if (not path or not country_code):
        return jsonify({"message": "Path and Country Code are required"}), 400

    short_code = generate_short_code(path=path, utm_source=utm_source, utm_campaign=utm_campaign,
                                     utm_medium=utm_medium, utm_content=utm_content, utm_term=utm_term)
    if not short_code:
        return jsonify({"message": "Something wrong, Can not generate short link"}), 400

    exist_code = ShortLink.objects.filter(
        short_code=short_code).allow_filtering().first()

    if exist_code:
        # campaign_params = exist_code.campaign_params()
        return jsonify({"message": "Short code has already generated", "short_code": exist_code.short_code, "country_code": exist_code.country_code}), 422

    try:
        new_short_link = ShortLink.create(path=path, short_code=short_code, utm_source=utm_source, utm_campaign=utm_campaign,
                                          utm_medium=utm_medium, utm_content=utm_content, utm_term=utm_term, country_code=country_code)
        return jsonify({"message": "Generate short code successfully.", "short_code": short_code, "country_code": country_code, "campaign_params": new_short_link.campaign_params()}), 201
    except Exception as error:
        return jsonify({"message": str(error)}), 400


# get result by short_code
def get_link_by_code(short_code):
    try:
        link = ShortLink.objects(
            short_code=short_code).allow_filtering().first()

        if link:
            return jsonify({"result": link.filtered_json()}), 201
        else:
            return jsonify({"error": "Link not found"}), 404

    except DoesNotExist:
        return None


# get result by country_code
def get_link_by_country(country_code):
    try:
        links = ShortLink.objects(
            country_code=country_code).allow_filtering()

        if links:
            links_in_country = []
            for link in links:
                links_in_country.append(link.filtered_json())
            return jsonify({"results": links_in_country})
        else:
            return jsonify({"error": "No links found in this country code"}), 404
    except DoesNotExist:
        return None
