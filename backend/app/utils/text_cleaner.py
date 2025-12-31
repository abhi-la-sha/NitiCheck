"""
Text cleaning and normalization utilities.
"""
import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    Removes excessive whitespace, normalizes line breaks.
    """
    if not text:
        return ""
    
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def split_into_clauses(text: str, min_length: int = 50) -> List[str]:
    """
    Split document text into potential clauses.
    Uses sentence boundaries and paragraph breaks.
    
    Args:
        text: Raw document text
        min_length: Minimum clause length to include
        
    Returns:
        List of text segments (potential clauses)
    """
    if not text:
        return []
    
    # Split on sentence boundaries (period, exclamation, question mark)
    # Also split on paragraph breaks (double newline)
    clauses = []
    
    # First, split on paragraph breaks
    paragraphs = re.split(r'\n\s*\n+', text)
    
    for paragraph in paragraphs:
        paragraph = clean_text(paragraph)
        if len(paragraph) < min_length:
            continue
            
        # Split paragraph into sentences
        sentences = re.split(r'([.!?]+(?:\s+|$))', paragraph)
        
        current_clause = ""
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]
            
            sentence = clean_text(sentence)
            if not sentence:
                continue
            
            # If sentence is long enough, make it a clause
            if len(sentence) >= min_length:
                if current_clause:
                    clauses.append(current_clause)
                    current_clause = ""
                clauses.append(sentence)
            else:
                # Accumulate short sentences
                if current_clause:
                    current_clause += " " + sentence
                else:
                    current_clause = sentence
                
                # If accumulated clause is long enough, add it
                if len(current_clause) >= min_length:
                    clauses.append(current_clause)
                    current_clause = ""
        
        # Add remaining accumulated clause
        if current_clause and len(current_clause) >= min_length:
            clauses.append(current_clause)
    
    # Filter out very short clauses
    return [c for c in clauses if len(c) >= min_length]


def extract_numbers(text: str) -> List[float]:
    """
    Extract all numeric values (including percentages) from text.
    
    Returns:
        List of extracted numbers
    """
    # Match percentages (e.g., "18%", "18.5%")
    percentage_pattern = r'(\d+\.?\d*)\s*%'
    percentages = re.findall(percentage_pattern, text)
    
    # Match regular numbers (e.g., "18", "18.5")
    number_pattern = r'\b(\d+\.?\d*)\b'
    numbers = re.findall(number_pattern, text)
    
    # Convert to floats
    all_numbers = []
    for num_str in percentages + numbers:
        try:
            all_numbers.append(float(num_str))
        except ValueError:
            continue
    
    return all_numbers

