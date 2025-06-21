from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from main import result
from semanticonly_7 import chatbot_

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
    k=query.k
    print("printing querry")
    print(user_query)
    print(f"the value of k i s:{k}")
    reply =chatbot_(user_query,k)
    return {"reply": reply}