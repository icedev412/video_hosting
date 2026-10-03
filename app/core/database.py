from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL =  "postgresql+psycopg2://postgres:12Seele12@localhost:5432/video_hosting"


engine = create_engine(
    DATABASE_URL,
    echo=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db #yield is used to create a generator function that can be used as a dependency in FastAPI. It allows the function to return a value (in this case, the database session) and then continue executing after the request is completed. This is useful for managing resources like database connections, as it ensures that the connection is properly closed after the request is finished.
    finally:
        db.close()