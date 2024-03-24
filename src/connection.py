from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from src.config import config
from src.models.short_link import ShortLink
import os


def load_config():
    config_mode = os.environ.get('CONFIG_MODE')
    Config = config[config_mode]
    return Config


def setup_connection(config):
    cassandra_keyspace = config.CASSANDRA_KEYSPACE
    cassandra_host = config.CASSANDRA_HOST
    cassandra_port = config.CASSANDRA_PORT

    auth_provider = PlainTextAuthProvider(
        username=os.environ.get("CASS_USERNAME"), password=os.environ.get("CASS_PASSWORD"))

    cluster = Cluster([cassandra_host], cassandra_port,
                      auth_provider=auth_provider)
    session = cluster.connect()

    conns = 'cluster1'

    connection.register_connection(conns, session=session, default=True)

    create_keyspace_simple(name=cassandra_keyspace,
                           connections=[conns], replication_factor=1)

    sync_tables()


def sync_tables():
    sync_table(ShortLink)
