import hashlib
import string


def generate_short_code(**factors):
    slug = build_campaign_URL(
        path=factors.get("path"), **{k: v for k, v in factors.items() if k.startswith('utm_')})
    sha256_hash = hashlib.sha256(slug.encode()).hexdigest()[:8]

    return base62_encode(int(sha256_hash, 16))


def build_campaign_URL(**factors):
    params = [('path', factors.get("path")),
              ('utm_campaign', factors.get("utm_campaign")),
              ('utm_content', factors.get("utm_content")),
              ('utm_medium', factors.get("utm_medium")),
              ('utm_source', factors.get("utm_source")),
              ('utm_term', factors.get("utm_term"))]

    # sort the factor string order: (domain?, path, utm_campaign?, utm_content?, utm_medium?, utm_source?,utm_term?)
    params.sort(key=lambda x: ('path', 'utm_campaign', 'utm_content',
                'utm_medium', 'utm_source', 'utm_term').index(x[0]))

    utm_fields = [f"{key}={value}" for key,
                  value in params if key.startswith('utm_') and value]

    campaign_URL = factors["path"] + "?" + "&".join(utm_fields)

    return campaign_URL


def base62_encode(num):
    # characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    characters = string.ascii_letters + string.digits
    base62 = ""

    while num > 0:
        num, remainder = divmod(num, 62)
        base62 = characters[remainder] + base62

    return base62 or "0"
