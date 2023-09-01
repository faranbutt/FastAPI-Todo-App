from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = f'postgresql://faranbutt:bFQ0sXL7yEpj@ep-morning-smoke-895844.us-east-2.aws.neon.tech/fastapi_todos'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()
