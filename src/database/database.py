from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from src.config import config

engine = create_engine(url=config.settings.DATABASE_URL)

# Map Existing Tables to Base Model
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.metadata.create_all(engine)

session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    session = session_local()
    try:
        yield session
    finally:
        session.close()
