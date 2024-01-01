from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

from sqlalchemy.engine import URL

# url_object = URL.create(
#     "postgresql",
#     username="postgres",
#     password="password",  # plain (unescaped) text
#     host="localhost",
#     database="fastapi",
# )

SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql",
    username=settings.database_username,
    password=settings.database_password,  # plain (unescaped) text
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name
)

# print(url_object)

#SQLALCHEMY_DATABASE_URL = """postgresql://postgres:'password'@localhost:5432/fastapi"""

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# print(SQLALCHEMY_DATABASE_URL)

# engine = create_engine(url_object)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password='password', cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connecgting to database failed")
#         print("Error: ", error) 
#         time.sleep(2)  
