from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "mssql+pyodbc://user:password@localhost:1433/ClearOps?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]


settings = Settings()
