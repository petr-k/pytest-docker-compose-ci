import os
import pytest
import psycopg2


def create_connection(hostname, port):
    """ try to connect to db"""
    try:
        return psycopg2.connect(dbname='test_db', user='su', host=hostname, password='su', port=port)
    except:
        return False


@pytest.fixture(scope='session')
def docker_allow_fallback():
    return True


@pytest.fixture(scope='session')
def db_connection(docker_ip, docker_services):
    port = docker_services.port_for('postgres', 5432)

    hostname = docker_ip
    if "CI_TESTS" in os.environ:
        # When running during tests within docker-compose, we provide hostname and port directly.
        hostname = "postgres"
        port = 5432

    docker_services.wait_until_responsive(
       timeout=30.0, pause=0.5,
       check=lambda: create_connection(hostname, port)
    )

    return create_connection(hostname, port)


@pytest.fixture(autouse=True)
def prepare_db(db_connection):
    """prepares db for test"""
    cur = db_connection.cursor()

    # remove all tables
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
          AND table_type='BASE TABLE'
    """)
    for row in cur.fetchall():
        cur.execute("DROP TABLE {} CASCADE".format(row[0]))

    # create schema
    cur.execute("CREATE TABLE t (a int, b int)")
    # insert test data
    cur.execute("INSERT INTO t (a, b) VALUES (5, 42)")


def test_add(db_connection):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO t (a, b) VALUES (1, 2)")
    cur.execute("SELECT a, b FROM t")

    rows = cur.fetchall()
    assert rows == [(5, 42), (1, 2)]


def test_delete(db_connection):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM t WHERE a=5 AND b=42")
    cur.execute("SELECT a, b FROM t")

    rows = cur.fetchall()
    assert rows == []
