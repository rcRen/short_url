from cassandra.cluster import Cluster
from src.config import config
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def connect_to_cassandra(config_mode):
    cassandra_keyspace = config[config_mode].CASSANDRA_KEYSPACE
    cassandra_host = config[config_mode].CASSANDRA_HOST
    cassandra_port = config[config_mode].CASSANDRA_PORT

    cluster = Cluster([cassandra_host], cassandra_port)
    session = cluster.connect()
    session.execute(
        f"CREATE  KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH REPLICATION = {{'class': 'SimpleStrategy', 'replication_factor' : 1 }} ")
    return session
