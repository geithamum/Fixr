from openai import OpenAI
from typing import List, Any
import logging
from config import MODEL_NAME

logger = logging.getLogger(__name__)

def generate_solution(query: str, chunks: List[Any]) -> str:
    """
    Generate a solution using OpenAI's GPT model based on the query and relevant chunks.
    
    Args:
        query: User's question
        chunks: List of relevant document chunks
        
    Returns:
        Generated solution text
    """
    if not chunks:
        logger.warning("No context chunks provided for generation")
        return "I apologize, but I couldn't find any relevant information to answer your question."
        
    try:
        context = "\n---\n".join([c.page_content for c in chunks])
        prompt = f"""You are a technical support AI. A user has this problem: "{query}".
Here are some relevant resources:
{context}

Give a clear, step-by-step solution.
"""

        client = OpenAI()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        solution = response.choices[0].message.content
        logger.info("Successfully generated solution")
        return solution
        
    except Exception as e:
        logger.error("Failed to generate solution: %s", str(e))
        return "I apologize, but I encountered an error while generating the solution. Please try again."
