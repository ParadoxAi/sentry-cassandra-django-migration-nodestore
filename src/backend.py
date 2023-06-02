
from sentry.nodestore.base import NodeStorage
from sentry.nodestore.django.backend import DjangoNodeStorage

# working around dashes in the package name
import importlib
sentry_cassandra_nodestore_backend = importlib.import_module('sentry-cassandra-nodestore.backend')
CassandraNodeStorage = getattr(sentry_cassandra_nodestore_backend, 'CassandraNodeStorage')

class CassandraDjangoMigrationNodeStorage(NodeStorage):
    def __init__(self, servers, keyspace='sentry', columnfamily='nodestore', **kwargs):
        self.cassandra_storage = CassandraNodeStorage(
            servers=servers,
            keyspace=keyspace,
            columnfamily=columnfamily,
            **kwargs
        )
        self.django_storage = DjangoNodeStorage()
        super(CassandraDjangoMigrationNodeStorage, self).__init__()

    def _get_bytes(self, id):
        bytes_data = self.cassandra_storage._get_bytes(id)
        if bytes_data is None:
            bytes_data = self.django_storage._get_bytes(id)
        return bytes_data

    def _get_bytes_multi(self, id_list):
        bytes_data = self.cassandra_storage._get_bytes_multi(id_list)
        missing_ids = [id for id in id_list if id not in bytes_data]
        if missing_ids:
            django_bytes_data = self.django_storage._get_bytes_multi(missing_ids)
            bytes_data.update(django_bytes_data)
        return bytes_data

    def _set_bytes(self, id, data, ttl=None):
        self.cassandra_storage._set_bytes(id, data, ttl=ttl)

    def delete(self, id):
        self.cassandra_storage.delete(id)
        self.django_storage.delete(id)
        self._delete_cache_item(id)

    def delete_multi(self, id_list):
        self.cassandra_storage.delete_multi(id_list)
        self.django_storage.delete_multi(id_list)
        self._delete_cache_items(id_list)

    def cleanup(self, cutoff_timestamp):
        self.cassandra_storage.cleanup(cutoff_timestamp)
        self.django_storage.cleanup(cutoff_timestamp)

    def bootstrap(self):
        self.cassandra_storage.bootstrap()
        self.django_storage.bootstrap()
