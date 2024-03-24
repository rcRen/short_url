import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from src.utils import build_campaign_params
from cassandra.cqlengine.management import sync_table


class ShortLink(Model):
    __keyspace__ = 'links'
    __table_name__ = 'links'

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    short_code = columns.Text(primary_key=True, required=True)
    country_code = columns.Text(required=True)
    utm_source = columns.Text()
    utm_campaign = columns.Text()
    utm_medium = columns.Text()
    utm_content = columns.Text()
    utm_term = columns.Text()
    path = columns.Text(required=True)

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

    # remove the empty fields
    def filtered_json(self):
        return {key: value for key, value in self.to_json(
        ).items() if value not in ("", None)}

    def campaign_params(self):
        return build_campaign_params(
            path=self.path, **{k: v for k, v in self.__dict__.items() if k.startswith('utm_')})
