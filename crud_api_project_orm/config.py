from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_port: str
    database_name: str
    database_password: str
    secret_key: str
    password_hash_algorithm: str = "HS256"
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()