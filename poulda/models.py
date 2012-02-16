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


DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
metadata = MetaData()


class Upload(object):
    pass

uploads_table = Table(
    'uploads',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Unicode),
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
