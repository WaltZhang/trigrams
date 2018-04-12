import sqlalchemy

DB_TYPETO_PROTOCOL = {
    'sqlite': 'sqlite+pysqlite',
    'mysql': 'mysql+pymysql',
    'postgresql': 'postgresql+pygresql',
    'oracle': 'oracle+cx_oracle',
    'mssql': 'mssql+pyodbc',
}


def create_connection(db_type, user, password, host, port, db_instance):
    protocol = DB_TYPETO_PROTOCOL.get(db_type)
    url = "{}://{}:{}@{}:{}/{}".format(protocol,
                                       user,
                                       password,
                                       host,
                                       port,
                                       db_instance)
    engine = sqlalchemy.create_engine(url)
    connection = engine.connect()
    return connection
