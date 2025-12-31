"""
Application configuration settings.
"""
from typing import List

# CORS origins - allow frontend to make requests
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
]

# File upload settings
MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx"]

# API settings
API_PREFIX: str = "/api"

