from datetime import timedelta
import os

databaseUrl=os.environ["DATABASE_URL"] #if os.environ["DATABASE_URL"] else "localhost:3308" #if "PRODUCTION" in os.environ else "local


class Configuration():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:123@{databaseUrl}/authentication"
    JWT_SECRET_KEY="JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)
