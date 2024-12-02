from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModel
import torch
import uvicorn
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize tokenizer and model
model_name = "microsoft/codebert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Neo4j connection
neo4j_uri = os.getenv('NEO4J_URI', 'bolt://neo4j:7687')
neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')

neo4j_driver = GraphDatabase.driver(
    neo4j_uri,
    auth=(neo4j_user, neo4j_password)
)

@app.get("/")
def read_root():
    return {"status": "NLP Service is running"}

@app.post("/encode")
async def encode_text(text: str):
    try:
        # Tokenize and encode text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get embeddings (use mean pooling)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        
        return {
            "embeddings": embeddings[0].tolist(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze_pattern")
async def analyze_pattern(code: str):
    try:
        # Encode the code
        inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1)
        
        # Query Neo4j for similar patterns
        with neo4j_driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                RETURN p.name, p.description
                LIMIT 5
            """)
            patterns = [{"name": record["p.name"], "description": record["p.description"]}
                       for record in result]
        
        return {
            "patterns": patterns,
            "embeddings": embeddings[0].tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
