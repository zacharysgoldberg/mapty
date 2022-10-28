# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from redis_om import get_redis_connection
import os
from dotenv import load_dotenv

load_dotenv()

# should be imported from original app
redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)


# SQLALCHEMY_DATABASE_URI = "postgresql://postgres@db:5432/pizza-drone"


# engine = create_engine(SQLALCHEMY_DATABASE_URI)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# def db():
#     try:
#         db = SessionLocal()
#         yield db

#     finally:
#         db.close()
