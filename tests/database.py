# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.database import get_db
# from app.database import Base

# from sqlalchemy.engine import URL


# SQLALCHEMY_DATABASE_URL = URL.create(
#     "postgresql",
#     username="postgres",
#     password="Aarav@2010",  # plain (unescaped) text
#     host="localhost",
#     port=5432,
#     database="fastapi_test"
# )


# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
            
#     app.dependency_overrides[get_db] = override_get_db   
#     yield TestClient(app)    