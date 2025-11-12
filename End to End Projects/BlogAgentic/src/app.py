import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from src.graphs.graphbuilder import GraphBuilder
from src.llms.groqllm import GroqLLM


import os
from dotenv import load_dotenv

from src.states.blog_state import Blog, BlogState
load_dotenv()


os.environ["LANGSMITH_API_KEY"] = os.getenv('LANGSMITH_API_KEY', '')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API ROUTES
@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic: str = data.get("topic", "")
    
    # get the llm object
    groq_llm = GroqLLM().get_llm()
    
    # get the graph
    graph_builder = GraphBuilder(groq_llm)
    
    if topic:
        graph = graph_builder.setup_graph()
        state = BlogState(
            topic=topic,
            blog = Blog(title="", content=""),
            current_language="en"
        )
        response = graph.invoke(state)
    
        return {"data": response}
    return HTTPException(status_code=500, detail="Could Not Get Response from Agent")