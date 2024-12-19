from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config import DB_NAME, DB_PASSWORD, DB_URL, DB_USER

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"
)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()
