from sqlmodel import Session, create_engine

async def get_session() -> Session:
    engine = create_engine("sqlite:///database.db")
    with Session(engine) as session:
        yield session