# Sentry Cassandra Django Migration Nodestore

This is a Sentry Nodestore to aid migration from the self-hosted default Django Nodestore to [sentry-cassandra-nodestore](https://pypi.org/project/sentry-cassandra-nodestore).

It is a wrapper for sentry-cassandra-nodestore; which writes all data to Cassandra, reads data from Cassandra first and falls back to Django is the data is not found. Deletes are attempted in both nodestores.

The idea is after the retention period has passed there is a lot less, if any, data to migrate between nodestores as only one can be configred.

## Installation

You should complete the pre-requisites for setting up sentry-cassandra-nodestore.

You can install the `sentry-cassandra-django-migration-nodestore` package using pip:

```bash
pip install git+https://github.com/rjocoleman/sentry-cassandra-django-migration-nodestore.git
```

## Configuration

To use this backend in Sentry, you need to update your Sentry configuration (`sentry/sentry.conf.py`) with the following settings:

1. Set the `SENTRY_NODESTORE` option to `'backend.CassandraDjangoMigrationNodeStorage'`.

2. Set the `SENTRY_NODESTORE_OPTIONS` dictionary with the necessary configuration options (this is identical to CassandraNodeStorage). Here's an example configuration:

```python
SENTRY_NODESTORE = 'backend.CassandraDjangoMigrationNodeStorage'

SENTRY_NODESTORE_OPTIONS = {
    'servers': [
        '127.0.0.1:9042',
    ],
# (optional) specify an alternative keyspace
    'keyspace': 'sentry',
# (optional) specify an alternative columnfamily
    'columnfamily': 'nodestore',
}
```

Make sure to replace the values in the `SENTRY_NODESTORE_OPTIONS` dictionary with your actual details.

## Usage

Once you have installed the package and configured Sentry, it will automatically use the combined Nodestore backends for storing event data.

For more information on using and configuring Sentry, refer to the [Sentry documentation](https://develop.sentry.dev/self-hosted/#configuration).
