from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from ministac.globals import DB_DATABASE, DB_HOSTNAME, DB_PASSWORD, DB_USERNAME

db_params = {'drivername': 'postgresql',
             'database': DB_DATABASE,
             'username': DB_USERNAME,
             'host': DB_HOSTNAME,
             'password': DB_PASSWORD}

db_url = URL(**db_params)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    import ministac.models
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope(Session=Session):
    """Provide a transactional scope around a series of operations.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
