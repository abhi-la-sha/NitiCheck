"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.analyze import router as analyze_router
from app.core.config import ALLOWED_ORIGINS, API_PREFIX

# Create FastAPI application
app = FastAPI(
    title="Financial Document Risk Analysis API",
    description="Backend API for analyzing financial documents and identifying risk clauses",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analyze_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Financial Document Risk Analysis API",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

