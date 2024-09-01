import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


def gpt_response(prompt):
    """Generate an embedding for the given prompt using Google Gemini API."""
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=prompt,
            task_type="retrieval_document",
            title="Embedding of single string"
        )
        
        embedding = result.get('embedding', None)
        if embedding is None:
            print("Embedding not found in result:", result)
            return [0] * 768 
        
        if not isinstance(embedding, list):
            print(f"Expected list, got {type(embedding)}: {embedding}")
            return [0] * 768
        
        if len(embedding) != 768:
            print(f"Unexpected embedding size: {len(embedding)}")
            if len(embedding) < 768:
                embedding.extend([0] * (768 - len(embedding)))
            elif len(embedding) > 768:
                embedding = embedding[:768]
        
        return embedding

    except Exception as e:
        print(f"Failed to get embedding: {e}")
        return [0] * 768
