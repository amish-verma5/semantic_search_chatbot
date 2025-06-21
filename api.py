from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from main import result
from main import SemanticRAG
import logging
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    user_query: str
    k:int

@app.post("/chat")
async def chat(query: Query):
    user_query = query.user_query
    k = query.k
    logger.info("Parameter received")
    logger.info(f"User querry: {user_query}")
    logger.info(f"Value of k is: {k}")

    semantic_rag = SemanticRAG()
    reply = semantic_rag.chatbot_(user_query,k)
    return {"reply": reply}