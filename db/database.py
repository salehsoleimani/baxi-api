from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

engine = create_engine(url="postgresql://root:8udQgORdzInF3xx3WGDrJhSI@tai.liara.cloud:31299/baxi",
                       )

Base = automap_base()
Base.prepare(engine, reflect=True)


session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    session = session_local()
    try:
        yield session
    finally:
        session.close()
