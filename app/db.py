from sqlmodel import create_engine

from app.settings import settings

# from app.models.models import *
print(str(settings.SQLALCHEMY_DATABASE_URI))
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
