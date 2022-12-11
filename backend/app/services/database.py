from app import database


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db_session():
    db_session = database.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
