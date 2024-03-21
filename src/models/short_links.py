from src.config import db
from src.utils import build_campaign_params


class Links(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_code = db.Column(db.String(50), unique=True, nullable=False)
    country_code = db.Column(db.String(20), nullable=False)
    utm_source = db.Column(db.String(120), unique=False, nullable=True)
    utm_campaign = db.Column(db.String(120), unique=False, nullable=True)
    utm_medium = db.Column(db.String(120), unique=False, nullable=True)
    utm_content = db.Column(db.String(120), unique=False, nullable=True)
    utm_term = db.Column(db.String(120), unique=False, nullable=True)
    path = db.Column(db.String(255), unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "short_code": self.short_code,
            "country_code": self.country_code,
            "path": self.path,
            "utm_source": self.utm_source,
            "utm_campaign": self.utm_campaign,
            "utm_medium": self.utm_medium,
            "utm_content": self.utm_content,
            "utm_term": self.utm_term
        }

    def campaign_params(self):
        return build_campaign_params(
            path=self.path, **{k: v for k, v in self.__dict__.items() if k.startswith('utm_')})
