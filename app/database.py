# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from redis_om import get_redis_connection

# should be imported from original app
redis = get_redis_connection(
    host="redis-17133.c53.west-us.azure.cloud.redislabs.com",
    port=17133,
    password="Dh2KdAJnHd7SSppW8ySSJzjnAeFXXXjk",
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
