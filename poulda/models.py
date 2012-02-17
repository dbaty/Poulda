"""This module is only used if the support for the Nginx Upload
Progress module has been disabled. If the support is enabled, we do
not need a database and this module only exports dummy symbols.
"""

try:
    from sqlalchemy import create_engine
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Unicode
    from sqlalchemy.orm import mapper
    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm import sessionmaker

    from zope.sqlalchemy import ZopeTransactionExtension
    WITH_DB = True
except ImportError:  # pragma: no cover
    WITH_DB = False


if WITH_DB:
    DBSession = scoped_session(
        sessionmaker(extension=ZopeTransactionExtension()))
    metadata = MetaData()

    class Upload(object):
        pass

    uploads_table = Table(
        'uploads',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('state', Unicode),
        Column('started', Integer),
        Column('tmp_path', Unicode(255)),
        Column('size', Integer),
        Column('final_path', Unicode(255)))

    mapper(Upload, uploads_table)

    def initialize_db(db_string, echo=False):
        engine = create_engine(db_string, echo=echo)
        DBSession.configure(bind=engine)
        metadata.bind = engine
        metadata.create_all(engine)
        return engine

else:  # pragma: no cover
    # Export just enough dummy symbols so that import statements from
    # other modules do not break.
    Upload = None
    DBSession = None
