"""
API endpoint for document analysis.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import DocumentAnalysis
from app.services.document_loader import DocumentLoader
from app.services.risk_analyzer import RiskAnalyzer
from app.core.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS

router = APIRouter()


@router.post("/analyze", response_model=DocumentAnalysis)
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze uploaded financial document for risk clauses.
    
    Args:
        file: Uploaded PDF or DOCX file
        
    Returns:
        DocumentAnalysis with identified risk clauses
        
    Raises:
        HTTPException: If file validation fails or processing error occurs
    """
    # Validate file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_extension = "." + file.filename.split('.')[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )
    
    # Reset file pointer for processing
    await file.seek(0)
    
    try:
        # Extract text from document
        text = await DocumentLoader.extract_text(file)
        
        if not text or len(text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from document. "
                       "File may be corrupted, image-based, or empty."
            )
        
        # Analyze text for risks
        clauses = RiskAnalyzer.analyze_document(text)
        
        # Return analysis results
        return DocumentAnalysis(clauses=clauses)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

