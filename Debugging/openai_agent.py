from typing import Annotated
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

class State(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages]


model = ChatOpenAI(temperature=0)

# create node
def call_model(state: State):
    return {"messages": [model.invoke(state.messages)]}

def make_default_graph():
    builder = StateGraph(State)

    # add node
    builder.add_node("agent", call_model)

    # add edge
    builder.add_edge(START, "agent")

    agent = builder.compile()

    return agent


agent = make_default_graph()
