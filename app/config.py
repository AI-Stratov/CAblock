"""Config file for the application."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str

    db_host_test: str
    db_port_test: str
    db_name_test: str
    db_user_test: str
    db_pass_test: str

    alembic_test_config: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def sql_alchemy_database_url(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def database_url_test(self):
        return f"postgresql://{self.db_user_test}:{self.db_pass_test}@{self.db_host_test}:{self.db_port_test}/{self.db_name_test}"


settings = Settings()
