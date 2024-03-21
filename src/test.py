import hashlib

def base62_encode(num):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base62 = ""

    while num > 0:
        num, remainder = divmod(num, 62)
        base62 = characters[remainder] + base62

    return base62 or "0"


def url_shortener(slug):
    article_id = hashlib.sha256(slug.encode()).hexdigest()[:8]

    print(article_id)

    return base62_encode(int(article_id, 16))

print(url_shortener("guan-yu-yi-se-lie-ha-ma-si-zhan-zheng-de-dong-yi-jiang-dui-jia-sha-de-xun-qiu-bi-hu-zhe-chan-sheng-ying-xiang-mi-lei-1710963903712"))