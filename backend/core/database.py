from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///database.db", echo=True)

def get_session() -> Session:
    with Session(engine) as session:
        yield session