import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./data/database.db"


engine = sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sql.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
