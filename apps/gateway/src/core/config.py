import os


class Settings:
    PROJECT_NAME: str = "QEVN Workforce API Gateway"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    CLERK_JWKS_URL: str = os.getenv("CLERK_JWKS_URL", "https://api.clerk.com/v1/jwks")
    CLERK_AUDIENCE: str = os.getenv("CLERK_AUDIENCE", "qevn-workforce")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/qevn"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # downstream orchestrator gRPC/HTTP URL
    ORCHESTRATOR_URL: str = os.getenv("ORCHESTRATOR_URL", "http://localhost:8001")


settings = Settings()
