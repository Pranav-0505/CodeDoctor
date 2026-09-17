import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Code Doctor"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Secret Key for JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "code-doctor-super-secret-key-change-in-production-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./code_doctor.db")
    
    # AI Engine Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ENABLE_AI_ENHANCEMENT: bool = True
    
    # Security & Verification
    SAFE_VERIFICATION_ONLY: bool = True
    MAX_PROJECT_FILE_SIZE_MB: int = 10
    MAX_PROJECT_FILES: int = 500
    
    # Platform / CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

settings = Settings()
